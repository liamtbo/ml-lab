Running the model
    start up python virtual environment
        source myenv/bin/activate 
    run model code
        $python3 concat_and_sum.py
concat_and_sum.py
    this file is where the model is trained and ran
/data
    this is where the cleaned train, test, and validation data can be found
parse_clean.py
    this file is for cleaning up data which has already been done

Multinomail naive bayes
    Naive Bayes doesn't distinguish between raw word frequencies or TF-IDF scores—it simply treats whatever is provided as features (typically word counts or weights).
    TF-IDF scores work well in this context because they give more weight to rarer or more unique terms, making those words more informative for classification.

    running testing data
        the tf of a single test data is combined with the idf score of the
        entire training corpus to get that documents td-idf scores. This is then used
        to classify it 
