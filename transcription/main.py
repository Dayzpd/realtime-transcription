import json
import logging
import os
import pathlib
from pprint import pprint
import time 

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import whisper

MP3_FOLDER = pathlib.Path.cwd().resolve() / './data'
TRANSCRIPTION_FOLDER = pathlib.Path.cwd().resolve() / './transcription'
CURRENT_TRANSCRIPTION = TRANSCRIPTION_FOLDER / 'current.json'
WHISPER_MODEL = os.environ['WHISPER_MODEL']
logging.info(f'Whisper Model: {WHISPER_MODEL}')
model = whisper.load_model(WHISPER_MODEL)

class AudioSegmentHandler(FileSystemEventHandler):
    def on_created(self, event):
        mp3_file = pathlib.Path(event.src_path).resolve()

        transcription = None
        while transcription is None:
            try:
                transcription = model.transcribe(str(mp3_file), fp16=False)
            except RuntimeError:
                transcription = None
                logging.warning(f'{mp3_file} has not finished being written. Waiting...')
                time.sleep(2)
                continue
        
        #transcription_file = TRANSCRIPTION_FOLDER / f"{mp3_file.name.split('.')[0]}.json"

        #transcription_file.write_text(json.dumps(transcription, indent=4))

        if CURRENT_TRANSCRIPTION.is_file():

            CURRENT_TRANSCRIPTION.unlink()

        CURRENT_TRANSCRIPTION.write_text(json.dumps(transcription, indent=4))

def main():

    
    logging.info(f'Data Folder: {MP3_FOLDER}')
    observer = Observer()
    event_handler = AudioSegmentHandler()
    observer.schedule(event_handler, path=str(MP3_FOLDER))
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()



if __name__ == "__main__":
    main()