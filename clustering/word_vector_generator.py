import collections

def generate_word_vector(raw_text):
    #stop counting words if the character is no Latin ( a -z )
    vector = {}
    for word in raw_text.split():
        vector.setdefault(word, 0)
        vector[word]+=1
    return vector
    