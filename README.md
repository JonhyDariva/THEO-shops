# theo shops — fábrica de animação (the real coin)

shorts de economia em cartoon com o theo, produzidos por um pipeline de apis.
este projeto não tem relação com o P.1 / pasta AntiGravity. o motor de legenda veio do projeto TheRealCoin (pasta trc).

## como nasce um short
1. roteiro: `roteiros/NNN.json` (fala, emoção, quadro e ação de cada cena)
2. geração no elevenlabs (quem faz é o claude, pelo conector): voz, quadros, atuação no veo, dublagem
3. download: `git pull` e `baixar.bat` (o claude gera o .bat com os links)
4. montagem: `python3 motor/montar.py NNN tudo` -> `final/NNN.mp4` + `final/NNN.txt`

passo a passo completo: `docs/RUNBOOK.md`. por que cada escolha: `docs/PIPELINE.md`.

## pastas
- docs/        pipeline, runbook, personagem e handoff
- personagem/  ficha do theo (referência de todo clipe)
- roteiros/    NNN.json (fonte única do short) e anotações de produção
- motor/       montar.py (montagem + legenda), transcribe.py (tempo por palavra), links.py (gera o baixar.bat)
- clipes/NNN/  cNN.mp4, um por cena (não vai pro git)
- audio/NNN/   fNN.mp3, uma fala por cena, e trilha.mp3 (não vai pro git)
- out/         arquivos intermediários (não vai pro git)
- final/       vídeo pronto e kit de postagem
