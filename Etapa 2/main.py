import random

import numpy as np

from functions import define_action, generate_board, print_agent_position

# Direções que o agente pode se mover

directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Parâmetros do tabuleiro

size = 3
num_pits = 2
num_wumpus = 1
num_treasure = 1

# Variáveis contadoras

total_movimentos = 0
total_mortes = 0
total_ouros = 0
total_wumpus = 0
total_vitorias = 0

num_jogos = 5  # Número de vezes que o jogo será executado


i = 0  # Contador para contabilizar o número de cada jogo

# Loop que executa os jogos

for _ in range(num_jogos):

    i += 1

    # Reinicializar o jogo

    board, agent_pos = generate_board(size, num_pits, num_wumpus, num_treasure)
    print("Game ", i)

    # Reinicializar o jogo

    matrix = board
    print(matrix)

    # Reiniciar as variáveis de estado
    has_treasure = False
    has_arrow = True

    # Loop principal do jogo
    while True:

        # Estratégia adotada para escolher a ação

        action_def = define_action(agent_pos, matrix)
        if type(action_def) == str:
            action_sort = action_def
        else:
            action_sort = random.choice(action_def)

        # Ação de atirar escolhida

        if action_sort == "atirar":
            if has_arrow:
                has_arrow = False
                print("O agente atirou")

                # Verificar se há um Wumpus em qualquer direção
                wumpus_hit = False

                row, col = agent_pos

                # Selecionar uma direção aleatória
                dx, dy = random.choice(directions)

                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < size and 0 <= new_col < size:
                    if matrix[new_row][new_col] == -2:
                        wumpus_hit = True
                        matrix[row][col] = 0  # Remove o agente da sala atual
                        matrix[new_row][new_col] = 0  # Remove o Wumpus da sala
                        total_wumpus += 1

                if wumpus_hit:
                    print("O agente matou o Wumpus!")
                else:
                    print("O agente atirou, mas não acertou o Wumpus.")
            else:
                print(matrix)
                print("O agente não possui flechas!")
                continue

        # Ação de atirar escolhida

        if action_sort == "mover":
            # Lógica para mover o agente
            row, col = agent_pos

            # Escolher uma direção aleatória
            dx, dy = random.choice(directions)

            new_row, new_col = row + dx, col + dy

            if 0 <= new_row < size and 0 <= new_col < size:
                if matrix[new_row][new_col] == -1 or matrix[new_row][new_col] == -2:
                    # Agente encontrou um buraco ou o Wumpus
                    print("O agente morreu!")
                    total_mortes += 1
                    break

                if matrix[new_row][new_col] == 1 and not has_treasure:
                    # Agente encontrou o tesouro
                    print("O agente pegou o tesouro!")
                    has_treasure = True
                    total_ouros += 1
                    matrix[new_row][new_col] = 0

                matrix[agent_pos[0]][agent_pos[1]] = 0
                agent_pos = (new_row, new_col)
                matrix[agent_pos[0]][agent_pos[1]] = 2

                print_agent_position(agent_pos)
                total_movimentos += 1

        # Verifica se o agente chegou à saída com o tesouro para vencer o jogo
        if has_treasure and agent_pos == (size - 1, 0):
            print("Parabéns! O agente venceu o jogo!")
            total_vitorias += 1

            break

print("Resultados do teste de validação:")
print("Total de jogos:", num_jogos)
print("Total de movimentos:", total_movimentos)
print("Total de mortes:", total_mortes)
print("Total de ouros pegos:", total_ouros)
print("Total de Wumpus mortos:", total_wumpus)
print("Total de vitórias:", total_vitorias)
