import asyncio
import json
import logging
import os
import pathlib
import time

from quart import websocket, Blueprint, Quart
import whisper

MP3_FOLDER = pathlib.Path.cwd().resolve() / './data'
TRANSCRIPTION_FOLDER = pathlib.Path.cwd().resolve() / './transcription'
CURRENT_TRANSCRIPTION = TRANSCRIPTION_FOLDER / 'current.json'
WHISPER_MODEL = os.environ['WHISPER_MODEL']
model = whisper.load_model(WHISPER_MODEL)

logging.info(f'Whisper Model: {WHISPER_MODEL}')


app = Quart(__name__)

def cleanup_orphaned_segments():
    for mp3_file in MP3_FOLDER.iterdir():
        mp3_file.unlink()

def cleanup_orphaned_transcriptions():
    for transcription_file in TRANSCRIPTION_FOLDER.iterdir():
        transcription_file.unlink()

    CURRENT_TRANSCRIPTION.write_text(json.dumps(dict(segment=-1)))

def get_numbered_segments():

    return sorted([
        int(mp3_file.name.replace('.mp3', ''))
        for mp3_file in MP3_FOLDER.iterdir()
    ])

def transcribe_segment(segment_number: int):

    mp3_file = MP3_FOLDER / f'{segment_number:05d}.mp3'

    transcription = model.transcribe(str(mp3_file), fp16=False)

    mp3_file.unlink()

    transcription.update(segment=segment_number)

    return transcription

def load_transcription(segment_number: int):

    transcription_file = TRANSCRIPTION_FOLDER / f'{segment_number}.json'

    return json.loads(transcription_file.read_text())

def transcribe():
    

    while True:

        numbered_segments = get_numbered_segments()


        app.logger.warning(f'Found segments: {[ str(seg) for seg in numbered_segments ]}')

        while numbered_segments:

            segment_number = numbered_segments.pop(0)

            try:
                transcription = transcribe_segment(segment_number)
            except RuntimeError:
                logging.warning(f'Segment #{segment_number} has not finished being written. Waiting...')
                break
            else:
                if CURRENT_TRANSCRIPTION.is_file():

                    CURRENT_TRANSCRIPTION.unlink()

                transcription_data = json.dumps(transcription, indent=4)

                CURRENT_TRANSCRIPTION.write_text(transcription_data)

                transcription_file = TRANSCRIPTION_FOLDER / f'{segment_number}.json'

                transcription_file.write_text(transcription_data)

                time.sleep(1)


@app.before_serving
async def startup():
    app.add_background_task(cleanup_orphaned_segments)
    app.add_background_task(cleanup_orphaned_transcriptions)
    app.add_background_task(transcribe)

@app.after_serving
async def shutdown():
    
    while app.background_tasks:

        app.background_tasks.pop().cancel()

sockets = Blueprint('sockets', __name__, url_prefix='/sockets')



@sockets.websocket("/english")
async def english():
    current_transcription = json.loads(CURRENT_TRANSCRIPTION.read_text())

    await websocket.send_json(current_transcription)

    current_segment_num = current_transcription.get('segment')
    current_segment_num += 1
    while True:

        

        try:
            next_transcription = load_transcription(current_segment_num)
            await websocket.send_json(next_transcription)
            current_segment_num += 1
        except Exception as err:
            logging.warning(f'Transcription #{current_segment_num} has not finished being written. Waiting...')
            continue
        finally:
            await asyncio.sleep(2)


app.register_blueprint(sockets)        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)