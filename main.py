from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoa_Fisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

# Interface
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(conta, valor):
        pass

# Herdaram a interface
# TODO verificar a necessidade de instanciar uma classe saque ou deposito para realizar um saque ou deposito
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        pass

# Receberá as transacoes
class Historico:
    def __init__(self):
        self._transacoes = []
    def adicionar_transacao(self, transacao):
        pass

# Não herda Cliente nem Historico mas recebe objeto dos dois
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
        excedeu_saldo = saldo < valor
        # excedeu_limite = limite < valor
        # excedeu_saque = numero_saques >= LIMITE_SAQUE

        if excedeu_saldo:
            print("Não foi possível fazer a transação! O valor inserido ultrapassa o saldo atual.")
            return saldo
        # elif excedeu_limite:
        #     print("Não foi possível fazer a transação! O valor inserido ultrapassa o limite da conta.")
        #     return saldo
        # elif excedeu_saque:
        #     print("Não foi possível fazer a transação! O limite de saques diários foi alcançado.")
        #     return saldo
        elif valor > 0:
            numero_saques += 1
            saldo -= valor
            retorno = f"R$ {valor:.2f} foram sacados!\n"
            # extrato.append(retorno)
            print(retorno)
            return saldo
        else:
            print("Digite um valor válido")
            return saldo
        
    def depositar(self, valor):
        if valor > 0:
            saldo += valor
            retorno = f"R$ {valor:.2f} foram depositados!\n"
            extrato.append(retorno)
            print(retorno)
            return saldo
        else:
            print("\nDigite um valor válido")
            return 0

# Extende Conta
class Conta_Corrente(Conta):
    def __init__(self, cliente):
        super().__init__(cliente)
        self._limite = 500
        self._limite_saques = 3


conta = Conta(100.1232, "joao")

print(conta.saldo())