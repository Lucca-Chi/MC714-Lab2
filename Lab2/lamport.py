"""
Implementação do Relógio Lógico de Lamport.

Todos os eventos locais, envios e recebimentos de mensagens devem
utilizar esta classe para manter a consistência dos timestamps.
"""

from threading import Lock


class LamportClock:
    """
    Implementação thread-safe do relógio lógico de Lamport.
    """

    def __init__(self):
        self._clock = 0
        self._lock = Lock()

    @property
    # Retorna o valor do relógio
    def value(self):

        with self._lock:
            return self._clock

    # Evento interno pra seguir o clock
    def tick(self):

        with self._lock:
            self._clock += 1
            return self._clock

    # Atualiza o relógio ao receber uma mensagem.
    def update(self, received_timestamp: int):
        
        with self._lock:
            self._clock = max(self._clock, received_timestamp) + 1
            return self._clock

    # Reinicia o relógio
    def reset(self):

        with self._lock:
            self._clock = 0

    def __str__(self):
        return str(self.value)