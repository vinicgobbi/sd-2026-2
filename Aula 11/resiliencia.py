#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aula 11 - Blindar a chamada de IA: timeout + retentativa + disjuntor.

Deterministico (sem rede real): o "servico de IA" segue um ROTEIRO de respostas,
onde cada resposta tem uma latencia (em "ticks") e um resultado (ok/erro).
Mostra, em ordem:
  - TIMEOUT: se a latencia passa do limite, a chamada e abortada (conta como falha);
  - RETENTATIVA: tenta de novo algumas vezes antes de desistir;
  - DISJUNTOR (circuit breaker): apos N falhas seguidas, ABRE e passa a falhar RAPIDO,
    protegendo o sistema; depois de um tempo de descanso, tenta "meia-volta".

Ampliacoes do lab (Missao 3):
  - BACKOFF exponencial: antes de cada retentativa espera 1, 2, 4... "ticks";
  - Cenario 2: o disjuntor REABRE (a sondagem da meia-volta falha);
  - Cenario 3: servico fora do ar, com x sem disjuntor (quantas chamadas o atingem).

Roda no Windows/venv:  python resiliencia.py
"""
import contextlib
import io

LIMITE_TIMEOUT = 3   # ticks: acima disso, e timeout
BACKOFF_BASE = 1     # ticks de espera antes da 1a retentativa (dobra a cada nova)


class ServicoInstavel:
    """Servico fake cujas respostas vem de um roteiro: (latencia, 'ok'|'erro')."""
    def __init__(self, roteiro):
        self.roteiro = list(roteiro)
        self.i = 0

    def chamar(self):
        lat, res = self.roteiro[min(self.i, len(self.roteiro) - 1)]
        self.i += 1
        if lat > LIMITE_TIMEOUT:
            raise TimeoutError(f"timeout (latencia {lat} > {LIMITE_TIMEOUT})")
        if res == "erro":
            raise RuntimeError("erro do servico")
        return f"resposta ok (latencia {lat})"


class Disjuntor:
    """fechado: deixa passar | aberto: bloqueia | meia-volta: deixa 1 tentar."""
    def __init__(self, limite_falhas=3, descanso=3):
        self.limite = limite_falhas
        self.descanso = descanso
        self.falhas = 0
        self.estado = "fechado"
        self.aberto_em = None

    def permite(self, agora):
        if self.estado == "aberto":
            if agora - self.aberto_em >= self.descanso:
                self.estado = "meia-volta"
                print(f"    [t{agora}] descanso terminou -> MEIA-VOLTA (deixa UMA sondagem)")
                return True          # deixa UMA tentativa de sondagem
            return False             # ainda em descanso: falha rapido
        return True

    def sucesso(self):
        self.falhas = 0
        self.estado = "fechado"

    def falha(self, agora):
        self.falhas += 1
        if self.falhas >= self.limite:
            self.estado = "aberto"
            self.aberto_em = agora


def chamar_blindado(servico, disjuntor, agora, tentativas=2):
    """Uma chamada protegida: consulta o disjuntor; se passar, tenta com retentativa."""
    if not disjuntor.permite(agora):
        return f"[t{agora}] disjuntor ABERTO -> falha rapido (nem chama o servico)"
    for tentativa in range(1, tentativas + 1):
        try:
            r = servico.chamar()
            disjuntor.sucesso()
            return f"[t{agora}] OK na tentativa {tentativa}: {r}  | disjuntor={disjuntor.estado}"
        except Exception as e:
            motivo = f"{type(e).__name__}: {e}"
            if tentativa < tentativas:
                espera = BACKOFF_BASE * 2 ** (tentativa - 1)        # 1, 2, 4, ...
                print(f"    [t{agora}] falha ({motivo}) -> espera {espera} tick(s) "
                      f"(backoff) e retenta ({tentativa+1}/{tentativas})")
    disjuntor.falha(agora)
    return (f"[t{agora}] FALHOU apos {tentativas} tentativas ({motivo})  | "
            f"disjuntor={disjuntor.estado} (falhas={disjuntor.falhas})")


def titulo(t):
    print("\n" + t)
    print("-" * len(t))


if __name__ == "__main__":
    # Roteiro: uma rajada ruim (timeouts/erros) que abre o disjuntor, depois o servico volta a ok.
    # Cada CHAMADA faz ate 2 tentativas, logo consome ate 2 itens do roteiro.
    roteiro = [
        (9, "ok"), (1, "erro"),   # t0: timeout + erro  -> chamada FALHA (falhas=1)
        (1, "erro"), (9, "ok"),   # t1: erro + timeout  -> chamada FALHA (falhas=2)
        (1, "erro"), (1, "erro"), # t2: erro + erro     -> chamada FALHA (falhas=3 -> ABRE)
        (1, "ok"), (1, "ok"),     # servico ja se recuperou (mas t3 nem chega a chamar)
        (1, "ok"), (1, "ok"),
    ]
    servico = ServicoInstavel(roteiro)
    disjuntor = Disjuntor(limite_falhas=3, descanso=2)

    titulo("Cenario 1 - chamadas blindadas (timeout + retentativa + disjuntor)")
    for agora in range(10):
        print(chamar_blindado(servico, disjuntor, agora))

    print("\nLeitura: timeouts e erros contam como falha (cada chamada ja tenta 2x);")
    print("na 3a chamada falha o disjuntor ABRE e em t3 falha RAPIDO (nem bate no servico);")
    print("passado o descanso, entra em MEIA-VOLTA, sonda em t4, da certo e FECHA de novo.")

    # O servico demora mais para voltar: a sondagem da meia-volta falha e o disjuntor REABRE.
    # 3 tentativas por chamada -> backoff de 1 e 2 ticks entre elas.
    roteiro = [(1, "erro")] * 9 + [(1, "erro")] * 3 + [(1, "ok")] * 10
    servico = ServicoInstavel(roteiro)
    disjuntor = Disjuntor(limite_falhas=3, descanso=2)

    titulo("Cenario 2 - a sondagem falha e o disjuntor REABRE (com backoff)")
    for agora in range(10):
        print(chamar_blindado(servico, disjuntor, agora, tentativas=3))

    titulo("Cenario 3 - servico FORA DO AR: com x sem disjuntor")
    for nome, limite in (("sem disjuntor", 10 ** 9), ("com disjuntor", 3)):
        servico = ServicoInstavel([(1, "erro")])           # erra para sempre
        disjuntor = Disjuntor(limite_falhas=limite, descanso=4)
        with contextlib.redirect_stdout(io.StringIO()):    # so interessa a contagem
            for agora in range(20):
                chamar_blindado(servico, disjuntor, agora)
        print(f"    {nome}: 20 chamadas -> {servico.i} batidas no servico caido")
    print("    => sem disjuntor, toda chamada (e cada retentativa) bate no servico que ja esta mal,")
    print("       segura o worker ate o timeout e agrava a sobrecarga; com ele, falha rapido.")
