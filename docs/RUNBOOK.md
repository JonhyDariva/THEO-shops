# runbook: produzir o short NNN

quem executa: o claude, numa conversa do projeto theo shops, com o conector do elevenlabs ligado
e a pasta `Desktop\THEO shops` conectada. o joão aprova nos pontos marcados com [aprovação].

## 0. antes de começar
- ler docs/PIPELINE.md e este arquivo. perguntar o saldo de créditos do elevenlabs (o claude não enxerga).
- canvas do theo: 6tdJSdyQmuLRNEAgbtyr. ficha: nó DPWxsGdlMRVpfzL16Wii.
- quadros base já aprovados: close if1ibDkSqwXHwYXh4ojP, plano médio com balança aXDYUYOM4sC7xBHNvFkm.
- voz do theo: MK5tXPmT83J5SUlpUo4K (antonio de jesus), modelo eleven_v4.

## 1. roteiro [aprovação]
- 8 a 12 cenas, uma fala curta por cena (até 11 palavras, cerca de 4s), 100 a 110 palavras no total.
- "você", sem números específicos, primeira frase é o gancho.
- loop: a última fala termina aberta e em vírgula, emendando na primeira.
- alternar close, plano médio e pelo menos duas cenas de objeto ou plano aberto.
- salvar em roteiros/NNN.json no formato do 001.json (fala, emocao, quadro, dur, modo, acao).

## 2. voz
- uma chamada de tts por cena, 1 take, no canvas do theo. anotar o nó de cada fala.
- consultar a duração de cada fala. acima de 3,9s a cena usa clipe de 6s.

## 3. quadros novos [aprovação]
- só pra cenário que ainda não existe. gemini-3-pro-image, ficha (ou quadro base) ligada como referência.
- criar o nó com estimate_only, configurar aspect_ratio 9:16 e resolution 1K com update_node, ligar a referência, rodar com 1 variação.
- pedir no prompt: sem texto, sem letras, sem logos, topo da imagem calmo.

## 4. atuação e boca
por cena com rosto:
1. criar o nó do veo (veo-3.1-fast-generate-001) com estimate_only e o prompt de atuação.
2. update_node: duration_secs 4 ou 6, aspect_ratio 9:16, resolution 720p, generate_audio false.
3. ligar o quadro em start_frame (na cena do loop, ligar também o quadro da cena 1 em end_frame).
4. criar o nó de dublagem (sync-lipsync-v3) com estimate_only, connect_from [nó do veo, nó da fala].
   na cena do loop: update_node com sync_mode remap.
5. rodar SÓ o nó de dublagem. ele puxa o veo sozinho. rodar os dois gera o veo em dobro.

por cena sem rosto: passos 1 a 3 e rodar o nó do veo. sem dublagem.

modelo de prompt de atuação (em inglês):
"Starting exactly from this frame. The cartoon scientist talks fast straight to the camera, mouth moving clearly
as he speaks. Acting: <emoção>. <gestos, um por frase da fala>. <o que não pode se mexer>. Camera locked,
<plano>, background unchanged. 3D vinyl-toy animation style. No text, no subtitles."
o joão gosta de atuação com bastante movimento: sempre pedir gesto de mão, sobrancelha e cabeça.

mostrar a primeira cena pronta antes de disparar o resto. [aprovação]
depois rodar em lotes de 3 a 4 cenas e avisar o custo de cada lote.

## 5. trilha
- reaproveitar audio/001/trilha.mp3 se servir. senão: nó music, eleven_music_v2_5, duration_seconds 42,
  instrumental, 2 variações, pedindo "no intro, no fade, no final hit". [aprovação]

## 6. download
- consultar creative_get_flow_run_status com as sessões finais. o resultado é grande e fica salvo em arquivo.
- montar o mapa destino -> generation_id (clipes/NNN/cNN.mp4, audio/NNN/fNN.mp3, audio/NNN/trilha.mp3).
  clipe de cena dublada = geração do sync. cena sem rosto = geração do veo.
- python3 motor/links.py NNN status.json mapa.json > baixar.bat, commit e push pelo clone do claude.
- o joão roda `git pull` e `baixar.bat`. os links vencem em cerca de 2 horas.

## 7. montagem
- na pasta conectada: python3 motor/montar.py NNN tudo
  (o ambiente do claude precisa de: pip install faster-whisper scipy)
- no ambiente do claude cada chamada dura no máximo 3 minutos e processo em segundo plano morre no fim da chamada.
  por isso rodar em duas chamadas: `base` + `tempo` numa, `final` na outra. no pc do joão o `tudo` roda direto.
- o check tem que dizer que todas as palavras caem na cena certa. se não disser, não entregar.
- ajustes sem custo: python3 motor/montar.py NNN final y=<altura da legenda> vol=<volume da trilha>

## 8. entrega [aprovação]
- final/NNN.mp4 e final/NNN.txt (título, descrição, hashtags).
- o claude não consegue assistir o vídeo: pedir pro joão conferir posição da legenda, volume da trilha e o loop.
- atualizar docs/HANDOFF.md e pedir o commit.

## erros que já aconteceram
- quadro saiu horizontal: proporção é configuração do nó, não do prompt.
- veo gerado em dobro: disparei veo e dublagem juntos.
- fala terminando em reticências sai cortada: usar vírgula.
- painel do chat para de atualizar com muitos nós: mandar o link do canvas.
- os.remove falha na pasta conectada: o ambiente do claude não pode apagar arquivos ali.
