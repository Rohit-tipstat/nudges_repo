from fastapi import FastAPI, HTTPException, Form
from typing import Optional, List
import pandas as pd
from data_analysis import (
    country_selected, university_selected, course_type_analysis, analyze_student_exam_data,
    course_level_analysis, course_name_analysis, general_nudges)
from llm_response import custom_nudges
from helper_function.helper import remove_outliers_iqr_specific_columns, indian_human_readable
import random

app = FastAPI(title="Student Loan Data Analysis API", version="1.0.0")

# Load your data
try:
    original_data = pd.read_excel('/home/ubuntu/api_for_nudges/MONTHEND_MIS_12MAR2025.xlsx')
    # Clean data by removing outliers for specific columns
    cleaned_data = remove_outliers_iqr_specific_columns(original_data, ['Total COE'])
    data = pd.read_csv("/home/ubuntu/api_for_nudges/output.csv")
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="Data file not found")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")

# API Endpoints
@app.post("/analyze/country", response_model=List[str])
async def analyze_country(
    country_of_study: str = Form(...),
    source_city: str = Form(...)
):
    """
    Analyze data for a specific country.
    """
    try:
        result = country_selected(data, country_of_study, source_city)
        # Optionally generate custom nudges
        print("Results: ", result)

        if not result:
            return ["No Nudge!"]
        nudges = custom_nudges([random.choice(result)])
        
        return nudges[0].nudges
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/analyze/university", response_model=List[str])
async def analyze_university(
    university_name: str = Form(...),
    source_city: str = Form(...)
):
    """
    Analyze data for a specific university.
    """
    try:
        result = university_selected(data, university_name, source_city)
        print("Results: ", result)

        if not result:
            return ["No Nudge!"]
        
        nudges = custom_nudges([random.choice(result)])
        
        return nudges[0].nudges
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/analyze/course-type", response_model=List[str])
async def analyze_course_type(
    course_type: str = Form(...),
    source_city: str = Form(...),
    country_of_study: Optional[str] = Form(default=None),
    university_name: Optional[str] = Form(default=None)
):
    """
    Analyze data based on course type.
    """
    try:
        result = course_type_analysis(
            data, course_type, source_city, 
            country_of_study, university_name
        )
        print("Results: ", result)

        if not result:
            return ["No Nudge!"]
        nudges = custom_nudges([random.choice(result)])
        
        return nudges[0].nudges
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/analyze/exam-data", response_model=List[str])
async def analyze_exam_data(
    exam_taken: str = Form(...),
    score: float = Form(...),
    course_type: str = Form(...),
    source_city: str = Form(...),
    country_of_study: str = Form(...),
    university_name: str = Form(...)
):
    """
    Analyze student exam data.
    """
    try:
        result = analyze_student_exam_data(
            data, exam_taken, score, course_type,
            source_city, country_of_study, university_name
        )
        print("Results: ", result)

        if not result:
            return ["No Nudge!"]
        nudges = custom_nudges([random.choice(result)])
        
        return nudges[0].nudges
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/analyze/course-level", response_model=List[str])
async def analyze_course_level(
    course_level: str = Form(...),
    source_city: str = Form(...),
    country_of_study: Optional[str] = Form(default=None),
    university_name: Optional[str] = Form(default=None)
):
    """
    Analyze data based on course level.
    """
    try:
        result = course_level_analysis(
            data, course_level, source_city, 
            country_of_study, university_name
        )
        print("Results: ", result)
        if not result:
            return ["No Nudge!"]
        nudges = custom_nudges([random.choice(result)])
        
        return nudges[0].nudges
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/analyze/course-name", response_model=List[str])
async def analyze_course_name(
    course_name: str = Form(...),
    source_city: str = Form(...),
    country_of_study: Optional[str] = Form(default=None),
    university_name: Optional[str] = Form(default=None)
):
    """
    Analyze data based on course name.
    """
    try:
        result = course_name_analysis(
            data, course_name, source_city, 
            country_of_study, university_name
        )
        print("Results: ", result)
        if not result:
            return ["No Nudge!"]
        nudges = custom_nudges([random.choice(result)])
        
        return nudges[0].nudges
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/analyze/general", response_model=List[str])
async def analyze_general():
    """
    Provide general nudges based on registration trends, countries, universities, and source branches.
    """
    try:
        result = general_nudges(data)
        print("Results: ", result)
        if not result:
            return ["No Nudge!"]
        nudges = custom_nudges([random.choice(result)])  # Optional: Apply custom nudges if you have this logic
        
        return nudges[0].nudges
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
