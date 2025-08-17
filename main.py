from abc import ABC, abstractmethod

# Ainda ta um pouco confuso quem extende quem, vou seguir a premisa que Cliente extende conta
class Pessoa_Fisica:
    def __init__(self, cpf, nome, data_nascimento):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

class Cliente(Pessoa_Fisica):
    def __init__(self, cpf, nome, data_nascimento, endereco, contas):
        super().__init__(cpf, nome, data_nascimento)
        self._endereco = endereco
        self._contas = contas

    def realizar_transacao(self, conta, transacao):
        pass

    def adicionar_conta(self, conta):
        pass

# Interface
class Transacao(ABC):
    def __init__(self, valor):
        self._valor = valor
    
    @abstractmethod
    def registrar(conta, valor):
        pass

# Herdaram a interface
# TODO verificar a necessidade de instanciar uma classe saque ou deposito para realizar um saque ou deposito
class Saque(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        pass

# Receberá as transacoes
class Historico:
    def adicionar_transacao(self, transacao):
        pass

# Não herda Cliente nem Historico mas recebe objeto dos dois
class Conta:
    # Número atual da contagem de conta, como não pode deletar conta pode ser um atributo de classe
    numero = 1
    def __init__(self, saldo, agencia, cliente, historico):
        self._saldo = saldo
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico

    def saldo (self):
        return f"Saldo atual:\tR$ {self._saldo:.2f}"

# Extende Conta
class Conta_Corrente(Conta):
    def __init__(self, saldo, agencia, cliente, historico, limite, limite_saques):
        super().__init__(saldo, agencia, cliente, historico)
        self._limite = limite
        self._limite_saques = limite_saques


conta = Conta(100.1232,"0001", "joao", "")

print(conta.saldo())