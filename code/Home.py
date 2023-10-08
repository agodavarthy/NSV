import streamlit as st
import random
import base64

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
    background-size: 1800px, 800px;
    background-repeat: no-repeat;

    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


def main():
    st.title("SafeSchoolNetwork")

    set_jpeg_as_page_bg('../data/classroom.jpeg')
    #st.sidebar.success("")

if __name__ == '__main__':
    main()
