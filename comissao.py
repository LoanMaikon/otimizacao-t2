from argparse import ArgumentParser
from time import time


def main():
    global melhor_tamanho, melhor_solucao, nos_explorados
    melhor_tamanho = -1
    melhor_solucao = []
    nos_explorados = 0

    args = get_args()
    problema = ler_problema()

    inicio = time()
    branch_and_bound(problema, [], args)
    fim = time()

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

def branch_and_bound(problema: Problema, escolhidos: list, args):
    global melhor_tamanho, melhor_solucao, nos_explorados
    nos_explorados += 1

    if len(escolhidos) > problema.num_candidatos:
        return

    if not args.disable_viability_cuts:
        if (len(escolhidos) > 1) and (escolhidos[-1] in escolhidos[:-1]):
            return
    
    if not args.disable_optimality_cuts:
        if len(escolhidos) > 1:
            set_antes = {grupo for candidato in escolhidos[:-1] for grupo in candidato.grupos}

            set_depois = set_antes.copy()
            for grupo in escolhidos[-1].grupos:
                set_depois.add(grupo)

            if len(set_antes) == len(set_depois):
                return

    if args.use_default_function:
        if (B(problema, escolhidos) >= melhor_tamanho) and (melhor_tamanho != -1):
            return
    else:
        if (Bdada(problema, escolhidos) >= melhor_tamanho) and (melhor_tamanho != -1):
            return

    if solucao_viavel(problema, escolhidos):
        if (len(escolhidos) < melhor_tamanho) or (melhor_tamanho == -1):
            melhor_tamanho = len(escolhidos)
            melhor_solucao = [candidato.id for candidato in escolhidos]
        return

    for candidato in problema.candidatos:
        escolhidos.append(candidato)
        branch_and_bound(problema, escolhidos, args)
        escolhidos.pop()

def B(problema, E):
    grupos_representados = get_grupos_representados(problema, E)

    if len(grupos_representados) == problema.num_grupos:
        return len(E)
    
    grupos_faltantes = set([i for i in range(1, problema.num_grupos + 1)]) - grupos_representados

    F = set(problema.candidatos) - set(E)
    len_p_1 = False
    for candidato in F:
        if len(set(candidato.grupos) & grupos_faltantes) == len(grupos_faltantes):
            len_p_1 = True

    if len_p_1:
        return len(E) + 1
    return len(E) + 2
    
def Bdada(problema, E):
    if solucao_viavel(problema, E):
        return len(E)
    return len(E) + 1

def solucao_viavel(problema, escolhidos):
    grupos_representados = get_grupos_representados(problema, escolhidos)
    return len(grupos_representados) == problema.num_grupos
    
def get_grupos_representados(problema, E):
    grupos_representados = set()
    for candidato in E:
        for grupo in candidato.grupos:
            grupos_representados.add(grupo)
    
    return grupos_representados

def ler_problema():
    num_grupos, num_candidatos = map(int, input().split())
    
    candidatos = []
    for i in range(num_candidatos):
        dados = input().split()
        c_grupos = list(map(int, dados[1:]))

        candidatos.append(Candidato(c_grupos, i + 1))
    
    return Problema(num_grupos, num_candidatos, candidatos)

def get_args():
    parser = ArgumentParser()
    parser.add_argument("-f", "--f", action="store_true",
                        dest="disable_viability_cuts",
                        help="Desativa os cortes de viabilidade")
    parser.add_argument("-o", "--o", action="store_true",
                        dest="disable_optimality_cuts",
                        help="Desativa os cortes de otimalidade")
    parser.add_argument("-a", "--a", action="store_false",
                        dest="use_default_function",
                        help="Usa a funcao limitante do professor")

    return parser.parse_args()

if __name__ == "__main__":
    main()