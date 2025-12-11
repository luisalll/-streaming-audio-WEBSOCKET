import asyncio
import websockets
import json
import time
import os
import wave  # para ler o WAV

HOST = "0.0.0.0"
PORT = 50007
AUDIO_FILE = "musica.wav"

# Tamanho do chunk em frames (não em bytes)
CHUNK_FRAMES = 2048  # você pode ajustar

async def send_chunks(websocket):
    print("Cliente conectado!")
    try:
        async for message in websocket:
            print(f"Recebido do cliente: {message}")

            # Se vier como bytes, tenta decodificar pra string
            if isinstance(message, bytes):
                message = message.decode("utf-8")

            # Protocolo simples: cliente manda "PLAY" para começar o áudio
            if message == "PLAY":
                if not os.path.exists(AUDIO_FILE):
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Arquivo de áudio não encontrado"
                    }))
                    continue

                print("Iniciando streaming de áudio para o cliente...")

                with wave.open(AUDIO_FILE, "rb") as wf:
                    rate = wf.getframerate()
                    channels = wf.getnchannels()
                    sample_width = wf.getsampwidth()

                    bytes_per_second = rate * channels * sample_width
                    bytes_per_chunk = CHUNK_FRAMES * channels * sample_width
                    chunk_duration = bytes_per_chunk / bytes_per_second

                    # 1) Envia cabeçalho com informações do áudio
                    header = {
                        "type": "audio_header",
                        "rate": rate,
                        "channels": channels,
                        "sample_width": sample_width,
                        "chunk_frames": CHUNK_FRAMES,
                    }
                    await websocket.send(json.dumps(header))

                    # 2) Envia os dados de áudio como binário
                    while True:
                        frames = wf.readframes(CHUNK_FRAMES)
                        if not frames:
                            break

                        # frames é bytes -> envia como binário
                        await websocket.send(frames)

                        # Mantém a taxa de envio parecida com tempo real
                        await asyncio.sleep(chunk_duration)

                    # 3) Envia mensagem avisando que acabou
                    await websocket.send(json.dumps({"type": "end"}))
                    print("Fim do streaming de áudio.")
            else:
                # eco padrão, caso queira manter
                resposta = f"Então você disse que: {message}"
                await websocket.send(resposta)

    except websockets.exceptions.ConnectionClosedOK:
        print("Conexão fechada normalmente.")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Conexão fechada com erro: {e}")

async def main():
    async with websockets.serve(send_chunks, HOST, PORT):
        print(f"Servidor WebSocket rodando em ws://{HOST}:{PORT}")
        await asyncio.Future()  # truque pra não encerrar

if __name__ == "__main__":
    asyncio.run(main())
