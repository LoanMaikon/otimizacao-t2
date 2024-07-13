import time

def main():
    problema = ler_problema()
    
    melhor_tamanho = -1
    melhor_solucao = []
    nos_explorados = 0

    inicio = time.time()
    branch_and_bound()
    fim = time.time()

    if melhor_tamanho == -1:
        print("Inviavel")
    else:
        print("Solucao: ", melhor_solucao)
        print("Tamanho: ", melhor_tamanho)
        print("Nos explorados: ", nos_explorados)
        print("Tempo: ", fim - inicio)
    
class Candidato:
    def __init__(self, grupos):
        self.grupos = grupos

class Problema:
    def __init__(self, num_grupos, num_candidatos, candidatos):
        self.num_grupos = num_grupos
        self.num_candidatos = num_candidatos
        self.candidatos = candidatos

def branch_and_bound():
    pass

def ler_problema():
    num_grupos = int(input())
    num_candidatos = int(input())
    
    candidatos = []
    for i in range(num_candidatos):
        c_num_grupos = int(input())
        c_grupos = []
        for j in range(c_num_grupos):
            c_grupos.append(int(input()))

        candidatos.append(Candidato(c_grupos))
    
    return Problema(num_grupos, num_candidatos, candidatos)

if __name__ == "__main__":
    main()