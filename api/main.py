import asyncio
import json
import logging
import pathlib

from quart import websocket, Quart

TRANSCRIPTION_FOLDER = pathlib.Path.cwd().resolve() / 'transcription'
CURRENT_TRANSCRIPTION = TRANSCRIPTION_FOLDER / 'current.json'

app = Quart(__name__)

@app.websocket("/english")
async def random_data():
    current_transcription = None
    while True:
        try:
            next_transcription = CURRENT_TRANSCRIPTION.read_text()
        except Exception as err:
            logging.warning(f'{CURRENT_TRANSCRIPTION.name} has not finished being written. Waiting...')
            await asyncio.sleep(2)
            continue

        if current_transcription != next_transcription:
            current_transcription = next_transcription
            await websocket.send(current_transcription)
        else:
            logging.warning(f'No new transcription to return. Waiting...')
            await asyncio.sleep(2)
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)