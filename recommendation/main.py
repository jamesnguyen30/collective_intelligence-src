
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
      'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
      'The Night Listener': 3.0},
     'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
      'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 3.5},
     'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
      'Superman Returns': 3.5, 'The Night Listener': 4.0},
     'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
      'The Night Listener': 4.5, 'Superman Returns': 4.0,
      'You, Me and Dupree': 2.5},
     'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 2.0},
     'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
     'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

#transformed a transformed_dictionary in recommendations.py
movies = {'Lady in the Water': {'Lisa Rose': 2.5, 'Gene Seymour': 3.0, 'Michael Phillips': 2.5,
 'Mick LaSalle': 3.0, 'Jack Matthews': 3.0}, 'Snakes on a Plane': {'Lisa Rose': 3.5,
  'Gene Seymour': 3.5, 'Michael Phillips': 3.0, 'Claudia Puig': 3.5, 'Mick LaSalle': 4.0,
   'Jack Matthews': 4.0, 'Toby': 4.5}, 'Just My Luck': {'Lisa Rose': 3.0, 'Gene Seymour': 1.5,
    'Claudia Puig': 3.0, 'Mick LaSalle': 2.0}, 'Superman Returns': {'Lisa Rose': 3.5,
     'Gene Seymour': 5.0, 'Michael Phillips': 3.5, 'Claudia Puig': 4.0, 'Mick LaSalle': 3.0,
      'Jack Matthews': 5.0, 'Toby': 4.0}, 'You, Me and Dupree': {'Lisa Rose': 2.5,
       'Gene Seymour': 3.5, 'Claudia Puig': 2.5, 'Mick LaSalle': 2.0, 'Jack Matthews': 3.5,
        'Toby': 1.0}, 'The NightListener': {'Lisa Rose': 3.0, 'Gene Seymour': 3.0,
         'Michael Phillips': 4.0, 'Claudia Puig': 4.5, 'Mick LaSalle': 3.0, 'Jack Matthews': 3.0}}


def get_critics():
    return critics

def get_movies():
    return movies
    
if __name__ == "__main__":
    pass