from .preprocessing import preprocess_text
import pandas as pd
import os

def autocomplete(text):
    # if text is empty or contains only spaces, return an empty list
    try:
        if text == '':
            return {'words': []}
        words = preprocess_text(text)
        
        datapath = os.path.join(os.path.dirname(__file__), 'ngram.csv')
        data = pd.read_csv(datapath)

        data.set_index('ngram', inplace=True)
        return {'words': data.loc[words[-1]]['next_word']} 
    except:
        print("Error")
        return {'words': []} 
