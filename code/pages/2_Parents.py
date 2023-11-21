import streamlit as st
import random
from st_pages import Page, show_pages
import datetime
from utils import image

def welcome():
    return 'welcome all'
    return img_html
def main():
    st.title("Parent Support tool")
    pointing_img = image.img_to_html("data/lfp_trans.jpeg") 
    st.markdown(
    f'<p style={"display:inline-block"}>Welcome to our parent support tool. It provides you with number of services related to your child’s well being. Please click on those you would like more information about. At present only the behavior insight tool is operational. The tools are provided in the side bar menu {pointing_img}</p>',
    unsafe_allow_html=True,
    )
    show_pages(
        [
            Page("code/Home.py", "Back to Main Menu"),
            Page("code/pages/7_Behaviors.py", "Behaviors"),
            Page("code/pages/8_Health.py", "Health"),
            Page("code/pages/9_Academic.py", "Academic"),
            Page("code/pages/10_Sleep.py", "Sleep"),
            Page("code/pages/11_Social_skills_enhancement.py", "Social Skills Enhancement"),
            Page("code/pages/12_Career_Design.py", "Career Design"),
        ]
    )
if __name__ == '__main__':
    main()
