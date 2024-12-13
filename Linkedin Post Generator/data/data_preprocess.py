import json
from textwrap import indent

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

# preprocess data
def preprocess_data():
    with open('LinkedIn posts.json', 'r', encoding='utf-8') as file:
        raw_posts = json.load(file)
    posts = [{'post_text': item['post_text']} for item in raw_posts]

    enriched_data = []
    for post in posts:
        metadata = get_metadata(post['post_text'])
        print(metadata)
        enriched_post = post | metadata
        enriched_data.append(enriched_post)
        if len(enriched_data) > 49:  # total posts are 1000, I took sample of 50 posts
            break

    # dump cleaned posts
    with open('processed_data.json', 'w', encoding='utf-8') as out_file:
        json.dump(enriched_data, out_file, indent=4)

# get metadata from llm
def get_metadata(post):
    prompt = '''
        You are provided with a LinkedIn `post_text`. Perform the following tasks:  

        1. Count the number of lines in the given `post_text`.  
        2. If there are no hashtags at the end of the post, generate 3 to 4 relevant and meaningful hashtags based on the content of the post.  
        3. Format the hashtags as follows:  
            - All hashtags should be a list of strings without the `#` symbol at the beginning.  
            - Each hashtag should follow the capitalized case (e.g., "Job Search" instead of "JOB SEARCH" or "job search").  
            - If a hashtag contains multiple words, segment it into meaningful words, and ensure each word starts with a capital letter (e.g., `capitalraising` → `Capital Raising`).  
        4. If hashtags are already present at the end, remove all hashtags from the end of the `post_text`.  
        5. Detect the language of the post and provide the full name of the language (e.g., "English" instead of "en").  

        Note: Return the result as a valid JSON object only. Do not include any additional text, headers, or explanations(No preamble)
         eg: `line_count`: 4
             `language`: `English`
             `hashtags`: [.....]
        Note: Never give any extra text
        Here is the actual post on which you need to perform this task:  
        {post_text}
        '''
    pt = PromptTemplate.from_template(prompt)
    chain = pt | llm
    response = chain.invoke(input={'post_text': post})

    # handle edge cases
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException('Cant parse data was too large!')

    # finally return metadata
    return res

# main method
if __name__ == '__main__':

    preprocess_data()



















# frame hashtags clean and meaningful
# from wordsegment import load, segment
# load()
# for item in data:
#     hashtags = item['hashtags']
#     enriched_hashtags = []
#     if hashtags:
#         enriched_hashtags = [
#             ' '.join(word.capitalize() for word in segment(hashtag.lstrip('#'))) for hashtag in hashtags]
#     item['hashtags'] = enriched_hashtags
#
# # handling the empty hashtag objects
# all_tags = ['Digital', 'Mindful Leadership', 'Resilience', 'Teamwork', 'Passion', 'Workout', 'Entrepreneur',
#             'Manufacturing', 'Job Search', 'Scam']
# import random
# for item in data:
#     if item['hashtags'] == []:
#         rand_idx1 = random.randint(0, len(all_tags)-1)
#         rand_idx2 = rand_idx1 - 1
#         new_hashtags = [all_tags[rand_idx1], all_tags[rand_idx2]]
#         item['hashtags'] = new_hashtags
#
#     # handle the line count
#     item['line_count'] = item['post_text'].count('.')
#
# for item in data:
#     print(item['post_text'], item['hashtags'])

