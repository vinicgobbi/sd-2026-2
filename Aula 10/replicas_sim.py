#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aula 10 - Replicacao, consistencia e o teorema CAP.

Simula DUAS replicas (A e B) do mesmo dado e uma PARTICAO de rede entre elas.
Sem dependencias externas. Roda no Windows/venv:  python replicas_sim.py

O que a simulacao mostra:
  (1) rede OK  -> a escrita em A e replicada para B  => consistencia eventual;
  (2) PARTICAO -> B deixa de receber as escritas       => DIVERGENCIA
                  (o programa registra o MOMENTO exato da divergencia);
  (3) sob particao, a escolha do CAP ao ler de B:
        - modo AP: responde o valor ANTIGO (mantem a disponibilidade, abre mao de C);
        - modo CP: RECUSA a leitura com 503 (mantem a consistencia, abre mao de A);
  (4) cura da particao -> B reconcilia e alcanca A      => consistencia eventual.

Ampliacoes do lab (Missoes 2 e 3):
  (2b) mais escritas sob particao + leitura de A x B lado a lado e quantas
       versoes A ficou a frente de B;
  (5)  ler(dado): a regra de negocio escolhe AP ou CP pelo TIPO do dado
       (saldo/estoque -> CP; curtidas/catalogo -> AP) sob a mesma particao.
"""


class Replica:
    """Uma copia do dado, com um numero de versao."""
    def __init__(self, nome):
        self.nome = nome
        self.valor = None
        self.versao = 0

    def aplicar(self, valor, versao):
        self.valor = valor
        self.versao = versao


class Cluster:
    def __init__(self):
        self.A = Replica("A")           # replica que recebe as escritas (lider)
        self.B = Replica("B")           # replica do outro lado da rede (leituras)
        self.particionado = False
        self.versao_global = 0          # versao da ultima escrita aceita
        self.divergiu_em = None         # momento (versao) em que B ficou para tras

    # ----- escrita (sempre em A) -----
    def escrever(self, valor):
        self.versao_global += 1
        v = self.versao_global
        self.A.aplicar(valor, v)
        print(f'    A <- "{valor}" (v{v})')
        if not self.particionado:
            self.B.aplicar(valor, v)                     # replicacao
            print(f'    B <- "{valor}" (v{v})   [replicado]')
        else:
            print(f'    B  x  NAO recebe (particao) - continua em v{self.B.versao}')
            if self.divergiu_em is None:
                self.divergiu_em = v
                print(f'    >>> MOMENTO DA DIVERGENCIA: A=v{v}  B=v{self.B.versao} <<<')

    # ----- leitura (na replica A: sempre a mais recente) -----
    def ler_de_A(self):
        return f'"{self.A.valor}" (v{self.A.versao})'

    # ----- leitura (na replica B) -----
    def ler_de_B(self, modo="AP"):
        desatualizada = self.B.versao < self.versao_global
        if self.particionado and desatualizada:
            if modo == "CP":
                return "503 INDISPONIVEL (CP: prioriza Consistencia)"
            return (f'"{self.B.valor}" (v{self.B.versao}) '
                    f'DESATUALIZADO (AP: prioriza Disponibilidade)')
        return f'"{self.B.valor}" (v{self.B.versao})'

    # ----- rede -----
    def particionar(self):
        self.particionado = True
        print("    ## rede PARTICIONADA: A e B nao se falam ##")

    def curar(self):
        self.particionado = False
        self.B.aplicar(self.A.valor, self.A.versao)      # reconciliacao: B copia A
        self.divergiu_em = None
        print(f'    ## rede CURADA: B reconcilia -> "{self.B.valor}" (v{self.B.versao}) ##')


def titulo(t):
    print("\n" + t)
    print("-" * len(t))


# ----- regra de negocio: o tipo do dado escolhe o lado do CAP -----
MODO_POR_DADO = {
    "saldo": "CP",       # mostrar saldo errado e pior que recusar
    "estoque": "CP",     # vender o que nao existe gera prejuizo
    "curtidas": "AP",    # um numero um pouco velho nao faz mal
    "catalogo": "AP",    # melhor mostrar o catalogo de ontem que nada
}


def ler(clusters, dado):
    """Le o dado na replica B, no modo (AP/CP) definido pelo tipo do dado."""
    modo = MODO_POR_DADO[dado]
    return f"{dado:9} [{modo}] -> {clusters[dado].ler_de_B(modo=modo)}"


if __name__ == "__main__":
    c = Cluster()

    titulo("Cenario 1 - rede OK: replicacao e consistencia eventual")
    c.escrever("preco=10")
    print(f"    leitura em B: {c.ler_de_B()}")
    print("    => A e B concordam (consistencia alcancada).")

    titulo("Cenario 2 - PARTICAO: a divergencia")
    c.particionar()
    c.escrever("preco=20")                                # so A recebe
    divergiu_em = c.divergiu_em
    c.escrever("preco=30")                                # escrita extra sob particao
    print(f"    leitura em A: {c.ler_de_A():22}| leitura em B: {c.ler_de_B()}")
    atraso = c.A.versao - c.B.versao
    print(f"    => A=v{c.A.versao} ('{c.A.valor}')  !=  B=v{c.B.versao} ('{c.B.valor}')  -> DIVERGEM.")
    print(f"    => A esta {atraso} versoes a frente de B: um cliente em cada replica ve um preco diferente.")

    titulo("Cenario 3 - sob particao, a escolha do CAP")
    print(f"    modo AP (disponivel):   {c.ler_de_B(modo='AP')}")
    print(f"    modo CP (consistente):  {c.ler_de_B(modo='CP')}")
    print("    => nenhuma opcao da C e A ao mesmo tempo DURANTE a particao (P e inevitavel).")

    titulo("Cenario 4 - cura da particao: consistencia eventual")
    c.curar()
    print(f"    leitura em B: {c.ler_de_B()}")
    print("    => passada a particao, as replicas voltam a concordar.")

    titulo("Cenario 5 - regra de negocio: o tipo do dado escolhe AP ou CP")
    clusters = {dado: Cluster() for dado in MODO_POR_DADO}
    iniciais = {"saldo": "R$ 100", "estoque": "5 un", "curtidas": "42", "catalogo": "v1"}
    novos = {"saldo": "R$ 40", "estoque": "4 un", "curtidas": "43", "catalogo": "v2"}
    for dado, cl in clusters.items():
        print(f"  {dado}:")
        cl.escrever(iniciais[dado])
        cl.particionar()
        cl.escrever(novos[dado])                          # a mesma particao em todos
    print()
    for dado in MODO_POR_DADO:
        print(f"    {ler(clusters, dado)}")
    print("    => sob a MESMA particao: saldo/estoque recusam (CP), curtidas/catalogo respondem (AP).")

    print(f"\nResumo: a divergencia comecou na versao v{divergiu_em}; "
          "sob particao escolhe-se C ou A, nunca os dois.")
