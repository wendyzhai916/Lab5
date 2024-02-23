import re
import pandas as pd

def remove_html_tags(text):
    """
    Removes HTML tags from the given text.
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_special_characters(text, remove_digits=False):
    """
    Removes special characters from the given text. Optionally, removes digits.
    """
    pattern = r'[^a-zA-Z0-9\s]' if not remove_digits else r'[^a-zA-Z\s]'
    text = re.sub(pattern, '', text)
    return text

def preprocess_data(data_frame):
    """
    Preprocesses the given DataFrame by cleaning text columns.
    """
    for column in data_frame.columns:
        # Assuming all columns are of type string; adjust logic if not.
        data_frame[column] = data_frame[column].apply(lambda x: remove_html_tags(x))
        data_frame[column] = data_frame[column].apply(lambda x: remove_special_characters(x))
        # Replace missing values with a placeholder
        data_frame[column] = data_frame[column].fillna('N/A')
    return data_frame

def main():
    data = {'api_number': ['123', '456', '<html>789</html>'], 
            'well_name': ['Well A', 'Well B', 'Well <b>C</b>']}
    df = pd.DataFrame(data)
    
    print("Before preprocessing:")
    print(df)
    
    # Preprocess the DataFrame
    preprocessed_df = preprocess_data(df)
    
    print("\nAfter preprocessing:")
    print(preprocessed_df)

if __name__ == "__main__":
    main()
