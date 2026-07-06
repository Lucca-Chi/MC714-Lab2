"""
Inicialização do programa.

Uso:

    python run.py <node_id>

Exemplo:

    python run.py 1
"""

import sys
import time

from config import MESSAGE
from node import Node


def menu():

    print()
    print("====================================")
    print("1 - Mostrar status")
    print("2 - Enviar mensagem de teste")
    print("3 - Solicitar região crítica")
    print("4 - Liberar região crítica")
    print("5 - Iniciar eleição")
    print("6 - Sair")
    print("====================================")


def main():

    if len(sys.argv) != 2:

        print("Uso:")
        print("python run.py <node_id>")
        return

    node_id = int(sys.argv[1])

    node = Node(node_id)

    node.start()

    print()
    print(f"Nó {node_id} iniciado.")

    while True:

        menu()

        option = input("Escolha: ").strip()

        if option == "1":

            node.print_status()

        elif option == "2":

            try:

                receiver = int(input("Destino: "))

                payload = {
                    "text": input("Mensagem: ")
                }

                node.send(

                    receiver,

                    MESSAGE,

                    payload

                )

            except Exception as e:

                print(e)

        elif option == "3":

            try:

                node.mutex.request_cs()

            except Exception as e:

                print(e)

        elif option == "4":

            node.mutex.release_cs()

        elif option == "5":

            node.bully.start_election()

        elif option == "6":

            node.stop()

            print("Encerrando...")

            time.sleep(1)

            break

        else:

            print("Opção inválida.")


if __name__ == "__main__":

    main()