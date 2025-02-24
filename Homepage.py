import streamlit as st
from models import baseline_model, prediction_model
from layout_css import expander_layout
from streamlit_extras.stylable_container import stylable_container

if '_language' not in st.session_state:
    st.session_state['_language'] = 'chinese'


def home_content():
    """
    Type your CHINESE homepage here
    """
    st.header('這是標題')
    st.write('這是內容')


def home_content_en():
    """
     Type your ENGLISH homepage here
    """
    st.header('This is header')
    st.write('This is content')


def run():
    st.set_page_config(layout="wide")
    expander_layout()

    # Set default language
    if '_language' not in st.session_state:
        st.session_state['_language'] = 'chinese'

    with st.container():
        col, but_col = st.columns([5, 1])
        with but_col:
            language_button = st.selectbox('Language/語言', ['繁體中文', 'English'])
            if language_button == '繁體中文':
                st.session_state['_language'] = 'chinese'
            elif language_button == 'English':
                st.session_state['_language'] = 'english'

    if st.session_state['_language'] == 'chinese':
        home_content()
    elif st.session_state['_language'] == 'english':
        home_content_en()
    else:
        st.session_state['_language'] = 'chinese'
        st.experimental_rerun()


if __name__ == '__main__':
    run()
