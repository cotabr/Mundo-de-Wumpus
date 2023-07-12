import random

import numpy as np

has_treasure = False  # Variável para controlar se o agente pegou o tesouro

has_arrow = True  # Variável para controlar se o agente tem uma flecha


def generate_board(size, num_pits, num_wumpus, num_treasure):
    # Cria a matriz preenchida com zeros
    nmatrix = np.zeros((size, size))

    # Define a posição inicial do agente
    agent_pos = (size - 1, 0)
    nmatrix[agent_pos] = 2  # 2 representa o agente

    # Define a posição aleatória dos buracos
    for _ in range(num_pits):
        while True:
            row, col = random.randrange(size), random.randrange(size)
            if nmatrix[row][col] == 0 and (row, col) != agent_pos:
                nmatrix[row][col] = -1  # -1 representa um buraco
                break

    # Define a posição aleatória do Wumpus
    for _ in range(num_wumpus):
        while True:
            row, col = random.randrange(size), random.randrange(size)
            if nmatrix[row][col] == 0 and (row, col) != agent_pos:
                nmatrix[row][col] = -2  # -2 representa o Wumpus
                break

    # Define a posição aleatória do tesouro
    for _ in range(num_treasure):
        while True:
            row, col = random.randrange(size), random.randrange(size)
            if nmatrix[row][col] == 0 and (row, col) != agent_pos:
                nmatrix[row][col] = 1  # 1 representa o tesouro
                break

    return nmatrix, agent_pos


def get_perceptions(agent_pos, matrix):
    perceptions = []
    row, col = agent_pos
    size = matrix.shape[0]
    # esquerda, direita, acima, abaixo
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for dx, dy in directions:
        new_row, new_col = row + dx, col + dy

        if 0 <= new_row < size and 0 <= new_col < size:
            if matrix[new_row][new_col] == -1:
                perceptions.append("brisa")
            elif matrix[new_row][new_col] == -2:
                perceptions.append("fedor")

    if matrix[row][col] == 1:
        if not has_treasure:  # Verifica se o agente ainda não pegou o tesouro
            perceptions.append("brilho")

    return perceptions


def define_action(agent_pos, matrix):
    perceptions = get_perceptions(agent_pos, matrix)
    if {"fedor", "brisa", "brilho"} <= set(perceptions):
        return "mover", "pegar", "atirar"
    elif {"fedor", "brisa"} <= set(perceptions):
        return "mover", "atirar"
    elif {"fedor", "brilho"} <= set(perceptions):
        return "mover", "pegar"
    elif set(perceptions) == {"fedor"}:
        return "atirar", "mover"
    elif set(perceptions) == {"brisa"}:
        return "mover"
    elif set(perceptions) == {"brilho"}:
        return "pegar"
    else:
        return "mover"


def print_agent_position(agent_pos):
    row, col = agent_pos
    print(f"Nova posição do agente: ({row}, {col})")
