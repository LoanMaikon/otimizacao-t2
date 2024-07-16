import time
import argparse

global melhor_tamanho, melhor_solucao, nos_explorados

melhor_tamanho = -1
melhor_solucao = []
nos_explorados = 0

def main():
    global melhor_tamanho, melhor_solucao, nos_explorados

    args = get_args()

    problema = ler_problema()

    inicio = time.time()
    branch_and_bound(problema, [], args)
    fim = time.time()

    if melhor_tamanho == -1:
        print("Inviavel")
    else:
        print("Melhor solucao: ", melhor_solucao)
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
        self._ordenar_candidatos()
    
    def _ordenar_candidatos(self):
        self.candidatos.sort(key=lambda candidato: len(candidato.grupos), reverse=True)

def branch_and_bound(problema, E, args):
    global melhor_tamanho, melhor_solucao, nos_explorados
    nos_explorados += 1

    if len(E) > problema.num_candidatos:
            return

    if not args.f:
        if len(E) > 1:
            if E[-1] in E[:-1]:
                return
    
    if not args.o:
        if len(E) > 1:
            set_antes = set(x.id for x in E[:-1])
            set_depois = set_antes.copy()
            set_depois.add(E[-1].id)
            if len(set_antes) == len(set_depois):
                return

    if args.a:
        if Bdada(problema, E) >= melhor_tamanho and melhor_tamanho != -1:
            return
    else:
        if B(problema, E) >= melhor_tamanho and melhor_tamanho != -1:
            return

    if grupos_totalmente_representados(problema, E):
        if melhor_tamanho == -1 or len(E) < melhor_tamanho:
            melhor_tamanho = len(E)
            melhor_solucao = [candidato.id for candidato in E]
        return

    for candidato in problema.candidatos:
        E.append(candidato)
        branch_and_bound(problema, E, args)
        E.remove(candidato)

def B(problema, E):
    pass

def Bdada(problema, E):
    grupos_representados = set()
    for candidato in E:
        for grupo in candidato.grupos:
            grupos_representados.add(grupo)
    
    if len(grupos_representados) == problema.num_grupos:
        return len(E)
    else:
        return len(E) + 1
    
def grupos_totalmente_representados(problema, E):
    grupos_representados = set()
    for candidato in E:
        for grupo in candidato.grupos:
            grupos_representados.add(grupo)
    
    return len(grupos_representados) == problema.num_grupos

def ler_problema():
    num_grupos, num_candidatos = map(int, input().split())
    
    candidatos = []
    for i in range(num_candidatos):
        dados = input().split()
        c_grupos = list(map(int, dados[1:]))

        candidatos.append(Candidato(c_grupos, i + 1))
    
    return Problema(num_grupos, num_candidatos, candidatos)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--f", required=False, action="store_true")
    parser.add_argument("-o", "--o", required=False, action="store_true")
    parser.add_argument("-a", "--a", required=False, action="store_true")

    return parser.parse_args()

if __name__ == "__main__":
    main()