import random
import typing as tp

import numpy as np

from functions import (Memory, choose_action, generate_board, get_perceptions,
                       guardar_passos, print_agent_position)

# Direções que o agente pode se mover

directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Criação da instância memory

memory = Memory()

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

num_jogos = 3000  # Número de vezes que o jogo será executado

exit_pos = (size - 1, 0)

i = 0  # Contador para contabilizar o número de cada jogo

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

    visited_rooms = []  # Lista de salas já visitadas

    passos_agente: tp.List[tp.Tuple[int, int]] = []

    # Loop principal do jogo
    while True:

        guardar_passos(passos_agente, agent_pos)

        # Estratégia adotada para escolher a ação

        # Atualizar as percepções na memória
        memory.update_perceptions(
            agent_pos, get_perceptions(agent_pos, matrix))

        # Utilizar a memória para decidir a ação
        action = choose_action(agent_pos, memory)

        action_sort = action

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

        # Ação de mover escolhida

        if action_sort == "mover":
            # Lógica para mover o agente
            row, col = agent_pos

            unvisited_moves = []

            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < size and 0 <= new_col < size:
                    if matrix[new_row][new_col] == 0 and (new_row, new_col) not in visited_rooms:
                        unvisited_moves.append((dx, dy))

            if unvisited_moves:
                dx, dy = random.choice(unvisited_moves)
            else:
                dx, dy = random.choice(directions)

            new_row, new_col = row + dx, col + dy

            if 0 <= new_row < size and 0 <= new_col < size:
                if matrix[new_row][new_col] == -1 or matrix[new_row][new_col] == -2:
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

                # Adiciona a sala atual à lista de salas visitadas
                visited_rooms.append(agent_pos)

                print_agent_position(agent_pos)
                total_movimentos += 1

                if has_treasure == True and agent_pos != exit_pos:
                    # Agente tem o tesouro e ainda não chegou à posição de saída
                    # Movimento em direção à posição de saída
                    # dx = 1 if exit_pos[0] > row else -1
                    # dy = 1 if exit_pos[1] > col else -1
                    for i in range(len(passos_agente) - 1, -1, -1):
                        row, col = passos_agente[i]
                        # Limpa a posição atual
                        matrix[agent_pos[0]][agent_pos[1]] = 0
                        agent_pos = (row, col)
                        # Define a nova posição do agente
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
