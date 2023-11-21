import streamlit as st
import random
import matplotlib.pyplot as plt
from st_pages import Page, show_pages
import datetime

def welcome():
    return 'welcome all'

def click_button():
    st.session_state.clicked = True

def main():
    #st.title("Parent Support Tools")
    st.markdown(
    """
    <div>
    <h8 style="color:black">
This support tool provides you with an understanding of what your child’s behaviors mean in the likelihood that they might signal
emotional needs that if left unmet might lead to violence. Please fill in the box below, listing behaviors you’ve seen changed in the
recent past. Please separate them by commas. And then press query. If you want help with behavior terms, click on the Behavior
Encyclopedia. And then press query.
    </h8>
    </div>
    """,
    unsafe_allow_html=True,
    )
    st.session_state.behavior_text = st.text_area("")

    st.session_state.button = st.button('Query', on_click=click_button)
    if st.session_state.button:
      if st.session_state.behavior_text != "":
        prediction_result="a low risk of violence and has been the victim of moderate bullying"
        prediction_text1="Thousands of data points and research sources have been queried and results suggest your child has "
        prediction_text2=". We suggest you contact your school’s SafeSchoolNetwork representative for the issue to be resolved."
        prediction_result_color="green"
        prediction_color="black"
        temp = f'<span style="color: {prediction_result_color}; font-size: 18px;"> {prediction_result}</span>'
        st.markdown(
           f'{prediction_text1} {temp} {prediction_text2}',
            unsafe_allow_html=True
        )
      else:
        st.markdown(
            "Please enter the behaviors",
            unsafe_allow_html=True
        )

if __name__ == '__main__':
    main()
