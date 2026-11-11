#!/usr/bin/env python3
"""monta um short do theo a partir dos clipes e das falas.

  python3 motor/montar.py 001 tudo      faz as três etapas abaixo em sequência e para se o check falhar
  python3 motor/montar.py 001 base      junta clipes + narração limpa -> out/001_base.mp4 e out/001_narr.wav
  python3 motor/montar.py 001 tempo     transcreve a narração (faster-whisper) -> out/001_tm.json + check
  python3 motor/montar.py 001 final     queima legenda e mixa a trilha -> final/001.mp4 + final/001.txt
  python3 motor/montar.py 001 final y=1100 vol=0.1    ajusta altura da legenda e volume da trilha sem refazer o resto

entradas: roteiros/001.json, clipes/001/cNN.mp4, audio/001/fNN.mp3, audio/001/trilha.mp3

regra herdada do motor do the real coin: o tempo da legenda vem do áudio real transcrito, nunca de estimativa.
"""
import json, os, re, subprocess, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(R, *a)
FPS = 24
W, H = 1080, 1920


def run(*c):
    subprocess.run(list(c), check=True)


def dur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).decode())


def plano(n):
    return json.load(open(P('roteiros', f'{n}.json')))


def midia(pasta, n, nome):
    # prefere a subpasta do short (clipes/001/c01.mp4); aceita o formato antigo (clipes/c01.mp4)
    a = P(pasta, n, nome)
    return a if os.path.exists(a) else P(pasta, nome)


def base(n):
    pl = plano(n)
    os.makedirs(P('out', n), exist_ok=True)
    vs, au, t = [], [], 0.0
    for i, c in enumerate(pl['cenas'], 1):
        k = f'{i:02d}'
        clip, fala = midia('clipes', n, f'c{k}.mp4'), midia('audio', n, f'f{k}.mp3')
        cd, ad = dur(clip), dur(fala)
        modo = c.get('modo', 'dublado')
        if modo == 'dublado':        # clipe já cortado no tamanho da fala
            alvo, pts = cd, 1.0
        elif modo == 'acelera':      # cena sem boca: acelera o clipe pra caber na fala
            alvo = round((ad + 0.1) * FPS) / FPS
            pts = alvo / cd
        else:                        # corta
            alvo, pts = round((ad + 0.05) * FPS) / FPS, 1.0
        fr = round(alvo * FPS)
        alvo = fr / FPS
        o = P('out', n, f'v{k}.mp4')
        run('ffmpeg', '-y', '-v', 'error', '-i', clip, '-an', '-vf',
            f'setpts={pts:.5f}*PTS,fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1', '-frames:v', str(fr),
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', o)
        a = P('out', n, f'a{k}.wav')
        run('ffmpeg', '-y', '-v', 'error', '-i', fala, '-af', f'apad,atrim=0:{alvo:.5f}', '-ar', '48000', '-ac', '2', a)
        vs.append(o); au.append(a)
        c['t0'], c['t1'] = round(t, 4), round(t + alvo, 4)
        t += alvo
        print(f'cena {k} {modo:8s} clipe {cd:.2f}s fala {ad:.2f}s -> {alvo:.3f}s')
    lv, la = P('out', n, 'v.txt'), P('out', n, 'a.txt')
    open(lv, 'w').write(''.join(f"file '{x}'\n" for x in vs))
    open(la, 'w').write(''.join(f"file '{x}'\n" for x in au))
    run('ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', la, '-c', 'copy', P('out', f'{n}_narr.wav'))
    run('ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lv, '-i', P('out', f'{n}_narr.wav'),
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', P('out', f'{n}_base.mp4'))
    json.dump({'total': round(t, 4), 'cenas': pl['cenas']}, open(P('out', f'{n}_cenas.json'), 'w'), ensure_ascii=False, indent=1)
    print('total', round(t, 3), 's ->', P('out', f'{n}_base.mp4'))


def tempo(n):
    pl = plano(n)
    tf = P('out', f'{n}.txt')
    open(tf, 'w').write('\n'.join(c['fala'] for c in pl['cenas']) + '\n')
    wav = P('out', f'{n}_16k.wav')
    run('ffmpeg', '-y', '-v', 'error', '-i', P('out', f'{n}_narr.wav'), '-ac', '1', '-ar', '16000', wav)
    run(sys.executable, P('motor', 'transcribe.py'), pl.get('lang', 'pt'), tf, wav, P('out', f'{n}_tm.json'))
    try:
        os.remove(wav)
    except OSError:
        pass
    check(n)


def check(n):
    # cada palavra do roteiro tem que cair dentro da cena a que pertence (tolerância 0.35s)
    cs = json.load(open(P('out', f'{n}_cenas.json')))['cenas']
    ws = [w for s in json.load(open(P('out', f'{n}_tm.json'))) for w in s['words']]
    i, ruim = 0, 0
    for k, c in enumerate(cs, 1):
        for _ in c['fala'].split():
            w = ws[i]; i += 1
            if not (c['t0'] - 0.35 <= w['t0'] <= c['t1'] + 0.35):
                ruim += 1
                print(f"  fora da cena {k:02d}: '{w['w']}' em {w['t0']:.2f}s (cena {c['t0']:.2f}-{c['t1']:.2f})")
    print('check:', 'ok, todas as palavras caem na cena certa' if not ruim else f'{ruim} palavra(s) fora do lugar')
    return ruim


def chunks(tm):
    # mesma regra do common.jsx: até 3 palavras, quebra em vírgula/fim de frase, junta blocos com menos de 0.45s
    raw = []
    for s in tm:
        cur = []
        for w in s['words']:
            cur.append(w)
            if len(cur) == 3 or w['p'] or w['c']:
                raw.append(cur); cur = []
        if cur:
            raw.append(cur)
    out, i = [], 0
    while i < len(raw):
        ch = raw[i]
        nx = raw[i + 1] if i + 1 < len(raw) else None
        if nx and nx[0]['t0'] - ch[0]['t0'] < 0.45 and len(ch) + len(nx) <= 4 and not ch[-1]['p']:
            raw[i + 1] = ch + nx
        else:
            out.append(ch)
        i += 1
    return out


def ts(t):
    t = max(0, t)
    return f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}'


def ass(n, total, y):
    tm = json.load(open(P('out', f'{n}_tm.json')))
    ch = chunks(tm)
    off, mus, deep = '&H00E3EFF4', '&H003FB7E8', '&H0026140A'   # cores do data.js do motor (bgr)
    L = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {W}', f'PlayResY: {H}', 'WrapStyle: 2', 'ScaledBorderAndShadow: yes', '',
         '[V4+ Styles]',
         'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
         f'Style: c,Poppins,92,{off},{off},{deep},{deep},-1,0,0,0,100,100,-1,0,1,8,0,5,40,40,0,1', '',
         '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    for i, c in enumerate(ch):
        fim = ch[i + 1][0]['t0'] if i + 1 < len(ch) else min(total, c[-1]['t1'] + 0.3)
        for k, w in enumerate(c):
            a = w['t0'] if k else c[0]['t0']
            b = c[k + 1]['t0'] if k + 1 < len(c) else fim
            if b - a < 0.02:
                continue
            txt = ' '.join((f'{{\\c{mus}}}' if j == k else f'{{\\c{off}}}') + x['w'].lower() for j, x in enumerate(c))
            pop = '\\fscx88\\fscy88\\t(0,120,\\fscx100\\fscy100)' if k == 0 else ''
            L.append(f'Dialogue: 0,{ts(a)},{ts(b)},c,,0,0,0,,{{\\an5\\pos({W // 2},{y}){pop}}}{txt}')
    f = P('out', f'{n}.ass')
    open(f, 'w').write('\n'.join(L) + '\n')
    return f


def final(n, y=None, vol=None):
    pl = plano(n)
    y = int(y if y is not None else pl.get('legenda_y', 1200))
    vol = float(vol if vol is not None else pl.get('trilha_vol', 0.07))
    total = json.load(open(P('out', f'{n}_cenas.json')))['total']
    f = ass(n, total, y)
    os.makedirs(P('final'), exist_ok=True)
    o = P('final', f'{n}.mp4')
    run('ffmpeg', '-y', '-v', 'error', '-i', P('out', f'{n}_base.mp4'), '-stream_loop', '-1', '-i', midia('audio', n, 'trilha.mp3'),
        '-filter_complex',
        f"[0:v]ass='{f}'[v];[1:a]volume={vol}[m];[0:a]volume=1.0[n];[n][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
        '-map', '[v]', '-map', '[a]', '-t', f'{total:.4f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', o)
    # kit de postagem, igual ao motor do the real coin
    kit = f"{pl.get('titulo', '')}\n\n{pl.get('descricao', '')}\n\n{pl.get('hashtags', '')}\n"
    open(P('final', f'{n}.txt'), 'w').write(kit)
    print('pronto ->', o, f'({dur(o):.2f}s, legenda em y={y}, trilha em {vol})')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    n, cmd = sys.argv[1], sys.argv[2]
    kw = dict(a.split('=') for a in sys.argv[3:])
    if cmd == 'base': base(n)
    elif cmd == 'tempo': tempo(n)
    elif cmd == 'check': sys.exit(1 if check(n) else 0)
    elif cmd == 'final': final(n, kw.get('y'), kw.get('vol'))
    elif cmd == 'tudo':
        base(n); tempo(n)
        if check(n):
            sys.exit('check falhou: não renderizei. confira as falas e os áudios.')
        final(n, kw.get('y'), kw.get('vol'))
    else:
        sys.exit(__doc__)
