
def get_prediction(model, folder, input_text):

    from sklearn.externals import joblib
    from keras.preprocessing.sequence import pad_sequences
    import numpy as np
    import os

    file_path = os.path.abspath(os.getcwd()) + "/models"

    eng_tokenizer = joblib.load(file_path + folder + '/eng_tokenizer.pkl')
    eng_length = joblib.load(file_path + folder + '/eng_length.pkl')
    targ_tokenizer = joblib.load(file_path + folder + '/targ_tokenizer.pkl')

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


def sample(args):
    
    import tensorflow as tf
    from model import Model
    import os
    from six.moves import cPickle

    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    #Use most frequent char if no prime is given
    if args.prime == '':
        args.prime = chars[0]
    model = Model(saved_args, training=False)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

            return (model.sample(sess, chars, vocab, args.n, args.prime,
                               args.sample).encode('utf-8'))

def print_text():
    import argparse

    from six import text_type

    parser = argparse.ArgumentParser(
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--save_dir', type=str, default='models/char_rnn',
                        help='model directory to store checkpointed models')
    parser.add_argument('-n', type=int, default=100,
                        help='number of characters to sample')
    parser.add_argument('--prime', type=text_type, default=u'',
                        help='prime text')
    parser.add_argument('--sample', type=int, default=2,
                        help='0 to use max at each timestep, 1 to sample at '
                            'each timestep, 2 to sample on spaces')

    args = parser.parse_args()

    new_txt = sample(args)

    return new_txt