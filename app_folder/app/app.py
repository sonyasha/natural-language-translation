from flask import Flask, render_template, jsonify, redirect, send_file, request
import keras
from keras import backend as K
import os
from functions import get_prediction

language = {
    'input': '',
    'output': '',
    'trans': ''   
}

file_path = os.path.abspath(os.getcwd()) + "/models"

UPLOAD_FOLDER = 'models/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model_spa = None
model_fra = None
graph = K.get_session().graph

def load_model_spa():
    global model_spa
    model_spa = keras.models.load_model(os.path.join(file_path or app.config['UPLOAD_FOLDER'], "spa/model_01081_32.h5"))

def load_model_fra():
    global model_fra
    model_fra = keras.models.load_model(os.path.join(file_path or app.config['UPLOAD_FOLDER'], "fra/fra_32.h5"))


@app.route('/')
def index():

    return render_template("index.html", lang = language)
    

@app.route('/form', methods=["GET","POST"])
def form():

    if request.method == "POST":

        if request.form.get('input-text'):

            input_text = request.form["input-text"]
            print(input_text)
            lang = request.form.get('lang')
            print(lang)

            global graph
            with graph.as_default():

                if lang == 'spa':

                    folder = '/' + lang
                    output_text = get_prediction(model_spa, folder, input_text)

                    if output_text:

                        language = {
                            'input': input_text,
                            'output': output_text,
                            'trans': 'to Spanish'  
                        }

                        return render_template("index.html", lang = language)

                if lang == 'fra':

                    folder = '/' + lang
                    output_text = get_prediction(model_fra, folder, input_text)

                    if output_text:

                        language = {
                            'input': input_text,
                            'output': output_text,
                            'trans': 'to French' 
                        }

                        return render_template("index.html", lang = language)

    return redirect('/', code=302)



if __name__ == "__main__":
    load_model_spa()
    load_model_fra()
    app.run(debug=True)