import io
import base64
from PIL import Image

#image = Image.open("rock.jpg")
#base64 = base64_encode(image)
#print(base64) #/9j/4AAQSkZJRgABAQAAA ... bSjrTEf/9k=
def base64_encode(image):
    bytesIO = io.BytesIO()
    try:
        image.save(bytesIO, "JPEG")
    except:
        image.save(bytesIO, "PNG")
    b64encoded = base64.b64encode(bytesIO.getvalue())
    base64_str = b64encoded.decode("utf-8")
    return base64_str
