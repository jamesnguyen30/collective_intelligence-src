import sys
sys.path.append("./")
import remove_text_noise, fetch_dataset, word_vector_generator
from collective_intelligence.recommendation import file_io
import hierarchical_clustering 

_OUTPUT_PATH = './collective_intelligence/output/clusters/'

def load_word_vectors_by_title(article_dataframe):
    rows = fetch_dataset.get_rows(article_dataframe)
    dataset = {}

    for index in range(rows):
        
        raw_text = article_dataframe.at[index, 'text']
        title = article_dataframe.at[index, 'title']

        raw_text = raw_text.lower()
        remmoved_common_words_text = remove_text_noise.remove_common_words(raw_text)
        cleaned_text = remove_text_noise.remove_text_noise(remmoved_common_words_text)

        dataset.setdefault(title, {})
        dataset[title] = word_vector_generator.generate_word_vector(cleaned_text)

    return dataset

if __name__ == "__main__":
    # dataset = file_io.read_dictionary_from_file(_OUTPUT_PATH + "word_count_dict")
    dataframe = fetch_dataset.get_medium_articles_csv()
    dataset = load_word_vectors_by_title(dataframe)

    file_io.write_dictionary_to_file(dataset, _OUTPUT_PATH + 'word_count_author_dict')