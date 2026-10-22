#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aula 11 - Consenso (Raft), de forma simplificada.

Simula, de forma DETERMINISTICA (sem rede real), as duas ideias centrais do Raft:
  (1) ELEICAO DE LIDER por MAIORIA (quorum) dentro de um "mandato" (term);
  (2) LOG REPLICADO: uma entrada so e COMITADA quando a MAIORIA confirma.

Nao e uma implementacao de producao - e um modelo para enxergar o mecanismo.

Ampliacao do lab (Missao 2): N = 7 nos (maioria = 4) e dois cenarios extras:
  (6) dois nos caidos antes de replicar -> 5/7 ainda e maioria -> COMITA;
  (7) quatro nos caidos -> so 3/7 gravam -> NAO comita (lado sem maioria para).
Roda no Windows/venv:  python raft_sim.py
"""

N = 7                 # 7 nos
MAIORIA = N // 2 + 1  # 4 votos fecham a maioria


class No:
    def __init__(self, nid):
        self.id = nid
        self.mandato = 0
        self.votou_em = None
        self.vivo = True
        self.papel = "seguidor"
        self.log = []


def eleicao(nos, candidato, mandato):
    """O candidato pede votos no 'mandato'. Cada no vivo vota no maximo UMA vez por mandato."""
    print(f"  Mandato {mandato}: No {candidato.id} vira CANDIDATO e pede votos.")
    votos = 0
    for no in nos:
        if not no.vivo:
            print(f"    No {no.id}: (caido, nao vota)")
            continue
        if mandato > no.mandato:           # mandato novo -> libera o voto
            no.mandato = mandato
            no.votou_em = None
        if no.votou_em is None:
            no.votou_em = candidato.id
            votos += 1
            print(f"    No {no.id}: vota em {candidato.id}  (votos={votos})")
        else:
            print(f"    No {no.id}: ja votou em {no.votou_em} neste mandato")
    if votos >= MAIORIA:
        for no in nos:
            no.papel = "seguidor"
        candidato.papel = "lider"
        print(f"  => No {candidato.id} eleito LIDER (maioria {votos}/{N}, precisa de {MAIORIA}).\n")
        return candidato
    print(f"  => SEM lider neste mandato (so {votos} votos, precisa de {MAIORIA}).\n")
    return None


def replicar(nos, lider, entrada):
    """O lider propoe uma entrada; ela e comitada quando a MAIORIA grava."""
    print(f"  Lider {lider.id} propoe a entrada '{entrada}'.")
    confirmacoes = 0
    for no in nos:
        if no.vivo:
            no.log.append(entrada)
            confirmacoes += 1
            print(f"    No {no.id}: gravou '{entrada}'  (confirmacoes={confirmacoes})")
        else:
            print(f"    No {no.id}: (caido, nao grava agora - recupera depois)")
    comitada = confirmacoes >= MAIORIA
    estado = "COMITADA" if comitada else "NAO comitada"
    print(f"  => '{entrada}' {estado} ({confirmacoes}/{N}, maioria={MAIORIA}).\n")
    return comitada


def titulo(t):
    print("\n" + t)
    print("-" * len(t))


if __name__ == "__main__":
    nos = [No(i) for i in range(1, N + 1)]

    titulo("1) Eleicao de lider")
    lider = eleicao(nos, nos[0], mandato=1)       # No 1 ganha

    titulo("2) Log replicado (maioria confirma)")
    replicar(nos, lider, "x=10")

    titulo("3) O lider cai")
    lider.vivo = False
    lider.papel = "seguidor"
    print(f"  No {lider.id} (lider) CAIU. Os seguidores percebem o silencio e abrem eleicao.\n")

    titulo("4) Nova eleicao (mandato aumenta)")
    novo = eleicao(nos, nos[1], mandato=2)        # No 2 assume

    titulo("5) O sistema continua")
    replicar(nos, novo, "x=20")

    titulo("E se nao houver maioria? (voto dividido)")
    for no in nos:                                # zera para um cenario limpo
        no.mandato, no.votou_em, no.vivo, no.papel = 0, None, True, "seguidor"
    for idx in (0, 1, 3, 4):                      # nos 1, 2, 4 e 5 ja prometeram voto a um concorrente
        nos[idx].mandato = 1
        nos[idx].votou_em = "concorrente"
    eleicao(nos, nos[2], mandato=1)               # No 3 so consegue ele + Nos 6 e 7 = 3 < 4 -> sem lider

    titulo("6) Dois nos caem antes de replicar (N=7)")
    for no in nos:                                # cenario limpo: todos vivos, ninguem votou
        no.mandato, no.votou_em, no.vivo, no.papel = 0, None, True, "seguidor"
    lider = eleicao(nos, nos[0], mandato=1)
    nos[5].vivo = nos[6].vivo = False             # caem os nos 6 e 7
    print("  Nos 6 e 7 CAIRAM.\n")
    replicar(nos, lider, "y=1")                   # 5/7 >= 4 -> comita

    titulo("7) Sem maioria: a escrita NAO comita")
    for idx in (3, 4):                            # caem tambem os nos 4 e 5
        nos[idx].vivo = False
    print("  Nos 4 e 5 tambem CAIRAM (restam 3 de 7).\n")
    replicar(nos, lider, "y=2")                   # 3/7 < 4 -> nao comita

    print("Resumo: lider so com MAIORIA; entrada so COMITA com MAIORIA; "
          "sem maioria, novo mandato e nova eleicao.")
