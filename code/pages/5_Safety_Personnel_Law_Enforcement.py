import streamlit as st
import random
import matplotlib.pyplot as plt
import datetime

def welcome():
    return 'welcome all'

def main():
    #st.set_page_config(page_title = "Safety Personnel/Law Enforcement")
    st.sidebar.markdown("Safety Personnel/Law Enforcement")
    st.title("School Risk Assessment Form")

    st.markdown(
    """
    <div style="background-color:gray">
    <h6 style="color:black">
    Please fill in this form so your school and your community can be compared to the 1,558 schools and communities having experienced a school shooting or violence preceding a shooting. This comparsion will provide both a detailed risk percentage by data category as well as an overall percentile ranking. Once specific vulnerables are identfied, you will be provided with options to lessen or remove those vulnerabilities.
    </h6>
    </div>
    """,
    unsafe_allow_html=True,
    )
    st.markdown(
	"""<h1>Counselors Form</h1>""", 
	
	unsafe_allow_html=True)


if __name__ == '__main__':
    main()
