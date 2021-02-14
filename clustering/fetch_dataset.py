import sys
import os
import pandas as pd

WORKSPACE_PATH = os.getcwd()
ARTICLES_DATASET_PATH = WORKSPACE_PATH + "/dataset/medium_article/"

sys.path.append("./")

def get_medium_articles_csv():
    dataframe = pd.read_csv(ARTICLES_DATASET_PATH + "articles.csv")
    return dataframe

def get_values_in_columns(name, dataframe):
    values = dataframe[name].tolist()
    return values

def get_article_titles_from_author(dataframe):
    result = {}
    authors = get_values_in_columns('author', dataframe)
    titles = get_values_in_columns('title', dataframe)
    for author,title in zip(authors, titles):
        result[author] = title
    return result

def get_rows(dataframe):
    return dataframe.shape[0]

def get_cols(dataframe):
    return dataframe.shape[1]

# if __name__ == "__main__":
    # dataframe = get_medium_articles_csv()
    # print(dataframe.shape) #rows x cols
    # print(dataframe.at[0, 'text']) #get cell at first row, 'text' column
    # get_values_in_columns('author', dataframe)
