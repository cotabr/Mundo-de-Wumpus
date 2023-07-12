# %% Bibliotecas
import random

import numpy as np

# %% Parâmetros do tabuleiro
size = 3
num_pits = 2
num_wumpus = 1
num_treasure = 1



# %% Criando o tabuleiro

# Cria a matriz preenchida com zeros
matrix = np.array([[0 for _ in range(size)] for _ in range(size)])

agent_pos = (size-1, 0)
matrix[agent_pos[0]][agent_pos[1]] = 2

# Define a posição aleatória dos buracos
for _ in range(num_pits):
    row, col = random.randrange(size), random.randrange(size)
    if matrix[row][col] not in [-2, 2, 1]:
        matrix[row][col] = -1  # -1 representa um buraco

# Define a posição aleatória do Wumpus
while True:
    row, col = random.randrange(size), random.randrange(size)
    if matrix[row][col] not in [-1, 2, 1]:
        matrix[row][col] = -2  # -2 representa o Wumpus
        break

# Define a posição aleatória do tesouro
while True:
    row, col = random.randrange(size), random.randrange(size)
    if matrix[row][col] not in [-1, -2, 2]:
        matrix[row][col] = 1  # 1 representa o tesouro
        break

# %% Criando a função das percepções do agente


def get_perceptions(agent_pos, matrix):
    perceptions = []
    row, col = agent_pos
    size = matrix.shape[0]
    # esquerda, direita, acima, abaixo
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for dx, dy in directions:
        new_row, new_col = row + dx, col + dy

        if 0 <= new_row < size and 0 <= new_col < size:
            if matrix[new_row][new_col] == -1:  # Verifica se há um buraco
                perceptions.append("brisa")
            elif matrix[new_row][new_col] == -2:  # Verifica se há o Wumpus
                perceptions.append("fedor")
            elif matrix[new_row][new_col] == 1:  # Verifica se há o tesouro
                perceptions.append("brilho")
            elif matrix[new_row][new_col] == 0:  # Verifica se está vazio
                perceptions.append("vazio")
        else:
            # Adiciona a percepção de parede quando fora dos limites do tabuleiro
            perceptions.append("parede")

    # if matrix[row][col] in [-1, -2]:  # Verifica se há buraco ou Wumpus na posição atual
    #     perceptions.append("impacto")
    # elif matrix[row][col] == 1:  # Verifica se há ouro na posição atual
    #     perceptions.append("tesouro")

    return perceptions

# %% Criando a função de movimentação do agente


def move_agent(agent_pos, matrix, new_row, new_col):
    size = matrix.shape[0]
    if not (0 <= new_row < size and 0 <= new_col < size):
        return "parede", agent_pos, matrix
    if matrix[agent_pos[0]][agent_pos[1]] == -1:  # Verifica se há um buraco
        return "morte", agent_pos, matrix
    elif matrix[agent_pos[0]][agent_pos[1]] == -2:  # Verifica se há o Wumpus
        return "morte", agent_pos, matrix
    elif matrix[agent_pos[0]][agent_pos[1]] == 1:  # Verifica se há o tesouro
        return "ganhou", agent_pos, matrix
    else:
        # Remove o agente da posição atual
        matrix[agent_pos[0]][agent_pos[1]] = 0
        matrix[new_row][new_col] = 2  # Coloca o agente na nova posição
        agent_pos = (new_row, new_col)  # Atualiza a posição do agente
        return "movimento", agent_pos, matrix

# %% Criando a função de atirar


def shoot_arrow(agent_pos, matrix, direction):
    row, col = agent_pos
    size = matrix.shape[0]
    dx, dy = direction
    new_row, new_col = row + dx, col + dy

    if 0 <= new_row < size and 0 <= new_col < size:
        if matrix[new_row][new_col] == -2:  # Verifica se há o Wumpus na posição adjacente
            matrix[new_row][new_col] = 0  # Remove o Wumpus do tabuleiro
            return "grito", agent_pos, matrix
    return "sem_alvo", agent_pos, matrix

# %% Criando a função de pegar (Não implementado)


def grab_treasure(agent_pos, matrix):
    row, col = agent_pos
    if matrix[row][col] == 1:  # Verifica se há ouro na posição atual
        matrix[row][col] = 0  # Remove o tesouro do tabuleiro
        print("Agente pegou o tesouro!")
    else:
        print("Não há ouro na posição atual!")
    return agent_pos, matrix

# %% Criando a função que define a ação


def perform_action(action, agent_pos, matrix):
    result = ""
    if action == "mover":
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        dx, dy = random.choice(directions)
        new_row, new_col = agent_pos[0] + dx, agent_pos[1] + dy
        result, agent_pos, matrix = move_agent(
            agent_pos, matrix, new_row, new_col)
        if result == "morte":
            print(matrix)
            print("Agente morreu!")
        elif result == "movimento":
            print("Agente se moveu para a posição:", agent_pos)
            print(matrix)
        elif result == "ganhou":
            print("O agente encontrou o ouro!")
            print(matrix)
        # else:
        #     print("O agente bateu na parede!")

    elif action == "atirar":
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        direction = random.choice(directions)
        result, agent_pos, matrix = shoot_arrow(agent_pos, matrix, direction)
        if result == "grito":
            print("Agente atirou e matou o Wumpus!")
        else:
            print("Agente atirou, mas não acertou o alvo.")

    # elif action == "pegar":
    #     agent_pos, matrix = grab_treasure(agent_pos, matrix)

    return agent_pos, matrix, result

# %% Outros


# Percepções do agente

new_matrix = np.copy(matrix)
perceptions = get_perceptions(agent_pos, matrix)
ação = ""
posicoes = []
# %% Loop principal

print("\nCampo Inicial")
print("----------------- ")
print(new_matrix)
print("----------------- ")
print("Percepções Iniciais do Agente: " + str(perceptions))
print("----------------- ")
print("Início do Jogo:")
actions = ["mover", "atirar"]

while True:

    if "brilho" in perceptions:
        if "fedor" in perceptions and "buraco" in perceptions:
            actions = ["mover", "atirar"]
            acao = perform_action(random.choice(actions), agent_pos, new_matrix)
            if acao[2] != "movimento":
                print("Tabuleiro Final:")
                print(new_matrix)
                break
            else:
                posicoes.append(acao[0])
        elif "buraco" in perceptions:
            actions = ["mover"]
            perform_action(random.choice(actions), agent_pos, new_matrix)
            if perform_action(random.choice(actions), agent_pos, new_matrix)[2] != "movimento":
                print("Tabuleiro Final:")
                print(new_matrix)
                break
            else:
                posicoes.append(perform_action(
                    random.choice(actions), agent_pos, new_matrix)[0])
        elif "fedor" in perceptions:
            actions = ["mover", "atirar"]
            perform_action(random.choice(actions), agent_pos, new_matrix)
            if perform_action(random.choice(actions), agent_pos, new_matrix)[2] != "movimento":
                print("Tabuleiro Final:")
                print(new_matrix)
                break
            else:
                posicoes.append(perform_action(
                    random.choice(actions), agent_pos, new_matrix)[0])
        else:
            perform_action("mover", agent_pos, new_matrix)
            if perform_action(random.choice(actions), agent_pos, new_matrix)[2] != "movimento":
                print("Tabuleiro Final:")
                print(new_matrix)
                print("\n")
                print("A posição final do agente foi: ", perform_action(
                    random.choice(actions), agent_pos, new_matrix)[1])
                break
            else:
                posicoes.append(perform_action(
                    "mover", agent_pos, new_matrix)[0])
    elif "fedor" in perceptions:
        if "buraco" in perceptions:
            actions = ["mover", "atirar"]
            perform_action(random.choice(actions), agent_pos, new_matrix)
            if perform_action(random.choice(actions), agent_pos, new_matrix)[2] != "movimento":
                print("Tabuleiro Final:")
                print(new_matrix)
                break
            else:
                posicoes.append(perform_action(
                    random.choice(actions), agent_pos, new_matrix)[0])
        else:
            perform_action("atirar", agent_pos, new_matrix)
            if perform_action("atirar", agent_pos, new_matrix)[2] != "movimento":
                print("Tabuleiro Final:")
                print(new_matrix)
                break
            else:
                posicoes.append(perform_action(
                    "atirar", agent_pos, new_matrix)[0])
    elif "brisa" in perceptions:
        if "fedor" in perceptions:
            actions = ["mover", "atirar"]
            perform_action(random.choice(actions), agent_pos, new_matrix)
            if perform_action(random.choice(actions), agent_pos, new_matrix)[2] != "movimento":
                print("Tabuleiro Final:")
                print(new_matrix)
                break
            else:
                posicoes.append(perform_action(
                    random.choice(actions), agent_pos, new_matrix)[0])
        else:
            perform_action("mover", agent_pos, new_matrix)
            if perform_action("mover", agent_pos, new_matrix)[2] != "movimento":
                print("Tabuleiro Final:")
                print(new_matrix)
                break
            else:
                posicoes.append(perform_action(
                    "mover", agent_pos, new_matrix)[0])
    else:
        perform_action("mover", agent_pos, new_matrix)
        if perform_action("mover", agent_pos, new_matrix)[2] != "movimento":
            print("Tabuleiro Final:")
            print(new_matrix)
            print("A posição final do agente foi: ",
                  perform_action("mover", agent_pos, new_matrix)[0])
            break
        else:
            posicoes.append(perform_action("mover", agent_pos, new_matrix)[0])
    print(posicoes)

# %% Outros
# print(matrix)
# print(get_perceptions(agent_pos, matrix))
# directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# dx, dy = random.choice(directions)
# new_row, new_col = agent_pos[0] + dx, agent_pos[1] + dy
# print(move_agent(agent_pos, matrix, new_row, new_col)[0])
# print(move_agent(agent_pos, matrix, new_row, new_col)[1])
# print(matrix)

# # matrix[agent_pos[0]][agent_pos[1]] = 2  # 2 representa o agente
# perceptions = get_perceptions(agent_pos, matrix)
# # print(matrix)
# # print(perceptions)

# # Movimentação

# actions = ["mover", "atirar", "pegar"]

# Seleciona uma ação aleatoriamente


# print(matrix)

# print(agent_pos)

# perform_action("mover", agent_pos, matrix)
