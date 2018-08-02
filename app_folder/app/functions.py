
def get_prediction(model, input_text):


    from sklearn.externals import joblib
    from keras.preprocessing.sequence import pad_sequences
    import numpy as np
    import os

    file_path = os.path.abspath(os.getcwd()) + "/models"

    eng_tokenizer = joblib.load(file_path + '/eng_tokenizer.pkl')
    eng_length = joblib.load(file_path + '/eng_length.pkl')
    targ_tokenizer = joblib.load(file_path + '/targ_tokenizer.pkl')


    def encode_input(input_text, tokenizer=eng_tokenizer, leng=eng_length):
        input_text = [input_text]
        token = tokenizer.texts_to_sequences(input_text)
        token = pad_sequences(token, maxlen=leng, padding='post')
        return token

    def translate(model, token):
        for i, tok in enumerate(token):
            tok = tok.reshape((1, tok.shape[0]))
            translation = predict_sequence(model, targ_tokenizer, tok)
            print(translation)
            return translation
        
    def word_for_id(integer, tokenizer):
        for word, index in tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    def predict_sequence(model, tokenizer, source):
        prediction = model.predict(source, verbose=0)[0]
        integers = [np.argmax(vector) for vector in prediction]
        target = []
        for i in integers:
            word = word_for_id(i, tokenizer)
            if word is None:
                break
            target.append(word)
        return ' '.join(target)

    translation = translate(model, encode_input(input_text))

    return translation