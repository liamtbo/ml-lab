from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    cleaned_data = "/home/frankwoods/Desktop/lab/data/test_data.csv"
    concat_by_state = "/home/frankwoods/Desktop/lab/data/concat_by_state.csv"

    cleaned_file = open(cleaned_data, "r")
    # concat_by_state_file = open(concat_by_state, "w")
    # concat_everything_file = open(concat_everything, "w")

    d_concat_by_state = {}
    for line in cleaned_file:
        year = line[:4]
        if not year.isnumeric(): continue # skip csv titles
        state = line[5:7]
        abstract = line[8:].strip()
        if state in d_concat_by_state:
            d_concat_by_state[state] += " " + abstract
        else:
            d_concat_by_state[state] = abstract

    # creatin parallel arrays of [state, all that states abstracts concated]
    abstracts_total_concat = []
    for state, abstract in d_concat_by_state.items():
        abstracts_total_concat.append(abstract)

    # create object
    tfidf = TfidfVectorizer()
    # get tf-df values
    result = tfidf.fit_transform(abstracts_total_concat)

    """
    rows -> documents
    cols -> word indexes
    (row, col) -> tf-idf value of word in document
    """
    matrix = result.toarray()
    for document_i in range(len(matrix)):
        top_words = []
        top_words_index = []
        print()
        

main()