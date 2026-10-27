# pingpong_py

Jogo de Ping Pong em Python com Tkinter, feito com programação orientada a objetos. Controle a raquete, rebata a bolinha e faça a maior pontuação antes de perder as vidas.

## Como jogar

- Mover para a esquerda: `←` ou `A`
- Mover para a direita: `→` ou `D`

Regras:

- Você começa com 2 vidas.
- Cada rebatida na raquete vale 1 ponto.
- Se a bolinha rebatida chegar ao topo da tela, você ganha 1 ponto e uma nova bolinha é lançada.
- Se a bolinha cair no fundo, você perde 1 vida.
- A bolinha fica mais rápida conforme a pontuação aumenta.
- Quando as vidas acabam, clique em "Jogar novamente" para recomeçar.

## Como executar

Requisitos: Python 3.8 ou superior com Tkinter (já incluso no Windows e no macOS).

No Linux, se necessário:

```bash
sudo apt install python3-tk
```

Executando o jogo:

```bash
git clone https://github.com/Lookeon/pingpong_py.git
cd pingpong_py
python pingpong_oop.py
```

## Estrutura

O código está em `pingpong_oop.py`, com três classes:

- `Paddle`: raquete e seu movimento
- `Ball`: bolinha, com velocidade e ângulo aleatórios
- `PingPongGame`: loop do jogo, colisões, pontuação, vidas e teclado

## Configuração

As constantes no topo do arquivo permitem ajustar o jogo:

| Constante       | Padrão | Descrição                      |
|-----------------|--------|--------------------------------|
| `GAME_WIDTH`    | 600    | Largura da área de jogo        |
| `GAME_HEIGHT`   | 400    | Altura da área de jogo         |
| `PADDLE_WIDTH`  | 110    | Largura da raquete             |
| `PADDLE_HEIGHT` | 14     | Altura da raquete              |
| `BALL_SIZE`     | 18     | Tamanho da bolinha             |
| `PLAYER_SPEED`  | 7      | Velocidade da raquete          |
| `FRAME_DELAY`   | 16     | Intervalo entre quadros (ms)   |



<img width="675" height="552" alt="image" src="https://github.com/user-attachments/assets/a817d9c9-294f-4cb9-90b1-238bb71d8c99" />

