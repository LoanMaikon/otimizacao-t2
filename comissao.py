import time

global melhor_tamanho, melhor_solucao, nos_explorados

melhor_tamanho = -1
melhor_solucao = []
nos_explorados = 0

def main():
    problema = ler_problema()
    
    inicio = time.time()
    branch_and_bound(problema, [])
    fim = time.time()

    if melhor_tamanho == -1:
        print("Inviavel")
    else:
        print("Melhor solucao: ", melhor_solucao)
        print("Melhor tamanho: ", melhor_tamanho)
        print("Nos explorados: ", nos_explorados)
        print("Tempo: ", fim - inicio)
    
class Candidato:
    def __init__(self, grupos, id):
        self.grupos = grupos
        self.id = id

class Problema:
    def __init__(self, num_grupos, num_candidatos, candidatos):
        self.num_grupos = num_grupos
        self.num_candidatos = num_candidatos
        self.candidatos = candidatos

def branch_and_bound(problema, E):
    global melhor_tamanho, melhor_solucao, nos_explorados

    nos_explorados += 1

    if Bdada(problema, E) >= melhor_tamanho and melhor_tamanho != -1:
        return

    if len(E) == problema.num_grupos:
        if melhor_tamanho == -1 or len(E) < melhor_tamanho:
            melhor_tamanho = len(E)
            melhor_solucao = [candidato.id for candidato in E]
        return

    for candidato in problema.candidatos:
        if candidato not in E:
            E.append(candidato)
            branch_and_bound(problema, E)
            E.pop()

def Bdada(problema, E):
    grupos_representados = set()
    for candidato in E:
        for grupo in candidato.grupos:
            grupos_representados.add(grupo)
    
    if len(grupos_representados) == problema.num_grupos:
        return len(E)
    else:
        return len(E) + 1

def ler_problema():
    num_grupos, num_candidatos = map(int, input().split())
    
    candidatos = []
    for i in range(num_candidatos):
        dados = input().split()
        c_num_grupos = int(dados[0])
        c_grupos = list(map(int, dados[1:]))

        candidatos.append(Candidato(c_grupos, i + 1))
    
    return Problema(num_grupos, num_candidatos, candidatos)

if __name__ == "__main__":
    main()