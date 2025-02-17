from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import numpy as np

def concat(input):

    # open up test_data
    cleaned_file = open(input, "r")
    # example of d_concat_by_state when done:
      # d_concat_by_state["or"] = "all abstract associate with oregon combined here"
      # d_concat_by_state["ca"] = "all abstracts assocaited with califronai combined here"
    d_concat_by_state = {}

    # loop over cleaned test data file
    # format of each line is like: 2024,or,abstract...
    for line in cleaned_file:
        # Skip CSV titles
        if line == "Award Year,State,Abstract\n": continue 
        
        state = line[5:7]  # Extract state abbreviation
        abstract = line[8:].strip()  # Extract abstract text
        # for each state, concatenate all abstract corresponding to said state
        if state in d_concat_by_state:
            d_concat_by_state[state] += " " + abstract
        else:
            d_concat_by_state[state] = abstract
    cleaned_file.close()
    
    # Creating parallel arrays of [state, concatenated abstracts]
    state_order = []
    abstracts = []
    for state, abstract in d_concat_by_state.items():
        state_order.append(state)
        abstracts.append(abstract)
    
    return state_order, abstracts

def get_predictions(input, model, state_order):
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
    
    predictions = model.predict(validation_abstracts)
    return predictions, ground_truth

def main():
    # Load and process training data
    cleaned_data = "./data/test_data.csv"
    # returns parallel arrays: abstract[i] is all the combined abstracts corresponding to state_order[i]
    state_order, abstracts = concat(cleaned_data)
    
    # Create the pipeline with a TfidfVectorizer and Naive Bayes model
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    
    # Fit the model on the training data
    train_texts = abstracts
    # Assign a unique index to each state, this is used as the predicted classes for the model
    # ex: (1: or, 2: ca, 3: wa, ....)
    train_labels = [i for i in range(len(state_order))]
    model.fit(train_texts, train_labels)
    
    # Load and process validation data
    validation_data = "./data/validation_data.csv"
    # loop through validation data, return predictions and ground truth values
    predictions, ground_truth = get_predictions(validation_data, model, state_order)
    
    # Compute prediction accuracy
    correct = sum(p == g for p, g in zip(predictions, ground_truth))
    incorrect = len(predictions) - correct
    prediction_accuracy = correct / (correct + incorrect)
    
    print(f"Prediction accuracy: {prediction_accuracy:.2%}")

# Run the main function
main()
