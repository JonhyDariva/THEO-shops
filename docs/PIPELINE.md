# pipeline (como ficou depois do short 001)

regra central: o áudio manda. a fala de cada cena é gravada primeiro e tudo se encaixa nela.
regra herdada do the real coin: o tempo da legenda vem do áudio real transcrito, nunca de estimativa.

## etapas
| # | etapa | ferramenta | quem |
|---|---|---|---|
| 1 | roteiro em cenas | roteiros/NNN.json | claude propõe, joão aprova |
| 2 | voz, uma fala por cena | elevenlabs tts (eleven_v4, voz do theo) | claude |
| 3 | quadro inicial de cada tipo de plano | elevenlabs imagem (gemini-3-pro-image, 9:16) com a ficha ligada | claude, joão aprova |
| 4 | atuação | veo 3.1 fast, start_frame = quadro, 9:16, 720p, sem áudio | claude |
| 5 | boca | sync-lipsync-v3 com o clipe do veo + a fala | claude |
| 6 | trilha | elevenlabs música, instrumental, sem intro nem final | claude |
| 7 | download | baixar.bat gerado por motor/links.py | joão roda |
| 8 | montagem + legenda | motor/montar.py (ffmpeg + faster-whisper) | claude ou joão |
| 9 | postagem e métricas | metricool / youtube | joão |

## decisões e o motivo
- veo + dublagem em vez de lip sync direto na imagem: nota 9,5 contra 5,5 no teste da cena 1.
- veo sem áudio nativo: a voz dele é descartada na dublagem e desligar economiza um terço do custo.
- quadros reaproveitados: um close e um plano médio servem pra várias cenas. só cena com cenário diferente pede quadro novo.
- cena em que a boca não aparece (objeto, plano aberto) não é dublada: a fala entra por cima na montagem.
- a dublagem recomprime o áudio. por isso a montagem tira o som dos clipes e usa a fala original.
- a dublagem corta o clipe no tamanho da fala (cut_off). pra cena que precisa do último quadro (loop), usar sync_mode remap.
- legenda queimada por ffmpeg (ass), não por remotion: as cenas já são vídeo pronto. estilo copiado do common.jsx do trc.
- loop: a última fala termina em vírgula ("e é por isso que,") e a última cena termina no quadro inicial da cena 1.

## limites conhecidos
- buzzy: o plano atual não tem ambiente de execução e o upload dele falha dentro do claude. fora do pipeline por enquanto.
- o claude não consegue baixar arquivos do elevenlabs. por isso existe o baixar.bat.
- o conversor de voz do canvas não aceita vídeo como entrada.
- o canvas do elevenlabs cria nós com proporção 16:9 por padrão. sempre configurar 9:16 no nó antes de rodar.

## custo
short 001 inteiro, com todos os testes e erros: cerca de 91 mil créditos (perto de us$ 16,50).
estimativa de um short de 12 cenas reaproveitando ficha e quadros base: 60 a 70 mil créditos.

| item | créditos |
|---|---|
| fala de uma cena | 35 a 65 |
| quadro (1 variação) | 1.827 |
| veo fast sem áudio, 4s / 6s | 2.424 / 3.636 |
| dublagem (cobra pela duração da fala) | 2.200 a 3.500 |
| trilha de 42s | 630 |

gargalo: o plano pro do elevenlabs dá 120 mil créditos por mês, ou seja, menos de 2 shorts nesse formato.
caminhos pra baratear, em ordem de impacto:
1. roteiro mais curto (8 a 9 cenas, 30s).
2. menos cenas dubladas: mais cenas de objeto ou plano aberto, que só custam o veo.
3. reaproveitar clipes de reação do theo entre shorts (biblioteca em clipes/base/).
4. testar veo 3.1 lite nas cenas sem rosto.
5. gerar os clipes do veo pela assinatura do google e subir à mão (quebra a automação, mas zera esse custo).
