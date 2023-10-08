import streamlit as st
import random
import datetime
import pandas as pd
import numpy as np
import math

def welcome():
    return 'welcome all'

def read_samples(filename):
    print("Reading the sample file:", filename)
    sample_file = pd.read_csv(filename)
    print("Type of Data File = ", type(sample_file))
    print("#Samples = ", len(sample_file))
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
        prediction_result = "Low vulnerability index"
        prediction_color = "green"  # Color for a positive result
    elif total_risk_factor >= 0.3 and total_risk_factor < 0.8:
        prediction_result = "Moderate vulnerability index"
        prediction_color = "orange"  # Color for a negative result

    else:
        prediction_result = "High vulnerability index"
        prediction_color = "red"  # Color for a negative result

    return prediction_result, prediction_color
def buildDict(df, row_id):
    row_dic = {}
    colnames = df.columns
    for col in colnames:
        print("Adding ", df.loc[row_id].at[col], " to dict:", col)
        row_dic[col] = df.loc[row_id].at[col]
    return row_dic

def fillup(row_vals):
    st.markdown(
    """
    <div style="background-color:lightgray">
    <h6 style="color:black">
    Please fill in this form so your school and your community can be compared to the 14,232 schools and communities having experienced a school shooting or violence preceding a shooting. This comparsion will provide both a detailed risk percentage by data category as well as an overall percentile ranking. Once specific vulnerables are identfied, you will be provided with options to lessen or remove those vulnerabilities.
    </h6>
    </div>
    """,
    unsafe_allow_html=True,
    )
    #st.markdown(nsv_caption, unsafe_allow_html=True)
    schoolName = ""
    if not math.isnan(row_vals["school_name"]):
        schoolName = row_vals["school_name"]
    school_name = st.text_input("School Name", schoolName)

    school_type_lst = ["", "Elementary", "Middle School", "High School"]
    print("row_vals['school_level_type'] = ", row_vals['school_level_type'])
    school_type_ind = school_type_lst.index(row_vals["school_level_type"])
    school_level_type = st.selectbox("School Level/Type", school_type_lst, school_type_ind)

    school_address_zip = st.text_input("School Address and Zip*", row_vals["school_address_zip"])

    st.write("Hours of Operation")
    col1, col2 = st.columns(2)
    with col1:
	    hours_oper_from = st.time_input("From", datetime.time())
	    #hours_oper_from = st.time_input("From", row_vals["hours_oper_from"])

    with col2:
	    hours_oper_to = st.time_input("To", datetime.time())
	    #hours_oper_from = st.time_input("From", row_vals["hours_oper_to"])


    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.write("Number of Staff")
    col1, col2 = st.columns(2)
    with col1:
            num_teachers = st.number_input("Teachers", min_value=1, value=row_vals["num_teachers"])
            #num_psych_couns= st.number_input("Psychologists/Counselors (FT/PT)", value=row_vals["num_psych_couns"])
            num_psych_couns= st.number_input("Psychologists/Counselors (FT/PT)", value=0)
            num_other_staff = st.number_input("Other", value=row_vals["num_other_staff"])

    with col2:
	    num_admin = st.number_input("Admin", value=row_vals["num_admin"])
	    num_safety_resources = st.number_input("Safety Resources", value=row_vals["num_safety_resources"])

    st.markdown("""<hr>""", unsafe_allow_html=True)
    num_enrolled_students = st.number_input("Student Enrollment Number", value=row_vals["num_enrolled_students"])
    col1, col2 = st.columns(2)
    with col1:
        num_male_students = st.number_input("% Male_Students", value=row_vals["num_male_students"])
        identifying_differently = st.number_input("% Identifying Differently", value=row_vals["identifying_differently"])
    with col2:
        num_female_students= st.number_input("% Female Students", value=row_vals["num_female_students"])

    st.write("Age Range of Student Body")
    col1, col2 = st.columns(2)
    with col1:
        min_age= st.number_input("Min Age", min_value=3, max_value=99, value=3)
    with col2:
        max_age = st.number_input("Max Age", min_value=3, max_value=99, value=3)

    st.markdown("""<hr>""", unsafe_allow_html=True)

    st.write("Percentage by Enthnicity")
    col1, col2 = st.columns(2)
    with col1:
            american_indian_alaska_native = st.number_input("American Indian or Alaska Native", value=row_vals["american_indian_alaska_native"])
            hispanic_latino = st.number_input("Hispanic or Latino", value=row_vals["hispanic_latino"])
            asian = st.number_input("Asian", value=row_vals["asian"])
    with col2:
            black_african_american = st.number_input("Black or African American", value=row_vals["black_african_american"])
            white = st.number_input("White", value=row_vals["white"])
            native_hawaiian_other_pacific_islander = st.number_input("Native Hawaiian or Pacific Islander", value=row_vals["native_hawaiian_other_pacific_islander"])

    st.markdown("""<hr>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
	    num_bullying_occurrences = st.number_input("Number of Bullying Occurrences",min_value=0, value=row_vals["num_bullying_occurrences"])

	    num_suicide_events = st.number_input("Number of Suicide Events", min_value=0, value=row_vals["num_suicide_events"])

    with col2:
	    num_times_guns_brought_school = st.number_input("Number of Times Guns Were Brought to School",min_value=0, value=row_vals["num_times_guns_brought_school"])

	    num_violent_events_total = st.number_input("Number of Violent Events Total",min_value=0, value=row_vals["num_violent_events_total"]) 

    st.markdown("""<hr>""", unsafe_allow_html=True)

    st.write("Number of Violent Events (Location)")
    col1, col2 = st.columns(2)
    with col1:
	    school_hours_and_reported_provocation = st.number_input("School Hours and reported provocation (ie. Escalation of dispute, racial, targeted victim)", min_value=0, value=row_vals["school_hours_and_reported_provocation"]) 
	    sporting_event = st.number_input("Sporting Event", min_value=0, value=row_vals["sporting_event"])
    with col2:
	    nearby_school = st.number_input("Nearby School", min_value=0, value=row_vals["nearby_school"])

    st.markdown("""<hr>""", unsafe_allow_html=True)

    st.write("Has media reported on any violent event at your school?")
    col1, col2 = st.columns(2)
    with col1:
	    media_when = st.text_input("When", "")
	    media_type = st.text_input("Media Type", "")
	    #media_when = st.text_input("When", row_vals["media_when"])
	    #media_type = st.text_input("Media Type", row_vals["media_type"])
    with col2:
	    how_many_times = st.number_input("How many times?", min_value=0,value=0)
	    dates_of_reports = st.text_input("Dates of reports?", "")
	    #how_many_times = st.number_input("How many times?", min_value=0,value=row_vals["how_many_times"])
	    #dates_of_reports = st.text_input("Dates of reports?", row_vals["dates_of_reports"])


    result = ""

    if st.button("Inference"):
        prediction_result, prediction_color = prediction(school_level_type, school_address_zip, num_teachers, num_psych_couns, num_enrolled_students, num_violent_events_total, num_suicide_events, num_times_guns_brought_school, num_bullying_occurrences, school_hours_and_reported_provocation, sporting_event, nearby_school)
        st.markdown(
            f'<p style="color: {prediction_color}; font-size: 18px;">Inference: {prediction_result}</p>',
            unsafe_allow_html=True
        )
    st.markdown(
    """
    <div style="background-color:lightgray">
    <h8 style="color:black">
    *Zip Codes are needed so the unique demographics of your city can be compared with those of the 14,232 schools having experienced a school shooting or having certain percentages of school violence. Such compared categories are medium household income, estimated per capita, income? Estimated medium house or condo value, median, gross rent, percentage of rentals to ownership, percentage of residence, living in poverty, ethnicity percentages, percentages of murders, rapes, robberies, assault, burglaries, theft, auto theft, arson, number of full timeline enforcement employees, Number of residents foreign born, unemployment rate, list of common industries, list of common occupations, climate averages by month, number of psychologist and adolescent psychologists, average household size, percentage of family household, percentage of households with unmarried partners, number of gun stores, number of gun shows, number of theaters, religion adherence, obesity rates, preschool, obesity, rates, people feeling badly about themselves, percentage of alcohol or consumers,and average property taxes. Data Sources: City Data
    </h8>
    </div>
    """,
    unsafe_allow_html=True,
    )


def main():
    filename = "/Users/archana/nsv/data/12Samples.csv"
    sampleData = read_samples(filename)
    num_samples = len(sampleData)
    low = 1
    moderate = 9
    high = 11
    #ind = random.sample(range(num_samples), 1)[0]
    ind = high 
    row_vals = buildDict(sampleData, ind)
    st.title("School Risk Assessment Form")
    fillup(row_vals)

if __name__ == '__main__':
    main()
