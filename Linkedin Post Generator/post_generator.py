from llm_helper import llm
from few_shots import FewShots
fs = FewShots()

def get_str_length(len):
    if len == 'Short':
        return '1 to 5 lines'
    elif len == 'Medium':
        return '5 to 10 lines'
    return '10 to 15 lines'

def get_prompt(tag, length, language):
    length_str = get_str_length(length)
    prompt = f'''
        Generate a LinkedIn post using the below information. No preamble.

        1) Topic: {tag}
        2) Length: {length_str}
        3) Language: {language}
        The script for the generated post should always be English except for Telugu.
        '''

    sample_posts = fs.get_ralated_posts(tag, length, language)

    if len(sample_posts) > 0:
        prompt += 'Note: Use the writing style as per the following examples.'

        for i, post in enumerate(sample_posts):
            prompt += f"\n\n Example: {i+1} \n\n {post['post_text']}"
            if i == 2:
                break

    prompt += "Don't add any extra text at beginning or end, Just valid is enough."
    return prompt


def get_post(tag, length, language):
    prompt = get_prompt(tag, length, language)
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    print(get_post("Job Search", "Short", "English"))


