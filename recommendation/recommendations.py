import math
import euclidian_distance as eu_distance
import main
import file_io


def similarity_score_distance( dataset, item_a, item_b ):
    ''' dataset format = dict { string: dict }, item_a and item_b are string
        returns [1. 0) : 1 means the same
    ''' 

    sim = {}

    for item in dataset[item_a]:
        if item in dataset[item_b]:
            sim[item] = 1
    
    if len(sim) == 0:
        return 0
    else:
        point_a = [ dataset[item_a][item] for item in sim ]
        point_b = [ dataset[item_b][item] for item in sim ] 

        return 1 / ( 1 + eu_distance(point_a, point_b))

# DEPRECATED, DO NOT USE 
def pearson_coefficient(dataset, item_a, item_b):
    ''' dataset format = dict { string: dict }, item_a and item_b are string
        returns [1, -1) : 1 means the same
    ''' 

    sim = {}

    for item in dataset[item_a]:
        if item in dataset[item_b]:
            sim[item] = 1
    
    n = len(sim)

    if n!=0:
        
        sum_a = sum( dataset[item_a][item] for item in sim)
        sum_b = sum( dataset[item_b][item] for item in sim)

        sum_of_square_a = sum( dataset[item_a][item]**2 for item in sim)
        sum_of_square_b = sum( dataset[item_b][item]**2 for item in sim)
    
        product_sum_ab = sum( dataset[item_a][item] * dataset[item_b][item] for item in sim)

        numerator = n*product_sum_ab - sum_a*sum_b
        denominator = math.sqrt( n*sum_of_square_a - (sum_a)**2) *  math.sqrt( n*sum_of_square_b - (sum_b)**2)

        if denominator!=0:
            return numerator / denominator
        else :
            return 0
    else:
        return 0
        
def top_matches(dataset, item, n = 5, similarity = pearson_coefficient):
    
    scores = [ ( similarity( dataset, item, compare_item), compare_item) for compare_item in dataset if item!=compare_item ]
    scores.sort()
    scores.reverse()
    scores[:n]

    return scores

def get_recommendations(dataset, item, similarity = pearson_coefficient):
    
    totals = {}
    similiarty_sums = {}

    for other in dataset:
        if other!=item:
            sim_score = similarity(dataset, item, other)
            
            if sim_score!=0:
                for sub_item in dataset[other]:
                    if sub_item not in dataset[item] or dataset[item][sub_item] == 0:
                        totals.setdefault(sub_item,0)
                        totals[sub_item] += sim_score * dataset[other][sub_item]

                        similiarty_sums.setdefault(sub_item,0)
                        similiarty_sums[sub_item] += sim_score
                    else:
                        continue
            else:
                continue
        else:
            continue
    
    rankings = [ ( total / similiarty_sums[n_item], n_item) for n_item, total in totals.items()]
    rankings.sort()
    rankings.reverse()

    print(rankings)

def flip_dictionary(dictionary):

    new_dictionary = {}

    for item in dictionary:
        for sub_item in dictionary[item]:
            new_dictionary.setdefault(sub_item, {})
            new_dictionary[sub_item][item] = dictionary[item][sub_item]
    
    return new_dictionary

def build_item_similiarity_dataset(dataset, n = 10, progress_update = True, similiarity = pearson_coefficient):
    results = {}

    #for progress update only
    count = 0
    total = len(dataset)
    # print progress for every 10%
    report_mark = int(total * 10 / 100)

    #prevent zero
    if report_mark ==0 :
        report_mark = 1

    for item in dataset:
        count+=1
        results[item] = top_matches(dataset, item, similarity=pearson_coefficient)
        if progress_update and count % report_mark == 0:
            print( "{0:.2f} %".format(count/total * 100.0))

    return results

def item_based_recommendation(dataset, similiar_item_dataset, item):
    item_values = dataset[item]
    totals_product = {}
    similiarity_sums = {}

    for (item, value) in item_values.items():
        for (similiarity_score, similiar_item) in similiar_item_dataset[item]:
           totals_product.setdefault(similiar_item, 0)
           totals_product[similiar_item] += value * similiarity_score

           similiarity_sums.setdefault(similiar_item,0)
           similiarity_sums[similiar_item] += similiarity_score

    results =[ (totals_product[n_item] / similiarity_sums[n_item], n_item) for n_item in totals_product ]
    results.sort()
    results.reverse()

    print(results)

if __name__ == "__main__":

    dataset = main.get_critics()

    transformed_dataset = main.get_movies()

    file_io.create_folder('./collective_intelligence/output/recommendations')

    file_io.write_dictionary_to_file(dataset, path = "./collective_intelligence/output/recommendations/critics")

    file_io.write_dictionary_to_file(transformed_dataset, path = "./collective_intelligence/output/recommendations/movies")

    sim_score = similarity_score_distance(dataset, 'Lisa Rose', 'Gene Seymour')
    
    print("distance similarity = " + str(sim_score))

    pearson_co = pearson_coefficient(dataset,  'Lisa Rose', 'Gene Seymour')

    print("pearson coefficient = " + str(pearson_co))

    print("top_matches: \n" + str(top_matches(dataset, 'Toby')))

    # Get Movie recommendations for Toby based on other similiar revieweres
    get_recommendations(dataset, 'Toby')

    print(transformed_dataset)

    print("flipped top matches : " + str(top_matches(transformed_dataset, 'Superman Returns')))

    # Get Reviewer recommendation for Just My Luck based on other similiar movies
    get_recommendations(transformed_dataset, 'Just My Luck')

    # Build a similiar_item dataset for item-based recommendation
    item_similiarity_dataset = build_item_similiarity_dataset(transformed_dataset)
    
    file_io.write_dictionary_to_file(transformed_dataset, path = "./output/recommendations/transformed")

    file_io.write_dictionary_to_file(item_similiarity_dataset, path = "./collective_intelligence/output/recommendations/item_similiarity_dataset")

    item_based_recommendation(dataset, item_similiarity_dataset, 'Toby')