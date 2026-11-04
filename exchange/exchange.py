# -*- coding: utf-8 -*-
# =====================================================================
# exchange.py - o programa principal (só os menus)
# Para rodar: python exchange.py
# =====================================================================

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import funcoes


def menu_investidor(cpf, investidores, moedas):
    while True:
        print("\n========== MENU DO INVESTIDOR ==========")
        print("1. Consultar saldo")
        print("2. Consultar extrato")
        print("3. Depositar")
        print("4. Sacar")
        print("5. Comprar criptomoedas")
        print("6. Vender criptomoedas")
        print("7. Atualizar cotação")
        print("8. Sair")
        print("========================================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            funcoes.consultar_saldo(cpf, investidores)
        elif opcao == "2":
            funcoes.consultar_extrato(cpf, investidores)
        elif opcao == "3":
            funcoes.depositar(cpf, investidores)
        elif opcao == "4":
            funcoes.sacar(cpf, investidores)
        elif opcao == "5":
            funcoes.comprar(cpf, investidores, moedas)
        elif opcao == "6":
            funcoes.vender(cpf, investidores, moedas)
        elif opcao == "7":
            funcoes.atualizar_cotacao(moedas)
        elif opcao == "8":
            print("\nSaindo da sua conta...")
            break
        else:
            print("Opção inválida! Digite um número de 1 a 8.")
            continue

        input("\nPressione Enter para continuar...")


def main():
    funcoes.criar_arquivos_iniciais()

    investidores = funcoes.carregar_investidores()
    moedas = funcoes.carregar_moedas()

    print("########################################")
    print("#        EXCHANGE DO VICTOR            #")
    print("#   compra e venda de criptomoedas     #")
    print("########################################")

    while True:
        print("\n1. Entrar")
        print("2. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cpf = funcoes.fazer_login(investidores)

            if cpf is not None:
                menu_investidor(cpf, investidores, moedas)
        elif opcao == "2":
            print("\nObrigado por usar a exchange!")
            break
        else:
            print("Opção inválida!")

    input("\nPressione Enter para fechar...")


if __name__ == "__main__":
    main()
