# rest-api-supporter

https://pypi.org/project/rest-api-supporter/
```
pip install rest-api-supporter
```

Supported APIs  

```
from rest_api_supporter.utils.base64_decode import base64_decode

print(full_encoded) #data:image/png;base64,/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
                     #data:audio/wav;base64,UklGRiTuAgBXQVZFZm...At84WACNZGwA=
                     #/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
base64_decoded = base64_decode(full_encoded)
print(type(base64_decoded)) #<class 'PIL.JpegImagePlugin.JpegImageFile'>
                            #<class 'bytes'>
                            #<class 'PIL.JpegImagePlugin.JpegImageFile'>
```

```
from rest_api_supporter.utils.base64_encode import base64_encode

image = Image.open("rock.jpg")
base64 = base64_encode(image)
print(base64) #data:image/png;base64,/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
```
```
from rest_api_supporter.utils.base64_encode import base64_encode
import datasets

path = 'up.wav'
dataset = datasets.Dataset.from_dict({"audio": [path]})
dataset = dataset.cast_column("audio", datasets.Audio())
array = dataset[0]["audio"]["array"]
#sampling_rate = dataset[0]["audio"]["sampling_rate"] #Wav2Vec2FeatureExtractor was trained using a sampling rate of 16000. Please make sure that the provided `raw_speech` input was sampled with 16000 and not 8000.
sampling_rate = 16000
base64 = base64_encode(array)
print(base64) #data:audio/wav;base64,UklGRiTuAgBXQVZFZm...At84WACNZGwA=
```
