import word_vector_generator as generator
import fetch_dataset
import re
import remove_text_noise
from collective_intelligence.recommendation import file_io, recommendations
import math
import json
import pickle

_DISTANCE_DATASET_PATH = "./collective_intelligence/output/clusters/pre_calculated_distance"

class BiCluster():
    def __init__(self, right = None, left = None, id = None, vector = None, distance = None):
        self.right = right
        self.left = left
        self.id = id
        self.vector = vector
        self.distance = distance

# PASSED
def pearson_coefficient(vector_a, vector_b):

    #peason_coefficient returns [1, -1] 
    # 1 means the 2 vector are identical
    # the closer to 0 the less similiar the 2 vectors
    if len(vector_a) != len(vector_b):
        raise Exception(" Pearson Coeffcient Error: vector_a and vector_b must have the same dimensions")
    else:
        n = len(vector_a)

        sum_a = sum(vector_a)
        sum_b = sum(vector_b)

        sum_of_square_a = sum( x**2 for x in vector_a)
        sum_of_square_b = sum( x**2 for x in vector_b)

        product_sum_ab = sum( x_a * x_b for x_a, x_b in zip(vector_a, vector_b) )

        numerator = n*product_sum_ab - sum_a*sum_b
        denominator = math.sqrt( n*sum_of_square_a - (sum_a)**2) *  math.sqrt( n*sum_of_square_b - (sum_b)**2)

        return numerator / denominator

# PASSED
def pearson_coefficient_by_dict(dict_a, dict_b):
    sim = {}
    for item in dict_a:
        if item in dict_b:
            sim[item] = 1

    if len(sim)>0:
        vector_a = [ dict_a[item] for item in sim.keys()]
        vector_b = [ dict_b[item] for item in sim.keys()]

        return pearson_coefficient(vector_a, vector_b)
    else:
        return 0

def pearson_method(vector_a, vector_b):
    return 1 - pearson_coefficient_by_dict(vector_a, vector_b)



def load_word_vector_by_author(articles_dataframe):
    rows = fetch_dataset.get_rows(articles_dataframe)
    dataset = {}

    # index is the index of the first column
    for index in range(rows):

        raw_text = articles_dataframe.at[index, 'text']

        author_name = articles_dataframe.at[index, 'author']
        # process the raw text by eliminating noise ( ex: nonsense character or html link or character)
        raw_text = raw_text.lower()
        cleaned_text = remove_text_noise.remove_text_noise(raw_text)

        dataset.setdefault(author_name, {})
        dataset[author_name] = generator.generate_word_vector(cleaned_text)

    return dataset   

def calculate_distances_in_all_dataset(dataset, distance_method = pearson_method, debug = False):

    distances = {}

    authors = [ author for author in dataset.keys() ]
    
    counter = 0
    for i in range(len(authors)):
        for j in range(i+1, len(authors)):
            d = distance_method(dataset[authors[i]], dataset[authors[j]])
            distances[ (authors[i] + ',' + authors[j] )] = d

        counter +=1
        if debug:
            print("PROGRESS : {0:.2f} %".format(counter * 100 / len(authors))) 
    
    file_io.write_dictionary_to_file(distances, './collective_intelligence/output/clusters/distances')
            

def hierarchical_clustering( dataset, pre_compute_distance, distance_method = pearson_method, debug = False):
    '''
    pre_compute_distance dataset is required to run this algorithm 
    '''
    #initial clusters
    clusters = [ BiCluster(vector = dataset[author], id = author ) for author in dataset.keys() ]
    
    counter = 0
    
    while len(clusters)>1:
        # pick 2 random item in the clusters
        closest_items = (0,1)
        smallest_distance = -1
     
        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):

                #because pre_calcualted distances has a format : { "author_a,author:b" : int32 }.
                #This is format is created by the calculate_distances_in_all_dataset()
                if (clusters[i].id + ',' + clusters[j].id) in pre_compute_distance:
                    d = pre_compute_distance[ (clusters[i].id + ',' + clusters[j].id) ]
                else:
                    d = distance_method( clusters[i].vector, clusters[j].vector )
                
                if smallest_distance<d:
                    closest_items = (i, j)
                    smallest_distance = d
                
        # found the smallest distance
        # merge the 2 vectors and create a new bi_cluster
        vector_a = clusters[ closest_items[0] ].vector
        vector_b = clusters[ closest_items[1] ].vector

        merged_vector = {}

        for item in vector_a:
            if item in vector_b:
                merged_vector[item] = (vector_a[item] + vector_b[item])/2.0
            else:
                merged_vector[item] = vector_a[item]

        for item in vector_b:
            if item not in merged_vector:
                merged_vector[item] = vector_b[item]

        new_id = clusters[ closest_items[0]].id + ", " + clusters[ closest_items [1]].id
        
        new_bicluster = BiCluster(right = clusters[closest_items[0]], left = clusters[ closest_items[1] ], id = new_id, vector = merged_vector)

        try:
            del clusters[closest_items[1]]
            del clusters[closest_items[0]]
        except IndexError:
            
            raise

        clusters.append(new_bicluster)

        counter += 1 
        if debug:
            print("REMAINING {}  ".format(len(clusters) )) 

    return clusters
    

if __name__ == "__main__":
    _OUTPUT_PATH = './collective_intelligence/output/clusters/'
    
    dataset = file_io.read_dictionary_from_file(_OUTPUT_PATH + "word_count_dict")

    pre_computed_distances = file_io.read_dictionary_from_file(_OUTPUT_PATH + "distances")

    # clusterings = hierarchical_clustering(dataset, pre_computed_distances, debug= True )

    #pickle the clusterings object and store in file
    #pickle.dump(clusterings, _OUPUT_PATH + "clusterings_binary")

    clusterings = file_io.pickle_load(_OUTPUT_PATH + 'clusterings_binary')

    # file_io.write_dictionary_to_file(clusterings, _OUTPUT_PATH + "clusters")
    
    
    

    # calculate_distances_in_all_dataset(dataset, debug= True)
    # vector_a = {'a': 4, 'b':5.5, 'c':6.7}
    # vector_b = {'a': 6.8, 'b':15.5, 'c':4.7, 'd':14}


    # hierarchical_clustering(dataset)


    # dataframe = fetch_dataset.get_medium_articles_csv()

    # file_io.create_folder("./collective_intelligence/output/clusters/")
    # # load_word_vector_by_author(dataframe)
    # # word_vector = generator.generate_word_vector("James the Majesty")

    # # print(word_vector)

    # word_count_dataset = load_word_vector_by_author(dataframe)

    # article_titles = fetch_dataset.get_article_titles_from_author(dataframe)

    # authors = fetch_dataset.get_values_in_columns('author', dataframe)

    # file_io.write_dictionary_to_file(authors, "./collective_intelligence/output/clusters/author")

    # file_io.write_dictionary_to_file(word_count_dataset, "./collective_intelligence/output/clusters/word_count_dict")

    # file_io.write_dictionary_to_file( article_titles, "./collective_intelligence/output/clusters/articles")
