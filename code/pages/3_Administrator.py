import streamlit as st
import random
import datetime
import pandas as pd
import numpy as np
import math
import swb_noschoolviolence_analysis as swb


#import SessionState

def welcome():
    return 'welcome all'

def read_samples(filename):
    sample_file = pd.read_csv(filename)
    return sample_file
    
def prediction(school_level_type, school_address_zip, num_teachers, num_psych_couns, num_enrolled_students, num_violent_events_total, num_suicide_events, num_times_guns_brought_school, num_bullying_occurrences, school_hours_and_reported_provocation, sporting_event, nearby_school):
    school_level_num = {'Elementary': 1, 'Middle School': 2, 'High School': 3}
    #rand_num = random.uniform(0, 1)
    rand_num = 0.1

    risk_factor = 1
    epsilon = 0.0001
    if num_bullying_occurrences == 0:
        num_bullying_occurrences = epsilon 
    if num_violent_events_total == 0:
        num_violent_events_total = epsilon 
    if num_times_guns_brought_school == 0:
        num_times_guns_brought_school = epsilon 
    num_provocations = school_hours_and_reported_provocation + sporting_event + nearby_school
    if num_provocations == 0:
        num_provocations = epsilon

    risk_factor = school_level_num[school_level_type] * num_provocations * num_bullying_occurrences*num_violent_events_total*num_times_guns_brought_school*((num_teachers/num_enrolled_students)+(num_psych_couns/num_enrolled_students))
    
    risk_factor = math.log(risk_factor)
    
    #total_risk_factor = rand_num * risk_factor 
    total_risk_factor = risk_factor * (1/10)
    print("Total Risk Factor = ", total_risk_factor)
    if total_risk_factor < 0.3:
        prediction_result = "Low vulnerability index - keep up the good work"
        prediction_color = "green"  # Color for a positive result
    elif total_risk_factor >= 0.3 and total_risk_factor < 0.8:
        prediction_result = "Moderate vulnerability index - close vigilance needed"
        prediction_color = "orange"  # Color for a negative result

    else:
        prediction_result = "High vulnerability index - immediate corrective action required"
        prediction_color = "red"  # Color for a negative result

    return prediction_result, prediction_color

def buildDict(df, row_id):
    row_dic = {}
    colnames = df.columns
    for col in colnames:
        row_dic[col] = df.loc[row_id].at[col]
    return row_dic

def click_button():
    st.session_state.clicked = True
    
def fillup(row_vals, geo_lookup, risk_factor_lookup):

    states = geo_lookup["STATE"].unique()
    states = np.insert(states, 0, "select a state", axis=0)

    st.title("School Risk Assessment Form")
    st.markdown("""<br>""", unsafe_allow_html=True)
    st.markdown(
    """
    <div>
    <h8 style="color:black">
    Please fill in this form so your school and your community can be compared to the 14,232 schools and communities having experienced a school shooting or violence preceding a shooting. This comparsion will provide both a detailed risk percentage by data category as well as an overall percentile ranking. Once specific vulnerables are identfied, you will be provided with options to lessen or remove those vulnerabilities.
    </h8>
    </div>
    """,
    unsafe_allow_html=True,
    )
    #st.markdown(nsv_caption, unsafe_allow_html=True)

    st.session_state.state = ""
    if row_vals["state"]:
       st.session_state.state = row_vals["state"]
    st.session_state.state = st.selectbox("School State", states, )

    #county = geo_lookup["COUNTY"].groupby(st.session_state.state).unique()
    county = geo_lookup.query("STATE==@st.session_state.state")["COUNTY"].unique()
    county = np.insert(county, 0, "select a county", axis=0)
    st.session_state.county = ""
    if row_vals["county"]:
       st.session_state.county = row_vals["county"]
    st.session_state.county= st.selectbox("School County", county)

    school_type_lst = ["", "Elementary", "Middle School", "High School"]
    school_type_ind = school_type_lst.index(row_vals["school_level_type"])
    st.session_state.school_level_type = st.selectbox("School Level/Type", school_type_lst, school_type_ind)
    zip_code = str(row_vals["school_address_zip"])
    if len(zip_code) < 5:
        while len(zip_code) < 5:
            zip_code = "0" + zip_code
        st.session_state.school_address_zip = st.text_input("School Zip Code*", zip_code)
    else:       
        st.session_state.school_address_zip = st.text_input("School Zip Code*", row_vals["school_address_zip"])

    st.write("Hours of Operation")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.hours_oper_from = st.time_input("From", datetime.time())
        #hours_oper_from = st.time_input("From", row_vals["hours_oper_from"])
    with col2:
        st.session_state.hours_oper_to = st.time_input("To", datetime.time())
        #hours_oper_from = st.time_input("From", row_vals["hours_oper_to"])


    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.write("Number of Staff")
    col1, col2 = st.columns(2)
    with col1:
            st.session_state.num_teachers = st.number_input("Teachers", min_value=1, value=row_vals["num_teachers"])
            #num_psych_couns= st.number_input("Psychologists/Counselors (FT/PT)", value=row_vals["num_psych_couns"])
            st.session_state.num_psych_couns= st.number_input("Psychologists/Counselors (FT/PT)", value=0)
            st.session_state.num_other_staff = st.number_input("Other", value=row_vals["num_other_staff"])

    with col2:
            st.session_state.num_admin = st.number_input("Admin", value=row_vals["num_admin"])
            st.session_state.num_safety_resources = st.number_input("Safety Resources", value=row_vals["num_safety_resources"])

    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.session_state.num_enrolled_students = st.number_input("Student Enrollment Number", value=row_vals["num_enrolled_students"])
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.num_male_students = st.number_input("% Male_Students", value=row_vals["num_male_students"])
        st.session_state.identifying_differently = st.number_input("% Identifying Differently", value=row_vals["identifying_differently"])
    with col2:
        st.session_state.num_female_students= st.number_input("% Female Students", value=row_vals["num_female_students"])

    st.write("Age Range of Student Body")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.min_age= st.number_input("Min Age", min_value=3, max_value=99, value=3)
    with col2:
        st.session_state.max_age = st.number_input("Max Age", min_value=3, max_value=99, value=3)
    st.markdown("""<hr>""", unsafe_allow_html=True)

    st.write("Percentage by Enthnicity")
    col1, col2 = st.columns(2)
    with col1:
            st.session_state.american_indian_alaska_native = st.number_input("American Indian or Alaska Native", value=row_vals["american_indian_alaska_native"])
            st.session_state.hispanic_latino = st.number_input("Hispanic or Latino", value=row_vals["hispanic_latino"])
            st.session_state.asian = st.number_input("Asian", value=row_vals["asian"])
    with col2:
            st.session_state.black_african_american = st.number_input("Black or African American", value=row_vals["black_african_american"])
            st.session_state.white = st.number_input("White", value=row_vals["white"])
            st.session_state.native_hawaiian_other_pacific_islander = st.number_input("Native Hawaiian or Pacific Islander", value=row_vals["native_hawaiian_other_pacific_islander"])

    st.markdown("""<hr>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
            st.session_state.num_bullying_occurrences = st.number_input("Number of Bullying Occurrences",min_value=0, value=row_vals["num_bullying_occurrences"])

            st.session_state.num_suicide_events = st.number_input("Number of Suicide Events", min_value=0, value=row_vals["num_suicide_events"])

    with col2:
            st.session_state.num_times_guns_brought_school = st.number_input("Number of Times Guns Were Brought to School",min_value=0, value=row_vals["num_times_guns_brought_school"])

            st.session_state.num_violent_events_total = st.number_input("Number of Violent Events Total",min_value=0, value=row_vals["num_violent_events_total"])

    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.write("Number of Violent Events (Location)")
    col1, col2 = st.columns(2)
    with col1:
            st.session_state.school_hours_and_reported_provocation = st.number_input("School Hours and reported provocation (ie. Escalation of dispute, racial, targeted victim)", min_value=0, value=row_vals["school_hours_and_reported_provocation"])
            st.session_state.sporting_event = st.number_input("Sporting Event", min_value=0, value=row_vals["sporting_event"])
    with col2:
            st.session_state.nearby_school = st.number_input("Nearby School", min_value=0, value=row_vals["nearby_school"])

    st.markdown("""<hr>""", unsafe_allow_html=True)

    st.write("Has media reported on any violent event at your school?")
    col1, col2 = st.columns(2)
    with col1:
            st.session_state.media_when = st.text_input("When", "")
            st.session_state.media_type = st.text_input("Media Type", "")
            #media_when = st.text_input("When", row_vals["media_when"])
            #media_type = st.text_input("Media Type", row_vals["media_type"])
    with col2:
            st.session_state.how_many_times = st.number_input("How many times?", min_value=0,value=0)
            st.session_state.dates_of_reports = st.text_input("Dates of reports?", "")
            #how_many_times = st.number_input("How many times?", min_value=0,value=row_vals["how_many_times"])
            #dates_of_reports = st.text_input("Dates of reports?", row_vals["dates_of_reports"])
    result = ""

    st.session_state.button = st.button('Query', on_click=click_button)
    if st.session_state.button:
        #prediction_result, prediction_color = prediction(st.session_state.school_level_type, st.session_state.school_address_zip, st.session_state.num_teachers, st.session_state.num_psych_couns, st.session_state.num_enrolled_students, st.session_state.num_violent_events_total, st.session_state.num_suicide_events, st.session_state.num_times_guns_brought_school, st.session_state.num_bullying_occurrences, st.session_state.school_hours_and_reported_provocation, st.session_state.sporting_event, st.session_state.nearby_school)
        risk_levels = swb.geo_risk_lookup(county=st.session_state.county, state=st.session_state.state, geo_lookup=geo_lookup, risk_factor_lookup=risk_factor_lookup)
        print(type(risk_levels))
        print(risk_levels.iloc[0]["violance occurance rate"])
        print(risk_levels.iloc[0]["risk_level"])
        total_risk_factor = risk_levels.iloc[0]["risk_level"] 
        if total_risk_factor =="low" or total_risk_factor == "very low":
            prediction_result = "Low vulnerability indication - keep up the good work"
            prediction_color = "green"  # Color for a positive result
        elif total_risk_factor == "medium":
            prediction_result = "Moderate vulnerability indication - Recommended Solutions"
            prediction_color = "orange"  # Color for a negative result
        elif total_risk_factor == "high":
            prediction_result = "High vulnerability indication - Recommended Solutions"
            prediction_color = "red"  # Color for a negative result
        else:
            prediction_result = "Invalid county info not available"
            prediction_color = "black"  # Color for a negative result

        #st.session_state.inference_text =  st.text("", "")
        #st.markdown(
        #"""
        #f'<p style="color: {prediction_color}; font-size: 18px;"> {prediction_result}</p>'
        #""",
        #unsafe_allow_html=True,
        #)
		#st.text(f'<p style="color: {prediction_color}; font-size: 18px;"> {prediction_result}</p>')
        st.markdown(
           f'<p style="color: {prediction_color}; font-size: 18px;"> {prediction_result}</p>',
            unsafe_allow_html=True
        )
        st.session_state.button = False
        #st.session_state.inference_text = " "
        #st.inference("")
        
    st.markdown(
    """
    <div>
    <h8 style="color:black">
    *Zip Codes are needed so the unique demographics of your city can be compared with those of the 14,232 schools having experienced a school shooting or having certain percentages of school violence. Such compared categories are medium household income, estimated per capita, income? Estimated medium house or condo value, median, gross rent, percentage of rentals to ownership, percentage of residence, living in poverty, ethnicity percentages, percentages of murders, rapes, robberies, assault, burglaries, theft, auto theft, arson, number of full timeline enforcement employees, Number of residents foreign born, unemployment rate, list of common industries, list of common occupations, climate averages by month, number of psychologist and adolescent psychologists, average household size, percentage of family household, percentage of households with unmarried partners, number of gun stores, number of gun shows, number of theaters, religion adherence, obesity rates, preschool, obesity, rates, people feeling badly about themselves, percentage of alcohol or consumers,and average property taxes. Data Sources: City Data
    </h8>
    </div>
    """,
    unsafe_allow_html=True,
    )

def getStatesFromDB(geo_lookup):
    states = geo_lookup["state"].unique()
    print(states)

def main():
    filename = "/app/nsv/data/12Samples.csv"
    sampleData = read_samples(filename)
    num_samples = len(sampleData)
    geo_lookup = pd.read_csv('data/geo_lookup.csv')
    risk_factor_lookup = pd.read_csv('data/risk_factor_lookup.csv')

    #ind = random.randint(0, num_samples-1)
    #st.title("School Risk Assessment Form")
    print("session state = ", st.session_state)
    if 'clicked' not in st.session_state:
        st.session_state.ind = random.sample(range(num_samples), 1)[0]
        st.session_state.row_vals = buildDict(sampleData, st.session_state.ind)

        st.session_state.clicked = False
    fillup(st.session_state.row_vals, geo_lookup, risk_factor_lookup)

    
if __name__ == '__main__':
    main()
