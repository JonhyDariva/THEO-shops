# 001 — por que tudo fica mais caro e seu salário não?

- idioma: português (br)
- duração alvo: 36s, fala rápida (~3 palavras por segundo, 110 palavras)
- formato: 9:16, 12 cenas de 2 a 4s
- cenário: laboratório do theo. no centro da bancada, uma balança de dois pratos:
  de um lado um envelope escrito "salário", do outro um carrinho de mercado em miniatura.
- status: roteiro escrito, aguardando aprovação. nada gerado ainda.

## cenas

| # | fala | emoção | enquadramento | ação |
|---|------|--------|---------------|------|
| 1 | seu salário subiu. e mesmo assim você tá mais pobre. | desconfiado | close | encara a câmera, levanta uma sobrancelha, aponta pro espectador |
| 2 | não é impressão sua. é matemática. | animado | plano médio | abre os braços mostrando a balança na bancada |
| 3 | o preço do mercado muda toda semana. | chocado | close no carrinho, theo ao fundo | o carrinho enche sozinho e o prato dele desce |
| 4 | o seu salário? muda uma vez por ano. | neutro, irônico | plano médio | segura o envelope parado no outro prato, olha pro relógio |
| 5 | e quando muda, só repõe a inflação que já passou. | bravo | close | balança a cabeça, dedo em riste |
| 6 | ou seja: você passa o ano inteiro correndo atrás. | chocado | plano aberto | corre numa esteira de laboratório atrás do carrinho, sem alcançar |
| 7 | e comida e aluguel muitas vezes sobem mais que a média. | desconfiado | close | segura um pão numa mão e uma chave na outra, pesando os dois |
| 8 | o índice oficial diz uma coisa. o seu carrinho diz outra. | bravo | plano médio | aponta pra um gráfico calmo na lousa, depois pro carrinho transbordando |
| 9 | aumento que só empata com a inflação não é aumento. | neutro, sério | close | fala devagar pra câmera, mão espalmada |
| 10 | é só você voltando pro lugar onde já tava. | desconfiado | plano médio | a balança volta a ficar nivelada, ele dá de ombros |
| 11 | quer ganhar da inflação? seu salário precisa subir mais que ela. | animado | close | sorri, coloca um segundo envelope no prato e o salário finalmente pesa mais |
| 12 | senão, todo ano é a mesma história. e é por isso que... | desconfiado | plano médio fechando pra close | dá de ombros, depois se inclina pra câmera e termina na mesma pose e expressão do início da cena 1 |

## loop
- a última fala fica em aberto ("e é por isso que...") e emenda na primeira
  ("seu salário subiu. e mesmo assim você tá mais pobre."). o vídeo recomeça sem o espectador perceber o corte.
- imagem: o último quadro da cena 12 tem que ser igual ao primeiro quadro da cena 1
  (mesmo close, mesma pose, sobrancelha levantada). gerar a cena 12 usando o primeiro quadro da cena 1 como quadro final.
- áudio: sem silêncio no fim da cena 12 nem no começo da cena 1. música em loop, sem final marcado.
- sem "segue aqui" falado, porque quebra o loop. o chamado pra seguir entra como texto na tela nas cenas 11 e 12.

## notas de produção

- corte seco entre cenas, alternando close e plano médio como no vídeo modelo.
- legenda: 2 palavras por vez, minúscula, branca com sombra, centro da tela.
- toda cena usa personagem/theo-ficha.png como referência.
- texto na tela só na edição (o "salário" do envelope pode sair torto no vídeo de ia;
  se sair, cobrir com legenda ou regerar a cena).
- teste de lip sync antes de gerar tudo: cenas 1 e 2, pelos dois caminhos
  (fala nativa do modelo de vídeo x lip sync dedicado em cima do áudio do elevenlabs).

## checagem de conteúdo

- reajuste salarial costuma ser anual e baseado na inflação passada: ok como regra geral no brasil.
- "comida e aluguel muitas vezes sobem mais que a média": dito como "muitas vezes", não como regra fixa.
- sem números específicos no roteiro, pra não envelhecer nem precisar de fonte por vídeo.
