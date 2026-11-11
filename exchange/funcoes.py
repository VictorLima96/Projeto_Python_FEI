# -*- coding: utf-8 -*-
# =====================================================================
# funcoes.py - as regras da exchange
# Tudo que envolve arquivo, login, saldo, extrato e operações fica aqui.
# O exchange.py cuida só dos menus.
# =====================================================================

import os
import random
import getpass
import math
from datetime import datetime

ENCODING = "utf-8"

# ---------- CAMINHOS DOS ARQUIVOS ----------

# pego o caminho da pasta do próprio arquivo para o programa funcionar
# de qualquer lugar (não depende de onde o terminal foi aberto)
PASTA_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")

ARQ_INVESTIDORES = os.path.join(PASTA_DADOS, "investidores.txt")
ARQ_MOEDAS = os.path.join(PASTA_DADOS, "moedas.txt")
ARQ_EXTRATO = os.path.join(PASTA_DADOS, "extrato.txt")

# quantas casas decimais cada moeda mostra na tela
CASAS = {"REAL": 2, "BTC": 8, "ETH": 6, "XRP": 2}


# ---------- FUNÇÕES DE ARQUIVO ----------

def moedas_iniciais():
    # cotações de exemplo, só para o programa não abrir vazio
    return {
        "BTC": {"cotacao": 350000.00, "taxa_compra": 0.02, "taxa_venda": 0.03},
        "ETH": {"cotacao": 16000.00, "taxa_compra": 0.01, "taxa_venda": 0.02},
        "XRP": {"cotacao": 2.57, "taxa_compra": 0.01, "taxa_venda": 0.01},
    }


def criar_arquivos_iniciais():
    # na primeira execução nada existe, então eu crio a pasta e os arquivos
    if not os.path.exists(PASTA_DADOS):
        os.makedirs(PASTA_DADOS)

    if not os.path.exists(ARQ_INVESTIDORES):
        arquivo = open(ARQ_INVESTIDORES, "w", encoding=ENCODING)
        arquivo.write("12345678900;Victor Lima;123456;1000.00;0.00000000;0.00000000;0.00\n")
        arquivo.close()

    if not os.path.exists(ARQ_MOEDAS):
        salvar_moedas(moedas_iniciais())

    if not os.path.exists(ARQ_EXTRATO):
        arquivo = open(ARQ_EXTRATO, "w", encoding=ENCODING)
        arquivo.close()


def carregar_investidores():
    # devolve um dicionário: cpf -> {nome, senha, carteira}
    investidores = {}

    if not os.path.exists(ARQ_INVESTIDORES):
        return investidores

    arquivo = open(ARQ_INVESTIDORES, "r", encoding=ENCODING)

    for linha in arquivo:
        linha = linha.strip()

        # linha vazia (por exemplo a última) é ignorada
        if linha == "":
            continue

        campos = linha.split(";")

        # se alguém editar o txt na mão e quebrar a linha, eu pulo ela
        if len(campos) != 7:
            continue

        try:
            carteira = {
                "REAL": float(campos[3]),
                "BTC": float(campos[4]),
                "ETH": float(campos[5]),
                "XRP": float(campos[6]),
            }
        except ValueError:
            continue

        investidores[campos[0]] = {
            "nome": campos[1],
            "senha": campos[2],
            "carteira": carteira,
        }

    arquivo.close()
    return investidores


def salvar_investidores(investidores):
    temporario = ARQ_INVESTIDORES + ".tmp"

    with open(temporario, "w", encoding=ENCODING) as arquivo:
        for cpf, dados in investidores.items():
            c = dados["carteira"]

            arquivo.write(
                f"{cpf};{dados['nome']};{dados['senha']};"
                f"{c['REAL']:.2f};"
                f"{c['BTC']:.8f};"
                f"{c['ETH']:.6f};"
                f"{c['XRP']:.2f}\n"
            )

        arquivo.flush()
        os.fsync(arquivo.fileno())

    os.replace(temporario, ARQ_INVESTIDORES)

def carregar_moedas():
    moedas = {}

    if not os.path.exists(ARQ_MOEDAS):
        return moedas

    arquivo = open(ARQ_MOEDAS, "r", encoding=ENCODING)

    for linha in arquivo:
        linha = linha.strip()

        if linha == "":
            continue

        campos = linha.split(";")

        if len(campos) != 4:
            continue

        try:
            moedas[campos[0]] = {
                "cotacao": float(campos[1]),
                "taxa_compra": float(campos[2]),
                "taxa_venda": float(campos[3]),
            }
        except ValueError:
            continue

    arquivo.close()
    return moedas


def salvar_moedas(moedas):
    temporario = ARQ_MOEDAS + ".tmp"

    with open (temporario, "w", encoding=ENCODING) as arquivo:
        for nome, dados in moedas.items():
            arquivo.write(
                f"{nome};"
                f"{dados['cotacao']:.2f};"
                f"{dados['taxa_compra']:.4f};"
                f"{dados['taxa_venda']:.4f}\n"
            )

        arquivo.flush()
        os.fsync(arquivo.fileno())

    os.replace(temporario, ARQ_MOEDAS)

def registrar_extrato(cpf, sinal, valor, moeda, cotacao, taxa, carteira):
    # grava UMA linha do extrato. Uso o modo "a" para nunca apagar o histórico.
    agora = datetime.now()
    data = agora.strftime("%d-%m-%Y")
    hora = agora.strftime("%H:%M")

    linha = (
        f"{cpf};{data};{hora};{sinal};{valor:.8f};{moeda};{cotacao:.2f};{taxa:.2f};"
        f"{carteira['REAL']:.2f};{carteira['BTC']:.8f};"
        f"{carteira['ETH']:.6f};{carteira['XRP']:.2f}"
    )

    arquivo = open(ARQ_EXTRATO, "a", encoding=ENCODING)
    arquivo.write(linha + "\n")
    arquivo.close()


def ler_extrato(cpf):
    linhas = []

    if not os.path.exists(ARQ_EXTRATO):
        return linhas

    arquivo = open(ARQ_EXTRATO, "r", encoding=ENCODING)

    for linha in arquivo:
        linha = linha.strip()

        if linha == "":
            continue

        campos = linha.split(";")

        if len(campos) != 12:
            continue

        if campos[0] == cpf:
            linhas.append(campos)

    arquivo.close()
    return linhas


# ---------- FORMATAÇÃO ----------

def formatar(valor, moeda="REAL"):
    casas = CASAS.get(moeda, 2)
    return f"{valor:.{casas}f}"


def formatar_cpf(cpf):
    # 12345678900 -> 123.456.789-00
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def mostrar_saldos(cpf, investidores):
    dados = investidores[cpf]
    c = dados["carteira"]

    print("\nNome:", dados["nome"])
    print("CPF:", formatar_cpf(cpf))
    print(f"Reais: R$ {c['REAL']:.2f}")
    print(f"Bitcoin: {c['BTC']:.8f}")
    print(f"Ethereum: {c['ETH']:.6f}")
    print(f"Ripple: {c['XRP']:.2f}")


def mostrar_cotacoes(moedas):
    print("\n----- COTAÇÕES ATUAIS -----")

    for nome, dados in moedas.items():
        print(
            f"{nome}: R$ {dados['cotacao']:.2f}"
            f"   (taxa de compra {dados['taxa_compra'] * 100:.0f}%"
            f" | taxa de venda {dados['taxa_venda'] * 100:.0f}%)"
        )

# ---------- ENTRADAS DO USUÁRIO ----------

def pedir_cpf():
    # 3 tentativas; se errar tudo, volta para o menu
    for tentativa in range(3):
        cpf = input("CPF (só os 11 números): ").strip()

        if len(cpf) == 11 and cpf.isdigit():
            return cpf

        print("CPF inválido! Digite 11 números, sem pontos e sem traços.")

    print("Tentativas esgotadas.")
    return None

def pedir_senha():
    for tentativa in range(3):
        senha = getpass.getpass("Senha (6 dígitos): ").strip()

        if len(senha) == 6 and senha.isdigit():
            return senha

        print("Senha inválida! Ela precisa ter exatamente 6 números.")

    print("Tentativas esgotadas.")
    return None


def pedir_valor(mensagem):
    # aceito vírgula também, porque todo mundo digita 150,50
    texto = input(mensagem).strip().replace(",", ".")

    try:
        valor = float(texto)
    except ValueError:
        print("Valor inválido! Digite apenas números.")
        return None

    if not math.isfinite(valor):
        print("Valor inválido! Use um número finito.")
        return None

    if valor <= 0:
        print("O valor precisa ser maior que zero.")
        return None

    if round(valor, 2) != valor:
        print("O valor precisa ter no máximo 2 casas decimais.")
        return None

    return valor


def escolher_moeda(moedas):
    print("\nMoedas disponíveis:", ", ".join(moedas.keys()))
    moeda = input("Qual moeda você quer? ").strip().upper()

    if moeda not in moedas:
        print("Moeda inválida!")
        return None

    return moeda


def confirmar_senha(cpf, investidores):
    # usada no saldo, extrato, compra e venda (o login já foi feito antes)
    for tentativa in range(3):
        senha = getpass.getpass("Digite sua senha (6 dígitos): ").strip()

        if senha == investidores[cpf]["senha"]:
            return True

        print("Senha incorreta!")

    print("Muitas tentativas erradas. Voltando ao menu...")
    return False


# ---------- LOGIN ----------

def fazer_login(investidores):
    while True:
        print("\n===== LOGIN =====")
        cpf = pedir_cpf()
        if cpf is None:
            return None

        senha = pedir_senha()
        if senha is None:
            return None

        if cpf in investidores and investidores[cpf]["senha"] == senha:
            print(f"\nBem-vindo(a), {investidores[cpf]['nome']}!")
            return cpf

        print("CPF ou senha incorretos!")

        if input("Tentar novamente? (S/N): ").strip().upper() != "S":
            return None


# ---------- OPERAÇÕES DO INVESTIDOR ----------

def consultar_saldo(cpf, investidores):
    if not confirmar_senha(cpf, investidores):
        return

    mostrar_saldos(cpf, investidores)


def consultar_extrato(cpf, investidores):
    if not confirmar_senha(cpf, investidores):
        return

    linhas = ler_extrato(cpf)
    dados = investidores[cpf]

    print("\nNome:", dados["nome"])
    print("CPF:", formatar_cpf(cpf))

    if len(linhas) == 0:
        print("Nenhuma operação registrada ainda.")
        return

    print()

    for campos in linhas:
        # cpf;data;hora;sinal;valor;moeda;cotacao;taxa;reais;btc;eth;xrp
        data, hora = campos[1], campos[2]
        sinal = campos[3]
        valor = float(campos[4])
        moeda = campos[5]
        cotacao = float(campos[6])
        taxa = float(campos[7])

        print(
            f"{data} {hora} {sinal} {formatar(valor, moeda):>12} {moeda:<4}"
            f" CT: {cotacao:<10.2f} TX: {taxa:<6.2f}"
            f" REAL: {float(campos[8]):.2f}"
            f" BTC: {float(campos[9]):.8f}"
            f" ETH: {float(campos[10]):.6f}"
            f" XRP: {float(campos[11]):.2f}"
        )


def depositar(cpf, investidores):
    print("\n===== DEPÓSITO =====")

    valor = pedir_valor("Valor do depósito: R$ ")
    if valor is None:
        return

    carteira = investidores[cpf]["carteira"]
    carteira["REAL"] = round(carteira["REAL"] + valor, 2)

    registrar_extrato(cpf, "+", valor, "REAL", 0.0, 0.0, carteira)
    salvar_investidores(investidores)

    print("Depósito realizado!")
    mostrar_saldos(cpf, investidores)


def sacar(cpf, investidores):
    print("\n===== SAQUE =====")

    carteira = investidores[cpf]["carteira"]
    valor = pedir_valor("Valor do saque: R$ ")
    if valor is None:
        return

    if valor > carteira["REAL"]:
        print(f"Saldo insuficiente! Você tem R$ {carteira['REAL']:.2f}.")
        return

    carteira["REAL"] = round(carteira["REAL"] - valor, 2)

    registrar_extrato(cpf, "-", valor, "REAL", 0.0, 0.0, carteira)
    salvar_investidores(investidores)

    print("Saque realizado!")
    mostrar_saldos(cpf, investidores)


def comprar(cpf, investidores, moedas):
    print("\n===== COMPRA =====")

    if not confirmar_senha(cpf, investidores):
        return

    mostrar_cotacoes(moedas)

    moeda = escolher_moeda(moedas)
    if moeda is None:
        return

    carteira = investidores[cpf]["carteira"]
    cotacao = moedas[moeda]["cotacao"]
    taxa_compra = moedas[moeda]["taxa_compra"]

    valor = pedir_valor(f"Quanto você quer gastar em {moeda}? R$ ")
    if valor is None:
        return

    # a taxa é cobrada em cima do valor investido, então o desconto é maior
    taxa = round(valor * taxa_compra, 2)
    total = round(valor + taxa, 2)

    if total > carteira["REAL"]:
        print(f"Saldo insuficiente! Você precisa de R$ {total:.2f} (valor + taxa) e tem R$ {carteira['REAL']:.2f}.")
        return

    casas = CASAS[moeda]

    quantidade = round(valor / cotacao, casas)

    if quantidade <= 0:
        print("Valor muito pequeno para comprar essa moeda.")
        return

    carteira["REAL"] = round(
        carteira["REAL"] - total, 2
    )

    carteira[moeda] = round(
        carteira[moeda] + quantidade, casas
    )

    registrar_extrato(cpf, "+", quantidade, moeda, cotacao, taxa, carteira)
    salvar_investidores(investidores)

    print(f"\nCompra feita: {formatar(quantidade, moeda)} {moeda}")
    print(f"Valor investido: R$ {valor:.2f}")
    print(f"Taxa de compra ({taxa_compra * 100:.0f}%): R$ {taxa:.2f}")
    print(f"Total debitado: R$ {total:.2f}")
    mostrar_saldos(cpf, investidores)

def vender(cpf, investidores, moedas):
    print("\n===== VENDA =====")

    if not confirmar_senha(cpf, investidores):
        return

    mostrar_cotacoes(moedas)

    moeda = escolher_moeda(moedas)
    if moeda is None:
        return

    carteira = investidores[cpf]["carteira"]
    cotacao = moedas[moeda]["cotacao"]
    taxa_venda = moedas[moeda]["taxa_venda"]

    print(f"Você tem {formatar(carteira[moeda], moeda)} {moeda}.")

    texto = input(
        f"Quanto você quer vender de {moeda}? "
    ).strip().replace(",", ".")

    try:
        quantidade = float(texto)
    except ValueError:
        print("Quantidade inválida!")
        return

    if not math.isfinite(quantidade):
        print("Quantidade inválida!")
        return

    casas = CASAS[moeda]

    if quantidade <= 0:
        print("A quantidade precisa ser maior que zero.")
        return


    if round(quantidade, casas) != quantidade:
        print(
            f"Essa moeda aceita no máximo {casas} casas decimais."
        )
        return

    quantidade = round(quantidade, casas)
    saldo_disponivel = round(carteira[moeda], casas)

    if quantidade > saldo_disponivel:
        print("Você não tem tudo isso para vender!")
        return

    bruto = quantidade * cotacao
    taxa = bruto * taxa_venda
    receber = bruto - taxa

    carteira[moeda] = round(
        saldo_disponivel - quantidade, casas
    )

    carteira["REAL"] = round(
        carteira["REAL"] + receber, 2
    )

    registrar_extrato(cpf, "-", quantidade, moeda, cotacao, taxa, carteira)
    salvar_investidores(investidores)

    print(f"\nVenda feita: {formatar(quantidade, moeda)} {moeda}")
    print(f"Valor bruto: R$ {bruto:.2f}")
    print(f"Taxa de venda ({taxa_venda * 100:.0f}%): R$ {taxa:.2f}")
    print(f"Você recebeu: R$ {receber:.2f}")
    mostrar_saldos(cpf, investidores)


def atualizar_cotacao(moedas):
    print("\n===== ATUALIZANDO COTAÇÕES =====")
    print("Cada moeda varia no máximo 5% para cima ou para baixo.\n")

    for nome in moedas:
        antiga = moedas[nome]["cotacao"]

        # random.uniform(-0.05, 0.05) devolve algo entre -5% e +5%
        variacao = random.uniform(-0.05, 0.05)
        nova = round(antiga * (1 + variacao), 2)

        # cotação nunca fica zero ou negativa
        if nova <= 0:
            nova = 0.01

        moedas[nome]["cotacao"] = nova

        print(f"{nome}: R$ {antiga:.2f} -> R$ {nova:.2f} ({variacao * 100:+.2f}%)")

    salvar_moedas(moedas)