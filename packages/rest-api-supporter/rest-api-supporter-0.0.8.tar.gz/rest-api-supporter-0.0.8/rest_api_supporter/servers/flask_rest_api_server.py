from flask import Flask
from flask import request
import flask_ngrok
from flask import Blueprint
import pathlib
import json
import base64
from PIL import Image
import re
from ..utils import image_to_base64
from ..utils import base64_to_image

class FlaskRestAPIServer():
    def __init__(self, blueprint_file_path, ngrok=True, enable_blueprint_test=True):
        super().__init__()
        self.ngrok = ngrok
        self.enable_blueprint_test = enable_blueprint_test

        if ngrok:
            self.index_url = '/'
            self.api_url = '/api'
        else:
            self.folder_name = pathlib.Path(blueprint_file_path).parts[-2]
            #print(self.folder_name) #son_height_tabular_regression_scikit_learn
            self.folder_name = self.folder_name.replace('_', '-')
            #print(self.folder_name) #son-height-tabular-regression-scikit-learn
            self.index_url = f'/{self.folder_name}/'
            self.api_url = f'/{self.folder_name}/api'

    def get_urls(self):
        return self.index_url, self.api_url

    def get_app(self, index_function, api_function):
        if self.ngrok:
            app = Flask(__name__)
        else:
            app = Blueprint(self.folder_name, self.folder_name)

        if self.ngrok or (not self.ngrok and self.enable_blueprint_test):
            @app.route(self.index_url)
            def index():
                return index_function()

        @app.route(self.api_url, methods=['post'])
        def api():
            return self.predict(request, api_function)

        '''
        if __name__ == "__main__":
            if self.ngrok:
                flask_ngrok.run_with_ngrok(app)
                app.run()
        '''
        if self.ngrok:
            flask_ngrok.run_with_ngrok(app)
            app.run()

        return app

    def is_float(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False

    def preprocess(self, d):
        #print(d['file']) #iVBORw...w9RndTMZLiy1AAAAABJRU5ErkJggg==
        #print(type(d['file'])) #<class 'str'>
        d_ = {}
        for key in d:
            value = d[key]
            if value.startswith('data:') : #Image
                '''
                #print(value) #data:image/jpeg;base64,/9j/4TT...
                value = value.replace("data:", "") #data url 부분 제거
                value = re.sub('^.+,', '', value)
                #print(value) #/9j/4TT...
                bytes = base64.b64decode(value)
                bytesIO = io.BytesIO(bytes)
                value = Image.open(bytesIO)
                '''
                #'''
                value = base64_to_image(value)
                #'''
            elif self.is_float(value):
                value = float(value)
            d_[key] = value
        return d_

    def postprocess(self, d):
        if isinstance(d, dict):
            d_ = {}
            for key in d:
                value = d[key]
                if str(type(value)) == "<class 'PIL.PngImagePlugin.PngImageFile'>":
                    value = image_to_base64(value)
                d_[key] = value
            return d_
        elif isinstance(d, list):
            l = d
            l_ = []
            for d in l:
                d_ = {}
                for key in d:
                    value = d[key]
                    if str(type(value)) == "<class 'PIL.PngImagePlugin.PngImageFile'>":
                        value = image_to_base64(value)
                    d_[key] = value
                l_.append(d_)
            return l_

    def predict(self, request, predict_function):
        payload = request.get_json()
        data = payload['data']
        #print(data) #[{'a': 1, 'b': 2}]
        postprocessed_examples = []
        for example in data:
            preprocessed_example = self.preprocess(example)
            #print(example) #{'file': <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=561x561 at 0x7F8457E79A30>}
            output_example = predict_function(**preprocessed_example)
            postprocessed_example = self.postprocess(output_example)
            postprocessed_examples.append(postprocessed_example)
        j = json.dumps({'data': postprocessed_examples})
        return j
