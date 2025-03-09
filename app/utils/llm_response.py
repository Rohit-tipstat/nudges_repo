from pydantic import BaseModel, ValidationError, Field
from ollama import chat
from typing import Optional, List


class CustomizedNudges(BaseModel):
    nudges: List[str] = Field(..., max_items=1)
    
def custom_nudges(data_report: list) -> Optional[list]:
    """
    Extracts event information from the input text using OpenAI's API.
    Args:
        data_report (str): The input text containing document information.
    Returns:
        dict: Parsed nudges or None if an error occurs.
    """
    try:
        # Prepare the prompt
        prompt = f"""
Objective:
Create engaging and creative notifications that enhance the student loan experience.

Your Role:
You are a witty and insightful content writer who crafts user-friendly nudges based only on the provided data.

Context:
The company offers student loans for studying abroad and displays notifications to students during form-filling stages.

Guidelines for Crafting Nudges:
a) Keep it short and engaging: Maximum 15 words per nudge.
b) Blend creativity with facts: Use humor, motivation, positivity, and relevant insights.
c) Use a respectful and inclusive tone: No offensive or misleading content.
d) Use emojis wisely: They enhance engagement but shouldn't be overused.
e) Be precise and accurate: Always include complete financial details, exact numbers, and time frames.
f) Focus on the company's role: Never assume students are self-financing; emphasize the loan provider's support.
g) Provide only one meaningful nudge per request.
h) No misleading or false claims: Use only the data provided, never assume anything or give infromation that is not mentioned 
i) Include all relevant details: Never leave out critical information like time frames, amounts, or application counts.
j) Avoid misleading phrasing: Instead of saying "You have received a loan," use "Students like you have received an average loan of X amount."
The data report is given below to analyze. Make sure to use the information provided. 
{data_report}
"""


        # Send the chat request
        response = chat(
            messages=[{"role": "user", "content": prompt}],
            model="deepseek-r1:70b",
            format=CustomizedNudges.model_json_schema(),
            options={'temperature': 0.1, 'top_p': 0.1, 'frequency_penalty': 0.7, 'presence_penalty': 0.9},
        )

        # Parse and validate the response
        output_json = CustomizedNudges.model_validate_json(response.message.content)
        #print("The result:", output_json)
        return [output_json]

    except ValidationError as ve:
        print("Validation error:", ve)
    except Exception as e:
        print("An error occurred during processing:", e)

    return None