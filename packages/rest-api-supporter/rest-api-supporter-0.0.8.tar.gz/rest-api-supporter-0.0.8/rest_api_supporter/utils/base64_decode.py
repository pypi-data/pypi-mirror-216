import base64
import io
from PIL import Image

'''
#print(full_encoded) #data:image/png;base64,/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
                     #data:audio/wav;base64,UklGRiTuAgBXQVZFZm...At84WACNZGwA=
                     #/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
base64_decoded = base64_decode(full_encoded)
print(type(base64_decoded)) #<class 'PIL.JpegImagePlugin.JpegImageFile'>
                            #<class 'bytes'>
                            #<class 'PIL.JpegImagePlugin.JpegImageFile'>
'''
def base64_decode(full_encoded):
    if "base64," in full_encoded:
        #print(full_encoded) #data:image/png;base64,/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
                             #data:audio/wav;base64,UklGRiTuAgBXQVZFZm...At84WACNZGwA=
        front = full_encoded.split('base64,')[0]
        encoded = full_encoded.split('base64,')[1]
        decoded = base64.b64decode(encoded)
        if "image" in front:
            image = Image.open(io.BytesIO(decoded))
            return image
        elif "audio" in front:
            return decoded
    else:
        #print(full_encoded) #/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
                             #UklGRiTuAgBXQVZFZm...At84WACNZGwA=
        decoded = base64.b64decode(full_encoded)
        image = Image.open(io.BytesIO(decoded))
        return image
