"""
Implementação do algoritmo Bully.

O processo com maior ID vivo torna-se o líder.

Mensagens utilizadas:

ELECTION
OK
COORDINATOR
"""

from threading import Lock, Timer

from config import (
    ELECTION,
    OK,
    COORDINATOR,
    ELECTION_TIMEOUT
)


class BullyElection:

    def __init__(self, node):

        self.node = node

        self.lock = Lock()

        self.leader = None

        self.election_running = False

        self.received_ok = False

        self.timer = None


    # Inicia eleição
    def start_election(self):

        with self.lock:

            if self.election_running:
                return

            self.election_running = True
            self.received_ok = False

        print(f"[Node {self.node.node_id}] Iniciando eleição.")

        higher = [
            pid
            for pid in self.node.other_nodes()
            if pid > self.node.node_id
        ]

        if len(higher) == 0:

            self.become_leader()
            return

        for pid in higher:

            self.node.send(
                pid,
                ELECTION
            )

        self.timer = Timer(
            ELECTION_TIMEOUT,
            self.finish_wait
        )

        self.timer.start()


    # Final do tempo de espera
    def finish_wait(self):

        with self.lock:

            if not self.received_ok:

                self.become_leader()

            else:
                self.election_running = False


    # Torna-se líder
    def become_leader(self):

        with self.lock:

            self.leader = self.node.node_id
            self.election_running = False

        print(
            f"[Node {self.node.node_id}] "
            f"Sou o novo líder."
        )

        self.node.broadcast(

            COORDINATOR,

            payload={
                "leader": self.node.node_id
            }

        )


    # Recebe ELECTION
    def receive_election(self, sender):

        print(

            f"[Node {self.node.node_id}] "
            f"Recebeu ELECTION de {sender}"

        )

        self.node.send(

            sender,

            OK

        )

        if not self.election_running:

            self.start_election()


    # Recebe OK
    def receive_ok(self, timestamp):

        self.node.clock.update(timestamp)

        with self.lock:

            self.received_ok = True


    # Recebe COORDINATOR
    def receive_coordinator(self, leader):

        with self.lock:

            self.leader = leader
            self.election_running = False

            if self.timer is not None:

                self.timer.cancel()

        print(

            f"[Node {self.node.node_id}] "
            f"Novo líder = {leader}"

        )


    # Consulta líder
    def get_leader(self):

        with self.lock:

            return self.leader


    # Estado
    def status(self):

        with self.lock:

            return {

                "leader": self.leader,
                "running": self.election_running,
                "received_ok": self.received_ok

            }