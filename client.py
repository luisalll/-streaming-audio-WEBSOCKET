import asyncio
import websockets
import json
import pyaudio
import threading
import queue

URI = "ws://localhost:50007"

audio_queue = queue.Queue()

def audio_player(stream):
    while True:
        data = audio_queue.get()
        if data is None:
            break
        stream.write(data, exception_on_underflow=False)

async def receive_audio():
    async with websockets.connect(
        URI,
        max_size=None,
        ping_interval=None
    ) as websocket:
        print("Conectado ao servidor")

        await websocket.send("Quero desafiar a gravidade!")

        # Recebe cabeçalho/header (informações da música)
        header = json.loads(await websocket.recv())

        rate = header["rate"]
        channels = header["channels"]
        sample_width = header["sample_width"]
        chunk_frames = header["chunk_frames"]

        print("Header recebido:", rate, channels, sample_width)

        # Configura PyAudio
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(sample_width),
            channels=channels,
            rate=rate,
            output=True,
            frames_per_buffer=chunk_frames
        )

        player = threading.Thread(
            target=audio_player,
            args=(stream,),
            daemon=True
        )
        player.start()

        # Para recepção contínua
        while True:
            msg = await websocket.recv()

            if isinstance(msg, bytes):
                audio_queue.put(msg)
            else:
                data = json.loads(msg)
                if data.get("type") == "end":
                    audio_queue.put(None)
                    break

        player.join()
        stream.stop_stream()
        stream.close()
        p.terminate()

        print("Música completa tocada")

if __name__ == "__main__":
    asyncio.run(receive_audio())
