from flask import Flask, render_template, redirect, request
from keras.models import load_model
from keras.backend import get_session
import os
from app.functions import prepare_model
from app.functions import get_prediction
from app.functions import print_text


language = {
    'input': '',
    'output': '',
    'trans': ''  
}

file_path = os.path.abspath(os.getcwd()) + "/app/models"

UPLOAD_FOLDER = '/app/models/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model_spa = prepare_model('spanish')
model_fra = prepare_model('french')
graph = get_session().graph

print('models are loaded')


@app.route('/')
def index():

    return render_template("index.html", lang = language, text = '')


@app.route('/form', methods=["GET","POST"])
def form():

    if request.method == "POST":
        
        if request.form.get('input-text'):

            input_text = request.form["input-text"]
            print(input_text)
            lang = request.form.get('lang')
            print(lang)
            # haikus = request.form['haik-text']

            global graph
            with graph.as_default():

                if lang == 'spa':

                    # folder = '/' + lang
                    folder = '/' + 'spanish'
                    output_text = get_prediction(model_spa, folder, input_text)

                    if output_text:

                        language = {
                            'input': input_text,
                            'output': output_text,
                            'trans': 'to Spanish'  
                        }

                        return render_template("index.html", lang = language, text = '')

                if lang == 'fra':

                    # folder = '/' + lang
                    folder = '/' + 'french'
                    output_text = get_prediction(model_fra, folder, input_text)

                    if output_text:

                        language = {
                            'input': input_text,
                            'output': output_text,
                            'trans': 'to French' 
                        }

                        return render_template("index.html", lang = language, text = '')
    
    return redirect('/', code=302)


@app.route('/haiku', methods=["GET","POST"])
def haiku():

    if request.method == "POST":
        
        haikus = print_text().decode("utf-8")
        
        input_text = request.form["eng"]
        output_text = request.form.get('other')
        trans = request.form['langg']

        if trans == 'spa':
            trans = 'to Spanish'

        if trans == 'fra':
            trans = 'to French'

        language = {
            'input': input_text,
            'output': output_text,
            'trans': trans 
        }
        
        return render_template("index.html", lang = language, text = haikus)


if __name__ == "__main__":
    app.run()