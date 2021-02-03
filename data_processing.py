import pickle


def load_stopwords():
    # Used to load stop word list from local file
    print('...Stopwords loading finished...')
    fs = open('stop_words.txt', encoding='utf_8_sig')
    sw = [line.strip() for line in fs]
    fs.close()
    return sw


sw = load_stopwords()  # Load stop words


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def del_punc(t: str) -> str:
    # Used to delete punctuations in text, including special characters e.g. \n, \r...
    t = t.lower()
    punc = list("~!@#$%^&*()_+`{}|\[\]\:\";\-\\\='<>?,./") + ['\n', '\r'] + list('0123456789')
    for s in punc:
        t = t.replace(s, ' ')
    return t
