"""
Implementação do algoritmo de exclusão mútua de Ricart-Agrawala.

Cada processo envia REQUEST para todos os outros processos e só entra
na região crítica após receber REPLY de todos.

Critério de prioridade:
    (timestamp, process_id)
"""

from threading import Lock, Event

from config import REQUEST, REPLY, REPLY_TIMEOUT


class RicartAgrawala:

    def __init__(self, node):

        # Referência ao Node proprietário
        self.node = node

        # Lock interno
        self.lock = Lock()

        # Indica se este processo deseja entrar na RC
        self.requesting = False

        # Indica se já está na RC
        self.in_cs = False

        # Timestamp do REQUEST atual
        self.request_timestamp = None

        # Processos dos quais ainda esperamos REPLY
        self.pending_replies = set()

        # Processos cujo REPLY foi adiado
        self.deferred = set()

        # Evento utilizado para bloquear até receber todas as respostas
        self.reply_event = Event()


    # Solicitação da região crítica
    def request_cs(self):

        with self.lock:

            self.requesting = True

            self.request_timestamp = self.node.clock.tick()

            self.pending_replies = set(self.node.other_nodes())

            self.reply_event.clear()

        print(
            f"[Node {self.node.node_id}] "
            f"Solicitando região crítica "
            f"(clock={self.request_timestamp})"
        )

        self.node.broadcast(
            REQUEST,
            timestamp=self.request_timestamp
        )

        if len(self.pending_replies) == 0:
            self.reply_event.set()

        received = self.reply_event.wait(REPLY_TIMEOUT)

        if not received:

            with self.lock:

                self.requesting = False
                self.in_cs = False
                self.request_timestamp = None
                self.pending_replies.clear()

            raise TimeoutError(
                "Tempo esgotado aguardando respostas do algoritmo Ricart-Agrawala."
            )

        with self.lock:
            self.in_cs = True

        print(f"[Node {self.node.node_id}] Entrou na região crítica.")


    # Liberação da região crítica
    def release_cs(self):

        with self.lock:

            self.in_cs = False
            self.requesting = False

            deferred = list(self.deferred)
            self.deferred.clear()

        print(f"[Node {self.node.node_id}] Saiu da região crítica.")

        for pid in deferred:
            self.node.send(
                pid,
                REPLY
            )


    # Recebimento de REQUEST
    def receive_request(self, sender, timestamp):

        send_reply = False

        with self.lock:

            if not self.requesting:

                send_reply = True

            elif self.in_cs:

                self.deferred.add(sender)

            else:

                my_priority = (
                    self.request_timestamp,
                    self.node.node_id
                )

                sender_priority = (
                    timestamp,
                    sender
                )

                if sender_priority < my_priority:

                    send_reply = True

                else:

                    self.deferred.add(sender)

        if send_reply:

            self.node.send(
                sender,
                REPLY
            )


    # Recebimento de REPLY
    def receive_reply(self, sender):

        with self.lock:

            self.pending_replies.discard(sender)

            if len(self.pending_replies) == 0:
                self.reply_event.set()


    # Estado atual
    def status(self):

        with self.lock:

            return {
                "requesting": self.requesting,
                "in_cs": self.in_cs,
                "waiting": list(self.pending_replies),
                "deferred": list(self.deferred),
                "timestamp": self.request_timestamp
            }