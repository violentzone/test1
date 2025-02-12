import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from models import baseline_model, prediction_model

def run():
    # Set st.session_state which page to display
    if 'page' not in st.session_state:
        st.session_state['page'] = 'baseline_model'

    space, col1, space, col2, space = st.columns([2.2, 5, 2.5, 5, 0.5])
    with col1:
        with stylable_container(
                key="baseline_model",
                css_styles="""
                   button {
                    height:50px;
                    padding-right: 5rem;
                    padding-left: 5rem;
                    width:auto;
                    background-color: gray;
                    color: white;
                    border-radius: 20px;
                    font-size: 1.5rem;
                    margin: 4px 2px;
font-size: 16px;
                   }
                   """,
        ):
            if st.session_state['_language'] == 'chinese':
                baseline = st.button("了解現在", key='baseline')
            elif st.session_state['_language'] == 'english':
                baseline = st.button("Current status", key='baseline')
            if baseline:
                st.session_state['page'] = 'baseline_model'
    with col2:
        with stylable_container(
                key="prediction_model",
                css_styles="""
                   button {
                    height:50px;
                    padding-right: 5rem;
                    padding-left: 5rem;
                    width:auto;
                    background-color: gray;
                    color: white;
                    border-radius: 20px;
                    font-size: 1.5rem;
                    margin: 4px 2px;
                   }
                   """,
        ):
            if st.session_state['_language'] == 'chinese':
                prediction = st.button("預測未來", key='predicton')
            elif st.session_state['_language'] == 'english':
                prediction = st.button('Prediction', key='prediction')
            if prediction:
                st.session_state['page'] = 'prediction_model'

    # Identify which to show
    if st.session_state['page'] == 'baseline_model':
        if st.session_state['_language'] == 'chinese':
            baseline_model.baseline_view()
        elif st.session_state['_language'] == 'english':
            baseline_model.baseline_view_en()
    elif st.session_state['page'] == 'prediction_model':
        if st.session_state['_language'] == 'chinese':
            prediction_model.prediction_view()
        elif st.session_state['_language'] == 'english':
            prediction_model.prediction_view_en()

if __name__ == '__main__':
    with st.container():
        col, but_col = st.columns([5, 1])
        with but_col:
            language_button = st.button('Language')
            if language_button:
                if st.session_state['_language'] == 'chinese':
                    st.session_state['_language'] = 'english'
                elif st.session_state['_language'] == 'english':
                    st.session_state['_language'] = 'chinese'
    run()
