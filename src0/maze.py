import sys

#Criando a classe node, aonde o metodo init automaticamente inicia a classe atribuindo a ela 3 caracteristicas ou variaveis. 
#A classe node é uma estrutura de dados que que serve para acompanhar as ações tomadas pelo agente
class Node():
    def __init__(self, state, parent, action):
        self.state = state #A variavel estado se refere ao estado atual do Node
        self.parent = parent #A variavel parent se refere ao Node pai, ou anterior aquele Node.
        self.action = action #A variavel action se refere a ação queo nó está tomando.

#Criação da fronteira gerenciada por stack DFS, a fronteira é o conjunto de proximos passos que são possíveis analisar a partir do passo atual ao qual não foram analisados ainda
#Depth-First Search é a frontier gerenciada em forma de stack, o primiero nó a ser removido e considerado é o ultimo a ser adicionado, ou LIFO (Last in first out) Ou Ultimo que entra é o primeiro que sai
class StackFrontier():
    def __init__(self):
        self.frontier = [] #Ao criar uma fronteira cria-se o seu atributo, uma lista vazia 

    def add(self, node): #Criado método para adicionar novos Nodes
        self.frontier.append(node)  #Adiciona um Node a lista, Visto que se trata de stack, os Nodes novos são sempre adicionados ao topo da stack, por isso append

    def contains_state(self, state): #Cria método para verificar se um um bloco está na fila, o bloco é localizado pelo seu estado
        return any(node.state == state for node in self.frontier) #se qualquer um dos nós possuir o estado, ele retornará true, visto a comparação e o for que busca os estados dos nodes na frontier inteira, se não encontrar em nenhum retorna false

    def empty(self): #metodo para verficar se a pilha está vazia
        return len(self.frontier) == 0 #ele faz isso ao verificar se o lenght da lista frontier é igual a 0(se o comprimento da lista é 0)

    def remove(self): #metodo para remover o node da pilha
        if self.empty(): #verifica se a pilha já não está vazia
            raise Exception("empty frontier") #avisa que a pilha já esta vazia, se tiver.
        else: 
            node = self.frontier[-1] #senão atribui o ultimo elemento da fronteira para o valor node
            self.frontier = self.frontier[:-1] #remove o ultimo elemento da fronteira(ou remove do topo)
            return node #retorna o ultimo node, gerenciando assim a fronteira de forma Depth-First Search (stack ou LIFO)


class QueueFrontier(StackFrontier): #a classe QueueFrontier herdou a classe anteriormente descrita, ou seja, possui todos os metodos e caracteristicas de funcionamento da classe anterior. Contudo foi alterado apenas o método remove abaixo:

    def remove(self): #redefinição do metodo para remover os nodes.
        if self.empty(): #primeiro verifica se a fronteria já não está vazia
            raise Exception("empty frontier") #se estiver vazia aponta a questão
        else: 
            node = self.frontier[0] #se não ela pega o primeiro node da lista de nodes fronteira e atribui ele a variavel node
            self.frontier = self.frontier[1:] #Elimina o primeiro node de dentro da lista fronteira
            return node #retorna o primeiro node, gerenciando assim a fronteira de forma Breadth-First Search (queue ou FIFO)

class Maze():

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)
