"""
Implementação de um nó distribuído.

Responsabilidades:

- abrir servidor TCP
- aceitar conexões
- enviar mensagens
- atualizar relógio de Lamport
- despachar mensagens
- integrar Ricart-Agrawala
- integrar Bully
"""

import json
import struct
import socket
import threading

from config import (
    NODES,
    SOCKET_TIMEOUT,
    REQUEST,
    REPLY,
    ELECTION,
    OK,
    COORDINATOR,
    MESSAGE
)

from message import Message
from lamport import LamportClock
from mutex import RicartAgrawala
from bully import BullyElection


class Node:

    def __init__(self, node_id):

        self.node_id = node_id

        self.host, self.port = NODES[node_id]

        self.clock = LamportClock()

        self.mutex = RicartAgrawala(self)

        self.bully = BullyElection(self)

        self.server_socket = None

        self.running = False


    def other_nodes(self):

        return [

            pid

            for pid in NODES

            if pid != self.node_id

        ]


    def start(self):

        self.running = True

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        self.server_socket.bind(

            (self.host, self.port)

        )

        self.server_socket.listen()

        threading.Thread(

            target=self.server_loop,
            daemon=True

        ).start()

        print(
            f"Node {self.node_id} iniciado "
            f"({self.host}:{self.port})"
        )


    def stop(self):

        self.running = False

        if self.server_socket:

            self.server_socket.close()


    def server_loop(self):

        while self.running:

            try:

                conn, addr = self.server_socket.accept()

                threading.Thread(

                    target=self.handle_connection,

                    args=(conn,),

                    daemon=True

                ).start()

            except:

                pass


    def handle_connection(self, conn):

        try:

            header = self.recv_exact(conn, 4)

            if header is None:
                return

            size = struct.unpack("!I", header)[0]

            data = self.recv_exact(conn, size)

            if data is None:
                return

            message = Message.from_json(data)

            self.clock.update(message.timestamp)

            self.dispatch(message)

        finally:

            conn.close()


    def dispatch(self, message):

        if message.msg_type == REQUEST:

            self.mutex.receive_request(

                message.sender,

                message.timestamp

            )

        elif message.msg_type == REPLY:

            self.mutex.receive_reply(

                message.sender,
                message.timestamp

            )

        elif message.msg_type == ELECTION:

            self.bully.receive_election(

                message.sender

            )

        elif message.msg_type == OK:

            self.bully.receive_ok(

                message.timestamp

            )

        elif message.msg_type == COORDINATOR:

            self.bully.receive_coordinator(

                message.payload["leader"],

            )

        elif message.msg_type == MESSAGE:

            print(
                f"[Node {self.node_id}] "
                f"Mensagem recebida de {message.sender}"
            )

            print(
                f"Clock local: {self.clock.value}"
            )

            print(
                f"Conteúdo: {message.payload}"
            )


    def send(self, receiver, msg_type, payload=None, timestamp=None):

        if timestamp is None:

            timestamp = self.clock.tick()

        message = Message(

            msg_type=msg_type,

            sender=self.node_id,

            receiver=receiver,

            timestamp=timestamp,

            payload=payload

        )

        host, port = NODES[receiver]

        sock = socket.socket(

            socket.AF_INET,

            socket.SOCK_STREAM

        )

        sock.settimeout(SOCKET_TIMEOUT)

        try:

            sock.connect(

                (host, port)

            )

            data = message.to_json()

            header = struct.pack("!I", len(data))

            sock.sendall(
                header + data
            )

        except Exception as e:

            print(

                f"[Node {self.node_id}] "

                f"Falha ao enviar "

                f"para {receiver}: {e}"

            )

        finally:

            sock.close()


    def broadcast(self, msg_type, payload=None, timestamp=None):

        if timestamp is None:

            timestamp = self.clock.tick()

        for pid in self.other_nodes():

            self.send(

                pid,

                msg_type,

                payload,

                timestamp

            )


    def recv_exact(self, conn, size):

        data = b""

        while len(data) < size:

            packet = conn.recv(size - len(data))

            if not packet:
                return None

            data += packet

        return data


    def print_status(self):

        print()

        print("================================")

        print(f"Node {self.node_id}")

        print(f"Clock : {self.clock.value}")

        print(f"Líder : {self.bully.get_leader()}")

        print()

        print("Mutex")

        print(self.mutex.status())

        print()

        print("Election")

        print(self.bully.status())

        print("================================")
