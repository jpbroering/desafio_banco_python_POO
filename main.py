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
        return f"Nome:\t\t\t{self._nome}\nData de nascimento:\t{self._data_nascimento}\CPD:\t\t\t{self._cpf}\nEndereço:\t\t{self._endereco}"

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
    def __init__(self,numero, cliente, limite=500, limite_saques=3):
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

def main():
    limpar_terminal(mode=False)
    MENSAGEM = """
    Novo Usuário:\t[u]
    Nova Conta:\t\t[c]
    Listar Conta:\t[l]
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
            nome = input("\nDigite o nome do completo: ")
            data = input("\nDigite a sua data de nascimento: ")
            cpf = input("\nDigite o seu cpf: ")
            endereco = input("\nDigite o seu endereco: ")
            usuarios.append(Pessoa_Fisica(nome,data,cpf,endereco))
            print(usuarios[0])
            limpar_terminal()
        elif opcao == "c":
            limpar_terminal(mode=False)

        elif opcao == "l":
            limpar_terminal(mode=False)

        elif opcao == "s":
            limpar_terminal(mode=False)

        elif opcao == "d":
            limpar_terminal(mode=False)

        elif opcao == "e":
            limpar_terminal(mode=False)

        elif opcao == "q":
            limpar_terminal(mode=False)

            print("Obrigado por usar nossos serviços!\n\n")
            break
        else:
            print("\n\nDigite uma opção válida!")
            limpar_terminal()

    
main()