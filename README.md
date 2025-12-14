# 🎵 Streaming de Áudio via WebSockets (WAV) – Cliente & Servidor

## 📝 Sobre

Este projeto implementa um sistema distribuído de **streaming contínuo de áudio via WebSockets, onde um servidor envia um arquivo WAV em blocos** e um **cliente reproduz o áudio em tempo real**, utilizando PyAudio, buffer e threads para garantir reprodução contínua e sem ruídos.

A solução simula um fluxo de áudio em tempo real, com controle de taxa de envio, pré-bufferização e detecção automática de fim do streaming.

---

## 📖 Informações
Este projeto demonstra conceitos essenciais de:

- comunicação cliente-servidor usando WebSockets,

- streaming contínuo de dados binários,

- envio de áudio PCM em frames,

- reprodução de áudio em tempo real com PyAudio,

- uso de threads para desacoplar recepção e reprodução,

- uso de buffer (Queue) para reduzir travamentos,

- protocolo simples baseado em:

- envio inicial de um header JSON com informações do áudio,

- envio contínuo de dados binários (frames do WAV),

- mensagem final indicando o fim do streaming.


O servidor lê o arquivo WAV em blocos de tamanho fixo e os envia de forma contínua via WebSocket, respeitando o tempo real do áudio.
O cliente recebe esses blocos, armazena em buffer e reproduz conforme chegam.

---

## 🏁 Como Utilizar

### Clone o repositório
```
git clone https://github.com/luisalll/-streaming-audio-WEBSOCKET
cd -streaming-audio-WEBSOCKET
```

### Entre no arquivo do cliente e preencha com o IP do servidor onde tem:

No arquivo do cliente, ajuste o endereço do servidor WebSocket:

`URI = "ws://IP_DO_SERVIDOR:50007"`

(você pode executar o comando `ipconfig` ou `ip a` no terminal onde será rodado o servidor para descobrir essa informação)

---

## 📦 Pré-requisitos
Python3 e pip

```
sudo apt install python3 python3-pip
```

PyAudio

```
pip install websockets pyaudio
```
---

## 📱 Usabilidade
### Rodando o Servidor 🔊

O servidor:

- cria um servidor WebSocket,

- aguarda a conexão do cliente,

- recebe a mensagem inicial de solicitação,

- lê o arquivo WAV,

- envia um header JSON com informações do áudio,

- transmite os dados do áudio em blocos binários,

- respeita o tempo real do áudio durante o envio,

- envia uma mensagem de fim ao concluir o streaming.

#### Execute:

```
python server.py
```

### Rodando o Cliente 🎧

O cliente:

- conecta-se ao servidor via WebSocket,

- envia a mensagem inicial solicitando o áudio,

- recebe o header com informações do WAV,

- inicia uma thread dedicada para reprodução,

- utiliza um buffer (Queue) para suavizar a reprodução,

- toca o áudio conforme os blocos chegam,

- encerra automaticamente ao receber o sinal de fim.

#### Execute:
```
python client.py
```
---

## 🎶 Resultados Esperados


- Conexão via WebSockets

- Envio do header com metadados do áudio

- Fatiamento do WAV em blocos

- Streaming contínuo de dados binários

- Bufferização no cliente

- Reprodução progressiva em tempo real

- Encerramento correto ao fim da música

- O sistema valida corretamente todo o ciclo de streaming contínuo de áudio via WebSockets, desde o envio até a reprodução.

---

## ⛏️ Tecnologias Utilizadas

- Python 3

- WebSockets

- Asyncio

- Threads (threading)

- PyAudio

- Queue

- JSON

- WAV PCM 16-bit

---

## 🎤 Equipe

[Caio Lopes](https://github.com/caioolops)

[Letícia Uchôa](https://github.com/leticiauchoa)

[Lorena Castello Branco](https://github.com/lccb2)

[Luísa Longo](https://github.com/luisalll)

[Maria Eduarda Braga](https://github.com/mecbDuda)
