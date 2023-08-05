from collections import defaultdict
from .preprocessing import preprocess_text



    # Define a function to build the n-gram model
def build_ngram_model(data, n=2):
    # Initialize a defaultdict to store the n-grams
    ngrams = defaultdict(list)
    
    # Loop through each row in the data
    for i, row in data.iterrows():
        # Get the list of words in the row
        words = row['words']
        
        # Loop through each 2-gram in the row and add it to the defaultdict 
        # Build the 2-gram model by adding word and its next word to the dictionary
        for j in range(len(words) - n + 1):
            ngram = ' '.join(words[j:j+n-1])
            next_word = words[j+n-1]
            ngrams[ngram].append(next_word)
    
    return ngrams


# Define a function to generate autocomplete suggestions
def suggest_words(text, ngrams, n=2):
    # Preprocess the text
    words = preprocess_text(text)
    
    # Get the most common next words for the 2-gram
    ngram = ' '.join(words[-n+1:]) if len(words) >= n else ''
    # print(ngram)
    if ngram in ngrams:
        next_words = ngrams[ngram]
        suggestions = sorted(set(next_words), key=next_words.count, reverse=True)
    else:
        suggestions = []
    
    return suggestions