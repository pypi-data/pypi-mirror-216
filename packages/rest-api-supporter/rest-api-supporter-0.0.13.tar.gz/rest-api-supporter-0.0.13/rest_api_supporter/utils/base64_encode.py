import io
import base64
from PIL import Image
import numpy
import random
import soundfile as sf
import os

def base64_encode(image):
    if isinstance(image, Image.Image):
        bytes_io = io.BytesIO()
        image.save(bytes_io, image.format)
        bytes = bytes_io.getvalue()
    elif isinstance(image, numpy.ndarray):
        '''
        f=open("up.wav", "rb")
        bytes = f.read()
        f.close()
        '''
        #'''
        wav_file = f"speech_{random.randint(1, 10000)}.wav"
        try:
            sf.write(wav_file, image, samplerate=16000)
            with open(wav_file, "rb") as f:
                bytes = f.read()
        finally:
            os.remove(wav_file)
        #'''
    base64_encoded = base64.b64encode(bytes)
    base64_encoded = base64_encoded.decode("utf-8") 
    if isinstance(image, Image.Image):
        #return "data:image/png;base64,"+base64_encoded
        return "data:image/"+image.format.lower()+";base64,"+base64_encoded
    elif isinstance(image, numpy.ndarray): 
        return "data:audio/wav;base64,"+base64_encoded
