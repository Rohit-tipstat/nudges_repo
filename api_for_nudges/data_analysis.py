import pandas as pd
from helper_function import helper
from typing import List, Optional
import math
from datetime import datetime, timedelta
import math




def country_selected(data: pd.DataFrame, country_of_study: str, source_city: str) -> List[str]:
    """
    Perform analysis for a specific country selection.

    Args:
        data (pd.DataFrame): Input DataFrame.
        country_of_study (str): The country selected for study.
        source_city (str): The city for filtering.

    Returns:
        List[str]: Analysis results.
    """
    # Convert 'Login Date' to datetime format
    data.loc[:, 'Login Date'] = pd.to_datetime(data['Login Date'], format='%Y-%m-%d')

    # Define date ranges
    today = datetime.today()
    six_months_ago = today - timedelta(days=6 * 30)
    three_months_ago = today - timedelta(days=3 * 30)
    one_month_ago = today - timedelta(days=30)

    # Filter data for the selected country
    country_selected_data = data[data['Country of Study'] == country_of_study]

    # Count registrations in the last 6, 3, and 1 months
    last_6_months_country_of_study = len(country_selected_data[country_selected_data['Login Date'] >= six_months_ago])
    last_3_months_country_of_study = len(country_selected_data[country_selected_data['Login Date'] >= three_months_ago])
    last_1_month_country_of_study = len(country_selected_data[country_selected_data['Login Date'] >= one_month_ago])

    # Count students from the source city
    count_filtered_by_city = len(country_selected_data[country_selected_data['Source Branch'] == source_city])

    # Loan details
    loan_disbursed_sanctioned = country_selected_data[country_selected_data['CURRENT_WS'].isin(['Disbursed', 'Sanctioned'])]
    sum_of_COE = math.ceil(loan_disbursed_sanctioned['Total COE'].fillna(0).sum())

    number_of_people = len(country_selected_data)
    average_loan_per_person = math.ceil(sum_of_COE / max(1, len(loan_disbursed_sanctioned)))

    output = []
    
    # Only add datapoints if they're greater than 0
    if average_loan_per_person > 0:
        output.append(f"On average, students applying for {country_of_study} had requested for a loan of amount {helper.indian_human_readable(average_loan_per_person)}")
    
    if count_filtered_by_city > 0:
        output.append(f"{count_filtered_by_city} students from {source_city} have applied to study in {country_of_study}.")
    
    if last_6_months_country_of_study > 0:
        output.append(f"A total of {last_6_months_country_of_study} students chose {country_of_study} as there prefered country to study in last 6 months.")
    
    if last_3_months_country_of_study > 0:
        output.append(f"{last_3_months_country_of_study} students chose {country_of_study} as there prefered country to study in the last 3 months!")
    
    if last_1_month_country_of_study > 0:
        output.append(f"{last_1_month_country_of_study} students chose {country_of_study} as there prefered country to study last month!")

    # Rank the country based on applications (only if there are applications)
    country_counts = data['Country of Study'].value_counts()
    if country_of_study in country_counts and country_counts[country_of_study] > 0:
        ranked_countries = country_counts.sort_values(ascending=False).reset_index()
        ranked_countries.columns = ['Country of Study', 'Number of Applications']
        rank_position = ranked_countries[ranked_countries['Country of Study'] == country_of_study].index[0] + 1
        output.append(f"{country_of_study} rank {rank_position} based on student applications received.")

    return output


def university_selected(data: pd.DataFrame, university_name: str, source_city: str) -> List[str]:
    """
    Perform data analysis for a selected university.

    Args:
        data (pd.DataFrame): Input DataFrame.
        university_name (str): The university name.
        source_city (str): Source city for filtering.

    Returns:
        List[str]: Analysis results.
    """
    # Convert 'Login Date' to datetime format
    data.loc[:, 'Login Date'] = pd.to_datetime(data['Login Date'], format='%Y-%m-%d')

    # Define date ranges
    today = datetime.today()
    six_months_ago = today - timedelta(days=6 * 30)
    three_months_ago = today - timedelta(days=3 * 30)
    one_month_ago = today - timedelta(days=30)

    # Filter data for the selected university
    university_data = data[data['University Name'] == university_name]
    six_month_city_specific_data = len(university_data[(university_data['Source Branch'] == source_city) & (university_data['Login Date'] >= six_months_ago)])
    three_month_city_specific_data = len(university_data[(university_data['Source Branch'] == source_city) & (university_data['Login Date'] >= three_months_ago)])
    one_month_city_specific_data = len(university_data[(university_data['Source Branch'] == source_city) & (university_data['Login Date'] >= one_month_ago)])

    # Count registrations in the last 6, 3, and 1 months
    last_6_months = len(university_data[university_data['Login Date'] >= six_months_ago])
    last_3_months = len(university_data[university_data['Login Date'] >= three_months_ago])
    last_1_month = len(university_data[university_data['Login Date'] >= one_month_ago])

    # Loan details
    loan_disbursed_sanctioned = university_data[university_data['CURRENT_WS'].isin(['Disbursed', 'Sanctioned'])]
    total_loan_amount = math.ceil(loan_disbursed_sanctioned['Total COE'].fillna(0).sum())
    avg_loan_per_person = math.ceil(total_loan_amount / max(1, len(loan_disbursed_sanctioned)))

    # Top 3 courses
    top_courses = university_data['Course Name'].value_counts().nlargest(3).reset_index()
    top_courses.columns = ['Course Name', 'Number of Applicants']

    # Rank the university based on applications
    university_counts = data['University Name'].value_counts()
    rank_position = "Not Ranked"
    if university_name in university_counts and university_counts[university_name] > 0:
        ranked_universities = university_counts.reset_index()
        ranked_universities.columns = ['University Name', 'Number of Applications']
        rank_position = ranked_universities[ranked_universities['University Name'] == university_name].index[0] + 1

    output = []

    # Only add datapoints if they're greater than 0
    if one_month_city_specific_data > 0:
        output.append(f"In last 1 month, {one_month_city_specific_data} students from {source_city} applied to {university_name}")
    
    if three_month_city_specific_data > 0:
        output.append(f"In last 3 months, {three_month_city_specific_data} students from {source_city} applied to {university_name}")
    
    if avg_loan_per_person > 0:
        output.append(f"An Average loan amount of {helper.indian_human_readable(avg_loan_per_person)} was requested previously by the students who joined {university_name}")
    
    if last_6_months > 0:
        output.append(f"A total of {last_6_months} students showed interest to study in {university_name} in last 6 months")
    
    if last_3_months > 0:
        output.append(f"{last_3_months} students showed interest to study in {university_name} in last 3 months")
    
    if last_1_month > 0:
        output.append(f"Last month, {last_1_month} students were interested to study in {university_name}")

    # Add ranking if university has applications
    if rank_position != "Not Ranked":
        output.append(f"{university_name} is ranked {rank_position} based on the number of student applications")

    # Format popular courses only if there are any
    if not top_courses.empty:
        course_nudges_ = [
            f"{university_name} Popular course {i + 1}: {row['Course Name']} with {row['Number of Applicants']} applicants"
            for i, row in top_courses.iterrows()
        ]
        course_nudge = " | ".join(course_nudges_)
        output.append(course_nudge)

    return output


def course_type_analysis(data: pd.DataFrame, course_type: str, source_city: str, 
                        country_of_study: Optional[str] = None, university_name: Optional[str] = None) -> List[str]:
    """
    Analyze data based on course type.

    Args:
        data (pd.DataFrame): Input DataFrame.
        course_type (str): Course type for filtering.
        source_city (str): Source city for filtering.
        country_of_study (Optional[str]): Optional country filter.
        university_name (Optional[str]): Optional university filter.

    Returns:
        List[str]: Analysis results.
    """
    
    data.loc[:, 'Login Date'] = pd.to_datetime(data['Login Date'], format='%Y-%m-%d')

    # Get current date
    today = datetime.today()

    # Define time ranges
    last_6_months = today - timedelta(days=6*30)
    last_3_months = today - timedelta(days=3*30)
    last_1_month = today - timedelta(days=30)

    # Filter data for the given course_type
    filtered_data = data[data['Course Type'] == course_type]

    # Total students who selected this course type
    total_students = len(filtered_data)
    city_students_count = len(filtered_data[filtered_data['Source Branch'] == source_city])

    # Loan calculations
    total_loan_amount = math.ceil(filtered_data['Total COE'].fillna(0).sum())
    avg_loan_amount = math.ceil(total_loan_amount / max(1, total_students))

    # Count students who chose this course_type in the last 6, 3, and 1 month
    last_6_months_count = len(filtered_data[filtered_data['Login Date'] >= last_6_months])
    last_3_months_count = len(filtered_data[filtered_data['Login Date'] >= last_3_months])
    last_1_month_count = len(filtered_data[filtered_data['Login Date'] >= last_1_month])

    # Rank course types by popularity
    course_type_counts = data['Course Type'].value_counts()
    rank_position = "Not Ranked"
    if course_type in course_type_counts and course_type_counts[course_type] > 0:
        ranked_course_types = course_type_counts.sort_values(ascending=False).reset_index()
        ranked_course_types.columns = ['Course Type', 'Number of Applications']
        rank_position = ranked_course_types[ranked_course_types['Course Type'] == course_type].index[0] + 1

    # Get popular courses
    popular_courses = filtered_data['Course Name'].value_counts().head(3).reset_index()
    popular_courses.columns = ['Course Name', 'Number of Applicants']

    output = []

    # Only add datapoints if they're greater than 0
    if total_students > 0:
        output.append(f"Over {total_students} students have selected {course_type} course uptil now.")
    
    if city_students_count > 0:
        output.append(f"Number of students from {source_city} applying to {course_type}: {city_students_count}")
    
    if last_6_months_count > 0:
        output.append(f"Students who selected {course_type} course in the last 6 months: {last_6_months_count}")
    
    if last_3_months_count > 0:
        output.append(f"Students who selected {course_type} course in the last 3 months: {last_3_months_count}")
    
    if last_1_month_count > 0:
        output.append(f"Students who selected {course_type} course in the last 1 month: {last_1_month_count}")
    
    if avg_loan_amount > 0:
        output.append(f"Previously students with {course_type} course requested for an Average loan amount of {helper.indian_human_readable(avg_loan_amount)}")

    
    # Popular course details only if there are any
    if not popular_courses.empty:
        popular_course_ = [
            f"Popular course {idx + 1}: {row['Course Name']} with {row['Number of Applicants']} applicants"
            for idx, row in popular_courses.iterrows()
        ]
        course_nudge = "|".join(popular_course_)
        output.append(course_nudge)

    # Country-specific data only if specified and has value
    if country_of_study:
        country_students = data[data['Country of Study'] == country_of_study]
        total_country_students = len(country_students)
        if total_country_students > 0:
            output.append(f"A total of {total_country_students} students have gone to {country_of_study} with our help")

    return output

def analyze_student_exam_data(
    data: pd.DataFrame,
    exam_taken: str,
    score: float,
    course_type: str,
    source_city: str,
    country_of_study: str,
    university_name: str) -> List[str]:
    """
    Analyze student application data and provide insights based on the given parameters.

    Args:
        data (pd.DataFrame): Input DataFrame containing student records.
        exam_taken (str): The exam taken by the student (e.g., GRE, TOEFL).
        score (float): The student's score in the exam.
        course_type (str): The type of course applied for (e.g., Masters, Bachelors).
        source_city (str): The city where the application originated.
        country_of_study (str): The country selected for study.
        university_name (str): The university selected by the student.

    Returns:
        List[str]: Analysis results including counts and averages.
    """
    
    data.loc[:, 'Login Date'] = pd.to_datetime(data['Login Date'], format='%Y-%m-%d')

    # Define time periods
    today = datetime.today()
    last_6_months = today - timedelta(days=180)
    last_3_months = today - timedelta(days=90)
    last_1_month = today - timedelta(days=30)

    # Filter data for students with similar exam scores applying to the same university
    similar_students = data[
        (data[exam_taken] >= score - 10) &
        (data[exam_taken] <= score + 10)
    ]
    num_similar_students = similar_students.shape[0]

    # Average loan amount for students with similar exam scores
    avg_loan = similar_students['Total COE'].mean()
    avg_loan_formatted = helper.indian_human_readable(math.ceil(avg_loan)) if not pd.isna(avg_loan) else "0"

    # Students who registered in the last 6 months, 3 months, and 1 month
    students_last_6_months = similar_students[similar_students["Login Date"] >= last_6_months].shape[0]
    students_last_3_months = similar_students[similar_students["Login Date"] >= last_3_months].shape[0]
    students_last_1_month = similar_students[similar_students["Login Date"] >= last_1_month].shape[0]

    # Top 3 most applied universities in the same country with the same exam and similar scores
    top_applied_universities_ = (
        data[
            (data['Country of Study'] == country_of_study) &
            (data[exam_taken] >= score - 10) &
            (data[exam_taken] <= score + 10)
        ]['University Name'].value_counts().head(3).index.tolist()
        if not data.empty else []
    )
    top_applied_universities = " * ".join(top_applied_universities_) if top_applied_universities_ else ""

    # Compile the results
    results = []

    # Only add datapoints if they're greater than 0 or meaningful
    if num_similar_students > 0:
        results.append(f"{num_similar_students} students with a similar {exam_taken} score have enrolled!")

    if not pd.isna(avg_loan) and avg_loan > 0:
        results.append(f"On average, students with a similar {exam_taken} score have requested for a loan amount of {avg_loan_formatted}.")

    if students_last_6_months > 0:
        results.append(f"In last 6 months, {students_last_6_months} students with a similar {exam_taken} score have registered with us!")

    if students_last_3_months > 0:
        results.append(f"In last 3 months, {students_last_3_months} students with a similar {exam_taken} score have registered with us!")

    if students_last_1_month > 0:
        results.append(f"In last 1 month, {students_last_1_month} students with a similar {exam_taken} score have registered with us!")

    if top_applied_universities:
        results.append(f"{country_of_study}'s popular colleges: {top_applied_universities}.")

    return results

def course_level_analysis(data: pd.DataFrame, course_level: str, source_city: str, 
                         country_of_study: Optional[str] = None, university_name: Optional[str] = None) -> List[str]:
    """
    Analyze data based on course level.

    Args:
        data (pd.DataFrame): Input DataFrame.
        course_level (str): Course level for filtering.
        source_branch (str): Source branch for filtering.
        country_of_study (Optional[str]): Optional country filter.
        university_name (Optional[str]): Optional university filter.

    Returns:
        List[str]: Analysis results.
    """
    
    data.loc[:, 'Login Date'] = pd.to_datetime(data['Login Date'], format='%Y-%m-%d')


    # Define time periods
    today = datetime.today()
    six_months_ago = today - timedelta(days=180)
    three_months_ago = today - timedelta(days=90)
    one_month_ago = today - timedelta(days=30)

    # Filter data based on course level
    filtered_data = data[data['Course level'] == course_level]
    total_students = len(filtered_data)
    branch_students_count = len(filtered_data[filtered_data['Source Branch'] == source_city])

    # Loan calculations
    total_loan_amount = filtered_data['Total COE'].fillna(0).sum()
    avg_loan_amount = math.ceil(total_loan_amount / max(1, total_students))

    # Registrations in last 6, 3, and 1 month(s)
    students_last_6_months = len(filtered_data[filtered_data['Login Date'] >= six_months_ago])
    students_last_3_months = len(filtered_data[filtered_data['Login Date'] >= three_months_ago])
    students_last_1_month = len(filtered_data[filtered_data['Login Date'] >= one_month_ago])

    # Popular courses at this course level
    popular_courses = filtered_data['Course Name'].value_counts().head(3).reset_index()
    popular_courses.columns = ['Course Name', 'Number of Applicants']
    
    # Universities offering this course level
    university_counts = filtered_data['University Name'].value_counts().head(5).reset_index()
    university_counts.columns = ['University Name', 'Number of Students']
    
    # Prepare output
    output = []

    # Only add datapoints if they're greater than 0
    if total_students > 0:
        output.append(f"A lifetime total of {total_students} students enrolled in {course_level} with us")
    
    if branch_students_count > 0:
        output.append(f"Number of students from {source_city} enrolled in {course_level}: {branch_students_count}")
    
    if avg_loan_amount > 0:
        output.append(f"Average loan per person for {course_level}: {helper.indian_human_readable(avg_loan_amount)}")
    
    if students_last_6_months > 0:
        output.append(f"In last 6 months, {students_last_6_months} students registered for {course_level} course")
    
    if students_last_3_months > 0:
        output.append(f"In last 3 months, {students_last_3_months} students registered for {course_level} course")
    
    if students_last_1_month > 0:
        output.append(f"In last 1 month, {students_last_1_month} students registered for {course_level} course")

    # Popular courses (only if there are any)
    if not popular_courses.empty:
        popular_courses_ = [f"Popular course {idx + 1}: {row['Course Name']} with {row['Number of Applicants']} applicants" 
                          for idx, row in popular_courses.iterrows()]
        output.append("|".join(popular_courses_))

    # Top universities (only if there are any)
    if not university_counts.empty:
        top_universities_ = [f"Top university {idx + 1}: {row['University Name']} with {row['Number of Students']} students" 
                            for idx, row in university_counts.iterrows()]
        output.append("|".join(top_universities_))

    # Country-level analysis (if provided and has data)
    if country_of_study:
        country_data = filtered_data[filtered_data['Country of Study'] == country_of_study]
        total_country_students = len(country_data)
        if total_country_students > 0:
            output.append(f"{country_of_study} has a lifetime total of {total_country_students} student applications.")

    # University-level analysis (if provided and has data)
    if university_name:
        university_data = filtered_data[filtered_data['University Name'] == university_name]
        total_university_students = len(university_data)
        if total_university_students > 0:
            total_university_loans = university_data['Total COE'].fillna(0).sum()
            avg_university_loans = math.ceil(total_university_loans / max(1, total_university_students))
            output.append(f"{university_name} has {total_university_students} students and an avg loan amount of {helper.indian_human_readable(avg_university_loans)} provided.")

    return output


def course_name_analysis(data: pd.DataFrame, course_name: str, source_city: str, 
                        country_of_study: Optional[str] = None, university_name: Optional[str] = None) -> List[str]:
    """
    Analyze data based on Course Name.

    Args:
        data (pd.DataFrame): Input DataFrame.
        course_name (str): Course name for filtering.
        source_city (str): Source city for filtering.
        country_of_study (Optional[str]): Optional country filter.
        university_name (Optional[str]): Optional university filter.

    Returns:
        List[str]: Analysis results.
    """
    
    data.loc[:, 'Login Date'] = pd.to_datetime(data['Login Date'], format='%Y-%m-%d')


    # Filter data based on the given course name
    filtered_data = data[data['Course Name'] == course_name]
    total_students = len(filtered_data)
    city_students_count = len(filtered_data[filtered_data['Source Branch'] == source_city])

    # Loan Analysis
    total_loan_amount = filtered_data['Total COE'].fillna(0).sum()
    avg_loan_amount = math.ceil(total_loan_amount / max(1, total_students))

    # Popular Universities for the Course
    popular_universities = filtered_data['University Name'].value_counts().head(3).reset_index()
    popular_universities.columns = ['University Name', 'Number of Students']

    # Time-based Analysis
    today = datetime.today()
    last_6_months = today - timedelta(days=180)
    last_3_months = today - timedelta(days=90)
    last_1_month = today - timedelta(days=30)

    last_6m_count = len(filtered_data[filtered_data['Login Date'] >= last_6_months])
    last_3m_count = len(filtered_data[filtered_data['Login Date'] >= last_3_months])
    last_1m_count = len(filtered_data[filtered_data['Login Date'] >= last_1_month])

    # Prepare output
    output = []

    # Only add datapoints if they're greater than 0
    if total_students > 0:
        output.append(f"A total of {total_students} students have enrolled in {course_name} in our application.")
    
    if city_students_count > 0:
        output.append(f"In total, {city_students_count} students from {source_city} applying for {course_name}.")
    
    if avg_loan_amount > 0:
        output.append(f"An Average loan of {helper.indian_human_readable(avg_loan_amount)} for a course like {course_name}")
    
    if last_6m_count > 0:
        output.append(f"In last 6 months, {last_6m_count} students have registered for {course_name}")
    
    if last_3m_count > 0:
        output.append(f"In the last 3 months, {last_3m_count} students have registered for {course_name}")
    
    if last_1m_count > 0:
        output.append(f"In the last 1 month, {last_1m_count} students have registered for {course_name}")

    # Popular Universities (only if there are any)
    if not popular_universities.empty:
        popular_universities_ = [
            f"Popular University {idx + 1}: {row['University Name']} with {row['Number of Students']} students"
            for idx, row in popular_universities.iterrows()
        ]
        output.append("|".join(popular_universities_))

    # Country-level analysis (if provided and has data)
    if country_of_study:
        country_data = filtered_data[filtered_data['Country of Study'] == country_of_study]
        total_country_students = len(country_data)
        if total_country_students > 0:
            output.append(f"{country_of_study} has a lifetime total of {total_country_students} student applications for {course_name}")

    # University-level analysis (if provided and has data)
    if university_name:
        university_data = filtered_data[filtered_data['University Name'] == university_name]
        total_university_students = len(university_data)
        if total_university_students > 0:
            output.append(f"{university_name} has {total_university_students} students enrolled in {course_name}")

    return output


def general_nudges(data: pd.DataFrame) -> List[str]:
    """
    Generate general nudges based on registration trends, countries, universities, and source branches.

    Args:
        data (pd.DataFrame): Input DataFrame containing student records.

    Returns:
        List[str]: List of general nudge messages.
    """
    # Convert 'Login Date' to datetime format
    data['Login Date'] = pd.to_datetime(data['Login Date'], errors='coerce')
    data = data.dropna(subset=['Login Date'])  # Drop rows with invalid dates
    
    # Define time periods
    today = datetime.today()
    one_year_ago = today - timedelta(days=365)
    six_months_ago = today - timedelta(days=6 * 30)
    three_months_ago = today - timedelta(days=3 * 30)
    
    # Calculate registrations over time
    registrations_one_year = len(data[data['Login Date'] >= one_year_ago])
    registrations_six_months = len(data[data['Login Date'] >= six_months_ago])
    registrations_three_months = len(data[data['Login Date'] >= three_months_ago])

    # Number of unique countries applied for
    num_countries = data['Country of Study'].nunique()

    # Number of unique universities students have gone to
    num_universities = data['University Name'].nunique()

    # Number of unique source branches
    num_source_branches = data['Source Branch'].nunique()

    # Prepare output nudges
    output = []

    # Only add nudges if values are greater than 0
    if registrations_one_year > 0:
        output.append(f"In the last 1 year, {registrations_one_year} students have registered with us!")
    
    if registrations_six_months > 0:
        output.append(f"In the last 6 months, {registrations_six_months} students have joined our platform.")
    
    if registrations_three_months > 0:
        output.append(f"In the last 3 months, {registrations_three_months} students have signed up.")
    
    if num_countries > 0:
        output.append(f"Students have applied to study in {num_countries} different countries so far!")
    
    if num_universities > 0:
        output.append(f"A total of {num_universities} unique universities have been chosen by students up to now.")
    
    if num_source_branches > 0:
        output.append(f"Applications have come from {num_source_branches} different cities across the board.")

    return output