from .base64_decode import base64_decode
from .base64_encode import base64_encode
import os
from PIL import Image
import numpy

def base64_postprocess(prediction):
    if isinstance(prediction, list):
        for i, p in enumerate(prediction):
            for k in p.keys():
                v = p[k]
                if isinstance(v, Image.Image) or isinstance(v, bytes):
                    base64_encoded = base64_encode(v)
                    prediction[i][k] = base64_encoded
    elif isinstance(prediction, dict):   
        for k in prediction.keys():
            v = prediction[k]
            if isinstance(v, Image.Image) or isinstance(v, bytes):
                base64_encoded = base64_encode(v)
                prediction[k] = base64_encoded
