import pandas as pd

# Load data into a Pandas DataFrame

# Preprocess the text data
# Define a function to preprocess the text data
def preprocess_text(text):
    # Remove any punctuation
    text = ''.join(c for c in text if c.isalnum() or c.isspace())
    # Convert to lowercase
    text = text.lower()
    # Split into individual words
    words = text.split()
    # Remove any stop words (optional)
    # words = [w for w in words if w not in stop_words]
    return words

# drop Asserion, Action, Target, Value columns
def preprocess_data():
    data = pd.read_csv('../text Analyzer/ner_testing.csv')
    data = data.drop(['assertion', 'action', 'target', 'value'], axis=1)

    data['words'] = data['text'].apply(preprocess_text)
    return data



