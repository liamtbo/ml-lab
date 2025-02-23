from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

def get_predictions(input, vectorizer, naive_bayes, state_order):
    # loop through validation data file
    # make two parallel arrays: validation_abstracts[i] holds the abstract corresponding to state in ground_truth[i]
    validation_abstracts = []
    ground_truth = []
    with open(input, "r") as file:
        for line in file:
            if line == "Award Year,State,Abstract\n": continue  # Skip header line
            
            state = line[5:7]  # Extract state abbreviation
            # get states corrsponding index we set in state_order
            ground_truth.append(state_order.index(state)) 
            
            abstract = line[8:].strip()  # Extract abstract text
            validation_abstracts.append(abstract)

    # gets tf-idf scores for every test data, idf scores are from trained set
    validation_features = vectorizer.transform(validation_abstracts)
    predictions = naive_bayes.predict(validation_features)
    return predictions, ground_truth

def main():
    # Load and process training data
    documents_file = "./data/train_documents.csv"
    # returns parallel arrays: abstract[i] is all the combined abstracts corresponding to state_order[i]
    state_order = []
    documents = []
    with open(documents_file, "r") as file:
        for line in file:
            line = line.strip()
            state_order.append(line[:2])
            documents.append(line[3:])

    train_texts = documents
    # Assign a unique index to each state, this is used as the predicted classes for the model
    # ex: (1: or, 2: ca, 3: wa, ....)
    train_labels = [i for i in range(len(state_order))]

    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2)
    # outputs tf-idf scores
    # vectorizer also stores training set idf to be applied later in predicting test-data
    print("Getting tf-idf scores...")
    train_texts = vectorizer.fit_transform(train_texts)

    naive_bayes = MultinomialNB()
    print("Fitting Naive Bayes...")
    naive_bayes.fit(train_texts, train_labels)
    
    # Load and process validation data
    validation_data = "./data/validation_data.csv"
    # loop through validation data, return predictions and ground truth values
    print("Getting predictions...")
    predictions, ground_truth = get_predictions(validation_data, vectorizer, naive_bayes, state_order)
    
    # Compute prediction accuracy
    correct = sum(p == g for p, g in zip(predictions, ground_truth))
    incorrect = len(predictions) - correct
    prediction_accuracy = correct / (correct + incorrect)
    
    print(f"Prediction accuracy: {prediction_accuracy:.2%}")

main()
