import streamlit as st
from models import baseline_model, prediction_model
from layout_css import expander_layout
from streamlit_extras.stylable_container import stylable_container


def run():
    st.set_page_config(layout="wide")
    expander_layout()

    # Set default language
    if '_language' not in st.session_state:
        st.session_state['_language'] = 'chinese'
    with st.container():
        col, but_col = st.columns([5, 1])
        with but_col:
            language_button = st.button('Language')
            if language_button:
                if st.session_state['_language'] == 'chinese':
                    st.session_state['_language'] = 'english'
                elif st.session_state['_language'] == 'english':
                    st.session_state['_language'] = 'chinese'

    st.header('Header')
    st.write('Content')

if __name__ == '__main__':
    run()
