

# returns parallel arrays: abstract[i] is all the combined abstracts corresponding to state_order[i]
def concat(input, output):
    # open up test_data
    cleaned_file = open(input, "r")
    # example of d_concat_by_state when done:
      # d_concat_by_state["or"] = "all abstract associate with oregon combined here"
      # d_concat_by_state["ca"] = "all abstracts assocaited with califronai combined here"
    d_concat_by_state = {}

    # loop over cleaned test data file
    # format of each line is like: 2024,or,abstract...
    i = 0
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
        if i % 100 == 0: print(i)
        i += 1
    cleaned_file.close()
    
    documents = open(output, "w")
    for state, abstract in d_concat_by_state.items():
        documents.write(f"{state},{abstract}\n")

    documents.close()

def main():
    # Load and process training data
    cleaned_data = "./data/train_data.csv"
    output_file = "./data/train_documents.csv"
    concat(cleaned_data, output_file)
main()