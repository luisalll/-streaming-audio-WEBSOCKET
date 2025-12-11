import asyncio
import websockets
import json
import pyaudio

URI = "ws://localhost:50007"

async def receive_audio():
    async with websockets.connect(URI) as websocket:
        #Pede para começar a tocar
        await websocket.send("Quero desafiar a gravidade!")

        #Recebe cabeçalho/header (informações da música)
        header_msg = await websocket.recv()
        if isinstance(header_msg, bytes):
            header_msg = header_msg.decode("utf-8")
        header = json.loads(header_msg)

        if header.get("type") != "audio_header":
            print("ERRO! Sem header.")
            return

        rate = header["rate"]
        channels = header["channels"]
        sample_width = header["sample_width"]

        print(f"Header recebido: rate={rate}, channels={channels}, width={sample_width}")

        # Configura PyAudio
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(sample_width),
            channels=channels,
            rate=rate,
            output=True,
        )

        try:
            while True:
                msg = await websocket.recv()

                # Pode ser texto (JSON) ou binário (dados de áudio)
                if isinstance(msg, bytes):
                    # Dados de áudio
                    stream.write(msg)
                else:
                    data = json.loads(msg)
                    if data.get("type") == "end":
                        print("Fim da música recebido.")
                        break
                    elif data.get("type") == "error":
                        print("Erro do servidor:", data.get("message"))
                        break
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

if __name__ == "__main__":
    asyncio.run(receive_audio())
