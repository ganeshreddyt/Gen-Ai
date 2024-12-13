import streamlit as st
from few_shots import FewShots
from post_generator import get_post
fs = FewShots()

lengths = ['Short', 'Medium', 'Long']
languages = fs.get_languages() + ['Telugu']

def main():
    st.title('Linkedin Post Generator')
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tag = st.selectbox("Title", options=fs.get_tags())
    with col2:
        selected_length = st.selectbox("Length", options=lengths)
    with col3:
        selected_language = st.selectbox("Language", options=languages)

    # generate btn
    if st.button("Generate"):
        output = get_post(selected_tag, selected_length, selected_language)
        st.write(f"{output}")
        
if __name__ == '__main__':
    main()