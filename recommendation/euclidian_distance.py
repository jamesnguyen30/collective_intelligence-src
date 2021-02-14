import math

def euclidian_distance(vector_a, vector_b):
    
    if len(vector_a) != len(vector_b):
        raise Exception(' vector_a and vector_b must have the same dimension')
    else:
        sum_of_square = sum( (a - b)**2 for a,b in zip(vector_a, vector_b))
        return math.sqrt(sum_of_square)