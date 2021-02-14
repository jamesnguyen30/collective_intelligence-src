import json
import os
import errno
import pickle


def create_folder(path):
	if not os.path.exists(path):
		os.makedirs(path)
	else:
		print("Path {} already exists".format(path))

def write_dictionary_to_file(target, path, debug=False):
    json.dump(target, open(path, 'w'))
    if debug:
        print("file is written in " + path)

def pickle_object(target, path, debug=False):
    with open(path, 'wb') as file:
        pickle.dump(target, file, pickle.HIGHEST_PROTOCOL)
    if debug:
        print("Object saved as binary to path: " + path)

def pickle_load(path, debug=False):
    loaded_object = None
    with open(path, 'rb') as file:
        loaded_object = pickle.load(file)
    return loaded_object     

def read_dictionary_from_file(path):
    return json.load(open(path, 'r'))
