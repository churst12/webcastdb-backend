from flask import Flask, request
import requests
app = Flask(__name__)

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
    response = operation.result(timeout=500)
    text = ""

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        #print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        #print('Confidence: {}'.format(result.alternatives[0].confidence))
        text += result.alternatives[0].transcript
    return text

counter = "01"

for i in range(17):
    print("creating text: " + counter)
    f= open("./lecture2/" +counter + ".txt","w+")
    f.write(transcribe_gcs("gs://webcastdb/lecture-audio/lecture2/"+ counter+".flac"))
    if counter[1] == "9":
        counter = "10"
    else:
        newcounter = counter[0]
        newcounter += str(int(counter[1]) + 1)
        counter = newcounter
f.close()

