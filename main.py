from abc import ABC, abstractmethod
from datetime import datetime
import os

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class Pessoa_Fisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf
    
    def __str__(self):
        return f"Nome:\t\t\t{self._nome}\nData de nascimento:\t{self._data_nascimento}\nCPF:\t\t\t{self._cpf}\nEndereço:\t\t{self._endereco}"

# Interface de Transação
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(conta, valor):
        pass

# Realiza um saque e registra no histórico
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Realiza um deposito e registra no histórico
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Receberá as transacoes
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._agencia = "0001"
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def criar_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        excedeu_saldo = self._saldo < valor

        if excedeu_saldo:
            print("\nNão foi possível fazer a transação! O valor inserido ultrapassa o saldo atual.")
            return False
        
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        else:
            print("\nDigite um valor válido")
            return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realizado com sucesso!")
            return True
        else:
            print("\nDigite um valor válido")
            return False

# Extende Conta
class Conta_Corrente(Conta):
    def __init__(self,numero, cliente,*, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self._historico.transacoes if transacao["tipo"] == Saque.__name__]
        ); 

        excedeu_limite = self._limite < valor
        excedeu_limite_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\nNão foi possível fazer a transação! O valor inserido ultrapassa o limite atual.")
            return False

        if excedeu_limite_saques:
            print("\nNão foi possível fazer a transação! O valor inserido ultrapassa o limite de saques da conta.")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""\
            Agência:\t{self._agencia}
            C/C:\t{self._numero}
            Titular:\t{self.cliente}
        """

# recebe um boolean e limpa o terminal 
def limpar_terminal(*,mode:bool=True):
    if mode:
        input("\nDigite qualquer tecla para continuar: ")
    os.system('cls')

def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario._cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def filtrar_contas(numero, contas):
    contas_filtrados = [conta for conta in contas if conta._numero == numero]
    return contas_filtrados[0] if contas_filtrados else None

def selecionar_conta_usuario(usuario,*, numero=None):
    if not usuario._contas:
        print("Operação inválida! Usuário não possuí contas.")
        return
    if numero:
        return filtrar_contas(numero, usuario._contas)
    
    return usuario._contas

def criar_usuario(usuarios):
    cpf = input("\nDigite o seu cpf: ")
    if filtrar_usuarios(cpf, usuarios):
        print("Operação inválida! esse usuário já existe.")
        return

    nome = input("\nDigite o nome do completo: ")
    data = input("\nDigite a sua data de nascimento: ")
    
    endereco = input("\nDigite o seu endereco: ")

    usuarios.append(Pessoa_Fisica(nome,data,cpf,endereco))

def criar_conta(contas, usuario):
    if not usuario:
        print("Usuario inexistente")
        return
    cliente = usuario._cpf

    numero = int(input("\nDigite o número: "))
    if numero < 0:
        print("Valor inválido! Digite um número válido.")
        return
    if filtrar_contas(numero, contas):
        print("Operação inválida! essa conta já existe.")
        return

    limite = input("\nDigite o limite: ")
    if limite == "":
        limite = False
    elif float(limite) < 0:
        print("Valor inválido! Digite um limite válido.")
        return
    limite = float(limite) if limite else False

    limite_saques = input("\nDigite o limite de saques: ")
    if limite_saques == "":
        limite_saques = False
    elif int(limite_saques) <= 0:
        print("Valor inválido! Digite um número de limite de saques válido.")
        return
    limite_saques = int(limite_saques) if limite_saques else False

    if limite and limite_saques:
        conta = Conta_Corrente(numero, cliente, limite=limite, limite_saques=limite_saques)
    elif limite and not limite_saques:
        conta = Conta_Corrente(numero, cliente, limite=limite)
    else:
        conta = Conta_Corrente(numero, cliente)

    contas.append(conta)
    usuario.adicionar_conta(conta)

def listar_contas(contas):
    for conta in contas:
        print(conta)

def transacao_usuario_conta(usuarios):
    cpf = input("Digite o CPF do cliente que realizará a transação: ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if not usuario:
        return False, False
    
    numero = int(input("Digite o número da conta: "))
    conta = selecionar_conta_usuario(usuario, numero=numero)

    if not conta:
        return usuario, False
    
    return usuario, conta

def sacar(usuarios):
    usuario, conta = transacao_usuario_conta(usuarios)

    if not usuario:
        print("Operação inválida! Usuário não encontrado.")
        return
    elif not conta:
        print("Operação inválida! Conta não encontrada.")
        return

    valor = float(input("\nDigite o valor a ser sacado: "))
    transacao = Saque(valor)

    usuario.realizar_transacao(conta, transacao)

def depositar(usuarios):
    usuario, conta = transacao_usuario_conta(usuarios)

    if not usuario:
        print("Operação inválida! Usuário não encontrado.")
        return
    elif not conta:
        print("Operação inválida! Conta não encontrada.")
        return

    valor = float(input("\nDigite o valor a ser depositado: "))
    transacao = Deposito(valor)

    usuario.realizar_transacao(conta, transacao)

def exibir_extrato(usuarios):
    usuario, conta = transacao_usuario_conta(usuarios)

    if not usuario:
        print("Operação inválida! Usuário não encontrado.")
        return
    elif not conta:
        print("Operação inválida! Conta não encontrada.")
        return
    limpar_terminal(mode=False)
    print(conta,end="\n\n")
    for transacao in conta.historico._transacoes:
        for chave, valor in transacao.items():
            print(f"{chave}:\t{valor}")
        print()

def main():
    limpar_terminal(mode=False)
    MENSAGEM = """
    Novo Usuário:\t[u]
    Nova Conta:\t\t[c]
    Listar Contas:\t[l]
    Sacar:\t\t[s]
    Depositar:\t\t[d]
    Extrato:\t\t[e]
    Sair:\t\t[q]
    """
    contas = []
    usuarios = []
    while True:
        print(" BEM VINDO AO BANCO SEM NOME ".center(36,"#"))
        print(MENSAGEM)
        opcao = input("Digite uma das opções: ")

        if opcao == "u":
            limpar_terminal(mode=False)
            criar_usuario(usuarios)
            limpar_terminal()

        elif opcao == "c":
            limpar_terminal(mode=False)
            usuario = filtrar_usuarios(input("Digite o CPF do cliente a qual a conta vai ser vinculada: "), usuarios)
            criar_conta(contas, usuario)
            limpar_terminal()

        elif opcao == "l":
            limpar_terminal(mode=False)
            usuario = filtrar_usuarios(input("Digite o CPF do cliente a qual as contas vão ser listadas: "), usuarios)
            limpar_terminal(mode=False)
            print(usuario, end="\n\n")
            contas_usuario = selecionar_conta_usuario(usuario)
            listar_contas(contas_usuario)
            limpar_terminal()

        elif opcao == "s":
            limpar_terminal(mode=False)
            sacar(usuarios)
            limpar_terminal()

        elif opcao == "d":
            limpar_terminal(mode=False)
            depositar(usuarios)
            limpar_terminal()

        elif opcao == "e":
            limpar_terminal(mode=False)
            exibir_extrato(usuarios)
            limpar_terminal()

        elif opcao == "q":
            limpar_terminal(mode=False)

            print("Obrigado por usar nossos serviços!\n\n")
            break
        else:
            print("\n\nDigite uma opção válida!")
            limpar_terminal()

main()