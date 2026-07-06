"""
Define o formato das mensagens trocadas entre os nós.

Todas as mensagens são serializadas em JSON antes de serem enviadas
pela rede e desserializadas quando recebidas.
"""

import json
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Message:
    """
    Estrutura padrão utilizada em toda comunicação.
    """

    msg_type: str
    sender: int
    timestamp: int = 0

    receiver: Optional[int] = None

    payload: Optional[dict] = None

    # Serializa a mensagem para bytes
    def to_json(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")

    # Reconstrói uma Message a partir dos bytes recebidos
    @staticmethod
    def from_json(data: bytes):
        obj = json.loads(data.decode("utf-8"))
        return Message(**obj)

    def __str__(self):
        return (
            f"[{self.msg_type}] "
            f"from={self.sender} "
            f"to={self.receiver} "
            f"clock={self.timestamp} "
            f"payload={self.payload}"
        )


# Função auxiliar para criar mensagens
def create_message(
    msg_type: str,
    sender: int,
    timestamp: int,
    receiver: Optional[int] = None,
    payload: Optional[dict] = None,
) -> Message:

    return Message(
        msg_type=msg_type,
        sender=sender,
        receiver=receiver,
        timestamp=timestamp,
        payload=payload,
    )