"""
Arquivo responsável pelas configurações da rede distribuída.

Cada nó possui:
    - um identificador único (ID)
    - um endereço IP
    - uma porta TCP

O dicionário NODES deve ser igual em todos os processos.
"""

HOST = "127.0.0.1"

NUM_NODES = 4

# Configuração dos nós
# ID -> (HOST, PORTA)

NODES = {
    1: (HOST, 5001),
    2: (HOST, 5002),
    3: (HOST, 5003),
    4: (HOST, 5004),
}


# Tipos de mensagens utilizados por todos os algoritmos

# Relógio de Lamport
LAMPORT = "LAMPORT"

# Ricart-Agrawala
REQUEST = "REQUEST"
REPLY = "REPLY"

# Bully
ELECTION = "ELECTION"
OK = "OK"
COORDINATOR = "COORDINATOR"

# Mensagem genérica para testes
MESSAGE = "MESSAGE"

# Encerramento
SHUTDOWN = "SHUTDOWN"


# Configurações a mais

# Timeout de sockets (segundos)
SOCKET_TIMEOUT = 2

# Tempo entre verificações do líder (segundos)
LEADER_CHECK_INTERVAL = 5

# Tempo máximo aguardando respostas de eleição
ELECTION_TIMEOUT = 3

# Tempo máximo aguardando replies do Ricart-Agrawala
REPLY_TIMEOUT = 10