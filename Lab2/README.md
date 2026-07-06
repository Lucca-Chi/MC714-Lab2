# Laboratório 2: Sistemas Distribuídos (MC714)

Este projeto consiste na implementação de um sistema distribuído composto por múltiplos nós independentes que se comunicam através de Sockets TCP puras (troca de mensagens em rede real). O sistema integra três conceitos fundamentais de sistemas distribuídos: Sincronização via Relógio Lógico de Lamport, Exclusão Mútua através do Algoritmo Distribuído de Ricart-Agrawala e Eleição de Líder via Algoritmo do Bully.

## Arquitetura do Projeto

* config.py: Centraliza as configurações de rede, IDs, portas e constantes dos protocolos.
* message.py: Define a estrutura padronizada de mensagens trafegadas em formato JSON.
* lamport.py: Implementação thread-safe do Relógio Lógico de Lamport.
* mutex.py: Mecanismo do algoritmo Ricart-Agrawala para controle de Região Crítica.
* bully.py: Lógica do algoritmo do Bully para eleição e monitoramento do coordenador.
* node.py: O servidor/cliente TCP do nó que gerencia as threads de recepção e despacho de mensagens.
* run.py: Interface de linha de comando (CLI) interativa para controle do usuário.

---

## Execução Local Multi-Terminal

### Passo 1: Abrir os Terminais
1. Abra **4 janelas ou abas** independentes do seu PowerShell.
2. Em cada uma delas, navegue até a pasta raiz do projeto.

### Passo 2: Inicializar os Nós
Execute um comando em cada terminal para subir as instâncias correspondentes:

* No Terminal 1 (Nó 1):
```
python run.py 1
```

* No Terminal 2 (Nó 2):
```
python run.py 2
```

* No Terminal 3 (Nó 3):
```
python run.py 3
```

* No Terminal 4 (Nó 4):
```
python run.py 4
```

Assim que o quarto nó for iniciado, a topologia estará completa. Os relógios lógicos serão sincronizados e o Nó 4 (por possuir o maior identificador ativo) assumirá o papel de líder inicial através do algoritmo do Bully.

### Passo 3: Utilizando a CLI Interativa
Cada terminal apresentará o menu numérico isolado daquele nó. Você poderá digitar as opções.

### Passo 4: Encerramento Limpo
Para fechar o sistema sem deixar processos pendentes em segundo plano ou pendurados nas portas, utilize a opção 6.

---

## Execução via Docker Compose

Para garantir que todos os 4 nós distribuídos iniciem em conformidade, sem a necessidade de abrir múltiplos terminais manuais, foi aberta a possibilidade de usar o Docker Compose. O ambiente foi configurado utilizando a diretiva network_mode: host, garantindo compatibilidade direta com os sockets TCP locais mapeados no trabalho.

### Passo 1: Construir e iniciar o Cluster Distribuído
Na raiz do projeto, execute o comando abaixo para compilar a imagem e inicializar os 4 nós de forma concorrente:

```
docker compose up --build
```

Você observará no terminal unificado os logs de inicialização de cada nó e o estabelecimento do líder inicial via algoritmo do Bully.

### Passo 2: Interagindo com os Nós individualmente
Como os nós rodam simultaneamente, para acessar o menu interativo CLI de um nó específico e testar os cenários de Exclusão Mútua (Ricart-Agrawala) ou forçar novas eleições, abra um novo terminal e anexe-se ao contêiner desejado.

Para descobrir o nome exato gerado para o contêiner na sua máquina, execute:

```
docker ps
```

Com o nome em mãos, utilize o comando attach para entrar no menu:

```
docker attach NOME_DO_CONTAINER
```

### Passo 3: Finalizar o ambiente e limpar os recursos
Para encerrar todas as instâncias e limpar completamente os recursos criados pelo Docker, execute:

```
docker compose down
```
