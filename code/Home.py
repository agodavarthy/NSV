import streamlit as st
import random
import base64
from st_pages import Page, show_pages, add_page_title
from streamlit_multipage import MultiPage

def welcome():
    return 'welcome all'
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_jpeg_as_page_bg(jpeg_file):
    #jpeg_file_ext = "jpeg"
    bin_str = get_base64_of_bin_file(jpeg_file)
    page_bg_img = '''
    <style>
    .stApp{ 
    background-image: url("data:image/jpeg;base64,%s");
    background-size: 1200px, 100px;
    background-repeat: no-repeat;

    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


def main():
    st.title("SafeSchoolNetwork")
    #st.set_page_config(
    #    initial_sidebar_state="expanded",
    #    menu_items={
    #        "Parents", "code/pages/1_Parents.py",
    #        "Teachers", "code/pages/2_Teachers.py",
    #        "Administrator", "code/pages/3_Administrator.py",
    #        "Counselor/Psychologist", "code/pages/4_Counselor_Psychologist.py",
    #        "Safety Personnel/Law Enforcement", "code/pages/5_Safety_Personnel_Law_Enforcement.py"
    #    }
    #)
    #app = MultiPage()
    #app.st = st

    #app.add_app("Parents", "code/pages/1_Parents.py")
    #app.add_app("Teachers", "code/pages/2_Teachers.py")
    #app.add_app("Administrator", "code/pages/3_Administrator.py")
    #app.add_app("Counselor/Psychologist", "code/pages/4_Counselor_Psychologist.py")
    #app.add_app("DudeSafety Personnel/Law Enforcement", "code/pages/5_Safety_Personnel_Law_Enforcement.py")

    #app.run()
    set_jpeg_as_page_bg('data/homepic.jpeg')
    st.sidebar.success("")
    show_pages(
        [
            Page("code/Home.py", "Home"),
            Page("code/pages/2_Parents.py", "Parents"),
            Page("code/pages/3_Teachers.py", "Teachers"),
            Page("code/pages/4_Administrator.py", "Administrator"),
            Page("code/pages/5_Counselor_Psychologist.py", "Counselor/Psychologist"),
            Page("code/pages/6_Safety_Personnel_Law_Enforcement.py", "Safety Personnel/Law Enforcement"),
        ]
    )


if __name__ == '__main__':
    main()
