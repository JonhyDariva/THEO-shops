# pipeline

regra central: o áudio manda. a voz é gerada primeiro e vira a régua de tudo.

1. roteiro: dividido em falas curtas, cada fala com emoção e enquadramento.
2. voz: elevenlabs, com timestamps por caractere.
3. legenda: gerada dos timestamps, 2 palavras por vez, minúscula, branca com sombra, centro.
4. cenas: um clipe de 2 a 4s por fala, sempre com a ficha do personagem como referência.
5. lip sync: aplicado no clipe usando o áudio do elevenlabs (voz igual no vídeo inteiro).
6. montagem: ffmpeg, cortes a cada 1-2s alternando plano médio e close, legenda queimada, música.
7. métricas: api do youtube, alimentando o próximo roteiro.

## ferramentas conectadas (11/11/2026)
- buzzy (mcp): imagem, vídeo (veo 3.1, kling 4, seedance 2.5), áudio, sandbox com ffmpeg.
- elevenlabs (mcp): voz, e também vídeo e modelos de lip sync dedicados.

## em aberto
- qual caminho de lip sync fica melhor no personagem: fala nativa do modelo de vídeo ou lip sync dedicado em cima do áudio.
- custo real por short (o buzzy não mostra créditos antes de gerar).
- plano anual do veo: só decidir depois do primeiro short pronto.
