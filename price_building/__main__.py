
import math
from random import random, randint
import sys
sys.path.append("./")
from collective_intelligence.recommendation import euclidian_distance
from collective_intelligence.recommendation import file_io

_OUTPUT_PATH = "./collective_intelligence/price_building/output/price_data"
def wineprice(rating,age):
      peak_age=rating-50
      # Calculate price based on rating
      price=rating/2
      if age>peak_age:
        # Past its peak, goes bad in 5 years
        price=price*(5-(age-peak_age))
      else:
        # Increases to 5x original value as it
        # approaches its peak
        price=price*(5*((age+1)/peak_age))
      if price<0: price=0
      return price


def wineset1(): 
    rows=[]
    for _ in range(500):
        # Create a random age and rating 
        rating=random( )*50+50 
        age=random( )*50
        # Get reference price
        price=wineprice(rating,age)
        # Add some noise 
        price*=(random( )*0.4+0.8)
        # Add to the dataset
        rows.append({'input':(rating,age),
                        'result':price})
    return rows

if __name__ == "__main__":
    # dataset = wineset1()
    dataset = file_io.read_dictionary_from_file(_OUTPUT_PATH)
    