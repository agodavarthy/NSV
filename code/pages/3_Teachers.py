import streamlit as st
import random
import matplotlib.pyplot as plt
from st_pages import Page, show_pages
import datetime
from /utils import image

def welcome():
    return 'welcome all'
def main():
    st.title("Teacher Support tool")
    pointing_img = image.img_to_html("data/lfp_trans.jpeg")
    st.markdown(
    f'<p style={"display:inline-block"}>Welcome to our teacher support tool. It provides you with number of services related to your child’s well being. Please click on those you would like more information about. At present only the behavior insight tool is operational. The tools are provided in the side bar menu {pointing_img}</p>',
    unsafe_allow_html=True,
    )
    show_pages([
        Page("code/Home.py", "Back to Main Menu"),
        Page("code/pages/7_Behaviors.py", "Behaviors"),
    ])
 
if __name__ == '__main__':
    main()
