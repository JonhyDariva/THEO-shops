import json, re, sys, difflib
from faster_whisper import WhisperModel

# transcreve com tempo por palavra e encaixa o texto do roteiro nesses tempos
# uso: python3 transcribe.py <lang> <roteiro.txt> <audio> <saida.json>
lang, tf, af, outp = sys.argv[1:5]

import numpy as np
from scipy.io import wavfile
sr, x = wavfile.read(af)
audio = x.astype(np.float32) / 32768
model = WhisperModel('small', device='cpu', compute_type='int8')
segs, _ = model.transcribe(audio, language=lang, word_timestamps=True, vad_filter=True, vad_parameters={'min_silence_duration_ms': 150, 'speech_pad_ms': 60}, beam_size=5, condition_on_previous_text=False)
asr = [w for s in segs for w in s.words]
print('reconhecido:', ' '.join(w.word.strip() for w in asr))

norm = lambda w: re.sub(r"[^\w]", '', w.lower())
script = open(tf).read().split()
a = [norm(w) for w in script]
b = [norm(w.word) for w in asr]

# casa palavra do roteiro com palavra reconhecida
match = {}
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            match[i1 + k] = (asr[j1 + k].start, asr[j1 + k].end)
    elif tag == 'replace' and j2 > j1:
        # distribui o trecho reconhecido entre as palavras do roteiro (ex: "1924" lido por extenso)
        t0, t1 = asr[j1].start, asr[j2 - 1].end
        n = i2 - i1
        for k in range(n):
            match[i1 + k] = (t0 + (t1 - t0) * k / n, t0 + (t1 - t0) * (k + 1) / n)

# palavras sem correspondência: interpola entre vizinhas
times = [match.get(i) for i in range(len(script))]
for i in range(len(times)):
    if times[i] is None:
        prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0)
        nxt = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), prev + 0.3)
        times[i] = (prev, max(prev + 0.05, nxt))
print('casadas', len([m for m in match]), 'de', len(script))

words = [{'w': w.strip('.,?!:…'), 't0': round(t[0], 3), 't1': round(t[1], 3),
          'p': bool(re.search(r'[.?!…:]$', w)), 'c': bool(re.search(r',$', w))} for w, t in zip(script, times)]
# agrupa em frases (fim de frase) para manter o formato dos outros arquivos
out, cur = [], []
for w in words:
    cur.append(w)
    if w['p']:
        out.append({'t0': cur[0]['t0'], 't1': cur[-1]['t1'], 'words': cur}); cur = []
if cur:
    out.append({'t0': cur[0]['t0'], 't1': cur[-1]['t1'], 'words': cur})
json.dump(out, open(outp, 'w'), ensure_ascii=False, indent=1)
for s in out:
    print(f"{s['t0']:6.2f}-{s['t1']:6.2f}  {' '.join(x['w'] for x in s['words'])}")
