# handoff

## estado atual (11/11/2026, claude)
- pasta criada e estruturada. ficha do theo gerada e aprovada (ver docs/PERSONAGEM.md). nenhum vídeo ainda.
- pipeline definido em docs/PIPELINE.md, personagem em docs/PERSONAGEM.md.
- buzzy e elevenlabs conectados no claude.

## próximo passo
1. salvar a ficha em personagem/theo-ficha.png.
2. escolher tema do primeiro short e escrever o roteiro em roteiros/.
3. teste de 3 segundos de fala pra comparar os dois caminhos de lip sync.

## limites encontrados
- buzzy: o plano atual não inclui o ambiente de execução (sem ffmpeg lá) e o seletor de upload falha dentro do claude. imagens entram no buzzy só por link público.
- elevenlabs: aceita upload pelo seletor dele e tem veo 3.1, kling 4, seedance 2.5 e lip sync dedicado. por enquanto é o caminho mais confiável.
