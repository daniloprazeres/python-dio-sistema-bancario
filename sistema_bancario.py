# ===============================================
# 💰 SISTEMA BANCÁRIO
# Desenvolvido por Danilo Praseres
# ===============================================

from datetime import datetime

# ======== FUNÇÕES DE INTERFACE ========

def menu():
    menu = """
================ MENU ==================
[d] Depositar
[s] Sacar
[e] Extrato
[t] Transferência
[nu] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[au] Atualizar Usuário
[q] Sair
========================================
=> """
    return input(menu).lower()

# ======== FUNÇÕES BANCÁRIAS ========

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"[{datetime.now().strftime('%d/%m/%Y %H:%M')}] Depósito: +R$ {valor:.2f}\n"
        print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("❌ Operação falhou! Valor inválido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("❌ Saldo insuficiente.")
    elif excedeu_limite:
        print(f"❌ Valor do saque excede o limite de R$ {limite:.2f}.")
    elif excedeu_saques:
        print("❌ Número máximo de saques atingido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"[{datetime.now().strftime('%d/%m/%Y %H:%M')}] Saque: -R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"💸 Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("❌ Valor inválido.")
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO ==========")
    print("Nenhuma movimentação registrada." if not extrato else extrato)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=============================\n")


def transferir(contas, extrato):
    origem = input("Informe o número da conta de origem: ")
    destino = input("Informe o número da conta de destino: ")

    conta_origem = next((c for c in contas if str(c["numero_conta"]) == origem), None)
    conta_destino = next((c for c in contas if str(c["numero_conta"]) == destino), None)

    if not conta_origem or not conta_destino:
        print("❌ Conta de origem ou destino não encontrada!")
        return extrato

    valor = float(input("Informe o valor da transferência: R$ "))

    if valor <= 0:
        print("❌ Valor inválido.")
        return extrato
    elif valor > conta_origem["saldo"]:
        print("❌ Saldo insuficiente na conta de origem.")
        return extrato

    # Efetuar transferência
    conta_origem["saldo"] -= valor
    conta_destino["saldo"] += valor

    mensagem = f"[{datetime.now().strftime('%d/%m/%Y %H:%M')}] Transferência: -R$ {valor:.2f} para {conta_destino['usuario']['nome']}\n"
    conta_origem["extrato"] += mensagem
    conta_destino["extrato"] += f"[{datetime.now().strftime('%d/%m/%Y %H:%M')}] Transferência recebida: +R$ {valor:.2f} de {conta_origem['usuario']['nome']}\n"

    print(f"✅ Transferência de R$ {valor:.2f} concluída com sucesso!")
    return extrato


# ======== FUNÇÕES DE USUÁRIOS ========

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("⚠️ Já existe um usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("✅ Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def atualizar_usuario(usuarios):
    cpf = input("Informe o CPF do usuário que deseja atualizar: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("❌ Usuário não encontrado.")
        return

    print(f"Usuário encontrado: {usuario['nome']}")
    novo_nome = input("Novo nome (deixe vazio para manter): ")
    novo_endereco = input("Novo endereço (deixe vazio para manter): ")

    if novo_nome:
        usuario["nome"] = novo_nome
    if novo_endereco:
        usuario["endereco"] = novo_endereco

    print("✅ Dados atualizados com sucesso!")


# ======== FUNÇÕES DE CONTAS ========

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do titular: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("✅ Conta criada com sucesso!")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "extrato": "",
            "numero_saques": 0
        }
    print("❌ Usuário não encontrado! Crie um usuário antes.")


def listar_contas(contas):
    if not contas:
        print("⚠️ Nenhuma conta cadastrada.")
        return

    for conta in contas:
        linha = f"""
Agência: {conta['agencia']}
C/C: {conta['numero_conta']}
Titular: {conta['usuario']['nome']}
Saldo: R$ {conta['saldo']:.2f}
"""
        print("=" * 40)
        print(linha)


# ======== FUNÇÃO PRINCIPAL ========

def main():
    LIMITE_SAQUES = 5
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            numero_conta = input("Informe o número da conta para depósito: ")
            conta = next((c for c in contas if str(c["numero_conta"]) == numero_conta), None)

            if conta:
                valor = float(input("Informe o valor do depósito: R$ "))
                conta["saldo"], conta["extrato"] = depositar(conta["saldo"], valor, conta["extrato"])
            else:
                print("❌ Conta não encontrada.")

        elif opcao == "s":
            numero_conta = input("Informe o número da conta para saque: ")
            conta = next((c for c in contas if str(c["numero_conta"]) == numero_conta), None)

            if conta:
                valor = float(input("Informe o valor do saque: R$ "))
                conta["saldo"], conta["extrato"], conta["numero_saques"] = sacar(
                    saldo=conta["saldo"],
                    valor=valor,
                    extrato=conta["extrato"],
                    limite=500,
                    numero_saques=conta["numero_saques"],
                    limite_saques=LIMITE_SAQUES,
                )
            else:
                print("❌ Conta não encontrada.")

        elif opcao == "e":
            numero_conta = input("Informe o número da conta para ver o extrato: ")
            conta = next((c for c in contas if str(c["numero_conta"]) == numero_conta), None)

            if conta:
                exibir_extrato(conta["saldo"], extrato=conta["extrato"])
            else:
                print("❌ Conta não encontrada.")

        elif opcao == "t":
            transferir(contas, extrato="")

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "au":
            atualizar_usuario(usuarios)

        elif opcao == "q":
            print("👋 Obrigado por usar! Até a próxima.")
            break

        else:
            print("⚠️ Operação inválida! Tente novamente.")


if __name__ == "__main__":
    main()
