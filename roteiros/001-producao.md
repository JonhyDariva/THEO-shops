# 001 — produção (ids no elevenlabs)

canvas: 6tdJSdyQmuLRNEAgbtyr
voz do theo: antonio de jesus (voice_id MK5tXPmT83J5SUlpUo4K), modelo eleven_v4
ficha (nó): DPWxsGdlMRVpfzL16Wii

## receita aprovada por cena (cena 1 = nota 9,5)
1. quadro inicial: gemini-3-pro-image, aspect_ratio 9:16 configurado no nó (o padrão é 16:9), ficha ligada como referência. ~1.827 créditos
2. atuação: veo-3.1-fast, start_frame = quadro, 9:16, 720p, 4s (6s em fala longa), fala no prompt. ~3.636 créditos em 4s
3. dublagem: sync-lipsync-v3 com o clipe do veo + áudio da voz do theo. ~3.159 créditos
total por cena: ~8.600 créditos (~us$ 1,60)

descartado: omnihuman (imagem + áudio) deu nota 5,5.
não funciona: voice changer não aceita vídeo como entrada no canvas.

## nós de áudio (voz do theo)
| cena | nó |
|---|---|
| 1 | 3AxCAuTq8zsEul8QkCaK |
| 2 | YctqVaQqcgiBUSrQmcpo |
| 3 | ZEEAQOTWxGtx30BzGOnC |
| 4 | ikOAkGj8lgKf7KGmEvc1 |
| 5 | ZYZEaueL22JevjJLa6Ad |
| 6 | 8T7P5Uu3xJVtzf7xU5pO |
| 7 | ayQRzcywGplbpjYmoDAG |
| 8 | wkKWF5rkFoe7ga4DiQBd |
| 9 | u4ZWWyTPfYW8zZGUtfBG |
| 10 | sXQZ9YoQLkiHL7v3QEI9 |
| 11 | 7l1jVfOc6vYYm5vnUHqF |
| 12 | 5NPGylQFf29oZCWqk5nv |

## cena 1 (pronta)
- quadro: if1ibDkSqwXHwYXh4ojP (geração qRUSiVtE5EL76Ml99DUu)
- veo: NBFCFkVZqNBrxI4u5nw7
- dublado (final): Gr60F15ZauoKl852Qbmx (geração V7xX6iBIpMITb6wnpsMZ)

## ajustes da receita (11/11, tarde)
- veo roda com generate_audio false (2.424 créditos em 4s, 3.636 em 6s). aprovado na cena 2.
- disparar só o nó de dublagem: ele já puxa o veo. rodar os dois juntos gera o veo em dobro.
- a dublagem recomprime o áudio. na montagem: silenciar o som dos clipes e usar o áudio original de cada fala.
- envelope trocado por pilha de moedas douradas lisas; carrinho maior.
- falas 7, 8, 11 e 12 passam de 4s: clipes de 6s.
- cena 11 virou close na balança (mão colocando moedas), sem boca, sem dublagem.

## quadros (nós de imagem)
| quadro | nó | uso |
|---|---|---|
| close do theo | if1ibDkSqwXHwYXh4ojP | cenas 1, 5, 7, 9 e quadro final da 12 |
| plano médio com balança | aXDYUYOM4sC7xBHNvFkm | cenas 2, 4, 8, 10, 12 |
| close do carrinho | R5eSuazFxvE16DsDaVxR | cena 3 |
| esteira | TjioyY1LFBxFxVX5NXpJ | cena 6 |
| close da balança | 1yKXHr3w7SLmXKI0k71g | cena 11 |

## cenas (nó veo / nó final dublado)
| cena | veo | final | status |
|---|---|---|---|
| 1 | NBFCFkVZqNBrxI4u5nw7 | Gr60F15ZauoKl852Qbmx | aprovada |
| 2 | 4ue1slX47Hn7kTGKtZSi | jfROCCuF82szmakxVzn5 | aprovada |
| 3 | a criar (sem dublagem) | - | quadro gerando |
| 4 | csY4G8BWxGMRAVAoqTMl | ClhTZcXNv1qLS4uxfS56 | aprovada |
| 5 | f7Ll4JeypNjKTD1KDbTc | sZszc0PZ1AbWZiGTXKMe | aprovada |
| 6 | a criar (sem dublagem) | - | quadro gerando |
| 7 | M7AbdLo51b9dTvNYLEJ2 | IO4LFaYGYPSE6HeGpisl | gerando |
| 8 | kpN837OTRHh1lNhCGUxm | YIrReAXrGX6Jb2uO1Sqj | gerando |
| 9 | xOCLO78N5GU6aahuzpGz | 0emC2oeBdSzDZQA1O3SP | aprovada |
| 10 | thyB4NjTrP8XrZQgj1qX | u87jlZe2is21cMQ7mLYq | gerando |
| 11 | a criar (sem dublagem) | - | quadro gerando |
| 12 | V8wyvp9tWGAUmFwtqoHn (start médio, end close) | 5nbrNuga3ciArBu7jkob | gerando |
