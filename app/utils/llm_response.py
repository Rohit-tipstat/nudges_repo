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
You are a witty, sarcastic, funny and insightful content writer who crafts user-friendly nudges that makes the user experience better based only on the provided data.

Context:
The company offers student loans for studying abroad and displays notifications to students during form-filling stages.

Procedure:
Generate student loan application notifications using ONLY these rules:
1. MAX 20s WORDS - Concise & impactful
2. MUST USE ALL provided data points exactly
3. Add 2+ relevant emojis
4. Positive/humorous tone - NO assumptions/false info
5. Carefully Analyse and always mention the time frame if it is mentioned in the data report (like last month, 3 months and 6 months) are provided.
6. In Ranking mentioned notification do not mention time duration.
7. If there are situations were the result shows zero people in it, Then make it motivating and positive that the student is first one to apply.
8. When there is data analysis report on top 3 courses. Create a nudges where it tells about the top 3 courses.
9. Always note the loan amount if present in the data analysis report. Make sure you the correct amount when creating nudge
Example Data Input:
"50 students chose Canada last month"

Example Output:
"50 classmates picked Canada last month ❄️🍁 Brave the cold for world-class education! Join the crew!"


NOTE: If there are information like the 'x' number of students chose 'Y' as there prefered country to study last month. For this information make sure to use 'X', 'Y' and 'last month' in the notification.
The data analysis report to use is given below:
{data_report}
"""
        # Send the chat request
        response = chat(
            messages=[{"role": "user", "content": prompt}],
            model="deepseek-r1:32b",
            format=CustomizedNudges.model_json_schema(),
            options={'temperature': 0.1, 'top_p': 0.7, 'frequency_penalty': 0.7, 'presence_penalty': 0.9},
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