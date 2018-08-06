from flask import Flask, render_template, jsonify, redirect, send_file, request, url_for, json, session
import keras
from keras import backend as K
import os
from functions import get_prediction
from functions import print_text

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
        
        # haikus = request.form.get('haik-text')
        # print(haikus)
        # language = {
        #     'input': '',
        #     'output': '',
        #     'trans': ''  
        # }
        if request.form.get('input-text'):

            input_text = request.form["input-text"]
            print(input_text)
            lang = request.form.get('lang')
            print(lang)
            haikus = request.form['haik-text']

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

                        return render_template("index.html", lang = language, text = haikus)

                if lang == 'fra':

                    folder = '/' + lang
                    output_text = get_prediction(model_fra, folder, input_text)

                    if output_text:

                        language = {
                            'input': input_text,
                            'output': output_text,
                            'trans': 'to French' 
                        }

                        return render_template("index.html", lang = language, text = haikus)
    
    # return render_template("index.html", lang = language, text = haikus)
    return redirect('/', code=302)
    # return redirect(url_for('.index', text = texts))


@app.route('/haiku', methods=["GET","POST"])
def haiku():
    if request.method == "POST":
        
        haikus = print_text().decode("utf-8")
        input_text = request.form["eng"]
        output_text = request.form.get('other')
        # trans = request.form.get('langg')


        language = {
            'input': input_text,
            'output': output_text,
            # 'trans': trans 
        }
        

        return render_template("index.html", lang = language, text = haikus)



if __name__ == "__main__":
    load_model_spa()
    load_model_fra()
    app.run(debug=True)