import streamlit as st
import random
import base64
from st-pages import Page, show_pages, add_page_title

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

    set_jpeg_as_page_bg('data/homepic.jpeg')
    #st.sidebar.success("")
    show_pages(
        [
            Page("code/pages/1_Parents.py", "Parents"),
            Page("code/pages/2_Teachers.py", "Teachers"),
            Page("code/pages/3_Administrator.py", "Administrator"),
            Page("code/pages/4_Counselor_Psychologist.py", "Counselor/Psychologist"),
            Page("code/pages/5_Safety_Personnel_Law_Enforcement.py", "Safety Personnel/Law Enforcement"),
        ]
    )


if __name__ == '__main__':
    main()
