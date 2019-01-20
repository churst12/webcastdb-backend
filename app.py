from flask import Flask, request
import requests
app = Flask(__name__)

from sqlalchemy import create_engine
db = create_engine('mysql+pymysql://chhurst@ucsc.edu:ucsccruzhacks2019@127.0.0.1/webcastdb')

def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)
    text = ""

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        #print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        #print('Confidence: {}'.format(result.alternatives[0].confidence))
        text += result.alternatives[0].transcript
    return text





	

@app.route('/')
def hello_world():
    with db.connect() as conn:
        result = conn.execute("show columns from lectures").fetchall()
        columns = ""
        for row in result:
           columns += row[0] + ", "

    return columns

@app.route('/getText', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
    	with db.connect() as conn:
        result = conn.execute("show columns from lectures").fetchall()
        columns = ""
        for row in result:
           columns += row[0] + ", "

        return columns
    else:
        return "nothing to see here"



