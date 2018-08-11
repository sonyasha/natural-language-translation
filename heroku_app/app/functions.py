from sklearn.externals import joblib
import os
file_path = os.path.abspath(os.getcwd()) + "/app/models"

def prepare_model(model_name):
    
    from keras.models import model_from_json
    
    json_file = open(file_path + '/' + model_name + '/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(file_path + '/' + model_name + '/weights.h5')
    loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    return loaded_model


def get_prediction(model, folder, input_text):

    from keras.preprocessing.sequence import pad_sequences
    from numpy import argmax

    eng_tokenizer = joblib.load(file_path + folder + '/eng_tokenizer.pkl')
    eng_length = joblib.load(file_path + folder + '/eng_length.pkl')
    targ_tokenizer = joblib.load(file_path + folder + '/targ_tokenizer.pkl')

    def encode_input(input_text, tokenizer=eng_tokenizer, leng=eng_length):
        token = tokenizer.texts_to_sequences([input_text])
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
        integers = [argmax(vector) for vector in prediction]
        target = []
        for i in integers:
            word = word_for_id(i, tokenizer)
            if word is None:
                break
            target.append(word)
        return ' '.join(target)

    translation = translate(model, encode_input(input_text))

    return translation


def sample(args):
    
    import tensorflow as tf
    from app.model import Model
    from tensorflow.python import pywrap_tensorflow

    #reset everything not to raise variables exist/not exist error (crazy!)
    tf.reset_default_graph()

    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = joblib.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = joblib.load(f)
    #Use most frequent char if no prime is given
    if args.prime == '':
        args.prime = chars[0]
        
    model = Model(saved_args, training=False)

    with tf.Session() as sess:

        def get_tensors_in_checkpoint_file(file_name,all_tensors=True,tensor_name=None):
            varlist=[]
            var_value =[]
            reader = pywrap_tensorflow.NewCheckpointReader(file_name)
            if all_tensors:
                var_to_shape_map = reader.get_variable_to_shape_map()
                for key in sorted(var_to_shape_map):
                    varlist.append(key)
                    var_value.append(reader.get_tensor(key))
            else:
                varlist.append(tensor_name)
                var_value.append(reader.get_tensor(tensor_name))
            return (varlist, var_value)

        def build_tensors_in_checkpoint_file(loaded_tensors):
            full_var_list = list()
            for i, tensor_name in enumerate(loaded_tensors[0]):
                # print(tensor_name)
                try:
                    tensor_aux = tf.get_default_graph().get_tensor_by_name(tensor_name +":0")
                except:
                    print('Not found: '+ tensor_name)
                full_var_list.append(tensor_aux)
            return full_var_list

        CHECKPOINT_NAME = ('app/models/char_rnn/model.ckpt-1119')
        restored_vars  = get_tensors_in_checkpoint_file(file_name=CHECKPOINT_NAME)
        tensors_to_load = build_tensors_in_checkpoint_file(restored_vars)
        saver = tf.train.Saver(tensors_to_load)
        saver.restore(sess, CHECKPOINT_NAME)

        return (model.sample(sess, chars, vocab, args.n, args.prime, args.sample).encode('utf-8'))


def print_text():
    import argparse
    # from random import SystemRandom
    # rand = SystemRandom()

    args = argparse.Namespace()
    args.save_dir = 'app/models/char_rnn'
    args.n = 100
    # args.prime = rand.choice(l)
    args.prime = ''
    args.sample = 2

    new_txt = sample(args)

    return new_txt