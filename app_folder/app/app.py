from flask import Flask, render_template, jsonify, redirect, send_file, request
import keras
from keras import backend as K
import os
from functions import get_prediction

languages = {
    'english': {
        'input': 'Enter Text',
        'output': 'Translation',
        'button': 'Eng - Spa'
    },
    'another': {
        'input': 'Olala',
        'output': 'Heyheyhey',
        'button': 'Eng - Ola'
    }
}

file_path = os.path.abspath(os.getcwd()) + "/models"
print(file_path)

UPLOAD_FOLDER = 'models/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = None
graph = None

def load_model():
    global model
    global graph
    model = keras.models.load_model(os.path.join(file_path or app.config['UPLOAD_FOLDER'], "model_01081_32.h5"))
    graph = K.get_session().graph


@app.route('/')
def index():

    return render_template("index.html", lang = languages)

@app.route('/form', methods=["GET","POST"])
def form():

    if request.method == "POST":

        if request.form.get('input-text'):

            input_text = request.form["input-text"]
            print(input_text)

            global graph
            with graph.as_default():

                output_text = get_prediction(model, input_text)

                if output_text:

                    languages = {
                        'english': {
                        'input': input_text,
                        'output': output_text,
                        'button': 'Eng - Spa'
                        },
                        'another': {
                        'input': 'Olala',
                        'output': 'Heyheyhey',
                        'button': 'Eng - Ola'
                        }
                    }
                    
                    return render_template("index.html", lang = languages)

    return redirect('/', code=302)



if __name__ == "__main__":
    load_model()
    app.run(debug=True)