import json
import pandas as pd

class FewShots:
    def __init__(self, file_path='data/processed_data.json'):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)
        self.get_unique_tags()

    def load_posts(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            posts = json.load(file)
            self.df = pd.json_normalize(posts)
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)

    def categorize_length(self, line_count):
        if line_count <= 4:
            return 'Short'
        elif line_count <= 8:
            return 'Medium'
        return 'Long'

    def get_unique_tags(self):
        all_tags = self.df['hashtags']
        unique_tags = set(tag for tags in all_tags for tag in tags)
        self.unique_tags = list(unique_tags)

    def get_tags(self):
        return self.unique_tags

    def get_languages(self):
        return list(set(self.df['language']))

    def get_ralated_posts(self, category, length, language):
        df_filtered = self.df[
                (self.df['hashtags'].apply(lambda tags: category in tags)) &
                (self.df['length'] == length) &
                (self.df['language'] == language)
              ]
        return df_filtered.to_dict(orient='records')

if __name__ == '__main__':
    fs = FewShots()
    relates_posts = fs.get_ralated_posts('Agriculture Technology', 'Long', 'English')
    print(fs.get_tags())
