from abc import ABC, abstractmethod

# Ainda ta um pouco confuso quem extende quem, vou seguir a premisa que Cliente extende conta
class Pessoa_Fisica:
    def __init__(self, cpf, nome, data_nascimento):
        pass

class Cliente(Pessoa_Fisica):
    def __init__(self, cpf, nome, data_nascimento, endereco, contas):
        super().__init__(cpf, nome, data_nascimento)
# Interface
class Transacao(ABC):
    @abstractmethod
    def registrar():
        pass

# Herdaram a interface
class Saque(Transacao):
    def registrar():
        pass

class Deposito(Transacao):
    def registrar():
        pass

# Receberá as transacoes
class Historico:
    def adicionar_transacao():
        pass

# Não herda Cliente nem Historico mas recebe objeto dos dois
class Conta:
    # Número atual da contagem de conta, como não pode deletar conta pode ser um atributo de classe
    numero = 1
    def __init__(self, saldo, agencia, cliente, historico):
        pass

# Extende Conta
class Conta_Corrente(Conta):
    def __init__(self, saldo, agencia, cliente, historico):
        super().__init__(saldo, agencia, cliente, historico)