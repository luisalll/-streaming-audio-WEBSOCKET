import asyncio
import websockets
import json
import wave
import os

HOST = "0.0.0.0"
PORT = 50007
AUDIO_FILE = "musica.wav"

# Tamanho do chunk em frames (não em bytes)
CHUNK_FRAMES = 8192

async def stream_audio(websocket):
    print("Cliente conectado")

     # Se vier como bytes, tenta decodificar pra string
    async for message in websocket:
        if isinstance(message, bytes):
            message = message.decode("utf-8")

        if message == "Quero desafiar a gravidade!":
            if not os.path.exists(AUDIO_FILE):
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Arquivo não encontrado"
                }))
                return

            with wave.open(AUDIO_FILE, "rb") as wf:
                rate = wf.getframerate()
                channels = wf.getnchannels()
                sample_width = wf.getsampwidth()

                print("INFO WAV:", rate, channels, sample_width)

                # HEADER
                # 1) Envia cabeçalho com informações do áudio
                await websocket.send(json.dumps({
                    "type": "audio_header",
                    "rate": rate,
                    "channels": channels,
                    "sample_width": sample_width,
                    "chunk_frames": CHUNK_FRAMES
                }))

                # STREAM
                # 2) Envia os dados de áudio como binário
                while True:
                    frames = wf.readframes(CHUNK_FRAMES)
                    if not frames:
                        break
                    await websocket.send(frames)

                 # 3) Envia mensagem avisando que acabou
                await websocket.send(json.dumps({"type": "end"}))
                print("Fim do streaming")

async def main():
    async with websockets.serve(stream_audio, HOST, PORT, max_size=None):
        print(f"Servidor WebSocket em ws://{HOST}:{PORT}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
