import streamlit as st
import random
import matplotlib.pyplot as plt
from st_pages import Page, show_pages
import datetime

def welcome():
    return 'welcome all'

def main():
    st.title("Parent Support tool")
    st.markdown(
    """
    <div>
    <h8 style="color:black">
    Welcome to our parent support tool. It provides you with number of services related to your child’s well being. The tools are provided on the side bar menu. <br/>Please click on those you would like more information about. At present only the behavior insight tool is operational. 
    </h8>
    </div>
    """,
    unsafe_allow_html=True,
    )
    show_pages(
        [
            Page("code/Home.py", "Back to Main Menu"),
            Page("code/pages/2_Behaviors.py", "Behaviors"),
            Page("code/pages/3_Health.py", "Health"),
            Page("code/pages/4_Academic.py", "Academic"),
            Page("code/pages/5_Sleep.py", "Sleep"),
            Page("code/pages/6_Social_skills_enhancement.py", "Social Skills Enhancement"),
            Page("code/pages/7_Career_Design.py", "Career Design"),
        ]
    )
if __name__ == '__main__':
    main()
