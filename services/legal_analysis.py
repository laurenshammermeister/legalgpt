import os
import json
import logging
from openai import OpenAI

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_legal_text(text, audience="layperson"):
    """
    Analyze legal text using OpenAI's GPT model.
    
    Args:
        text (str): The legal text to analyze
        audience (str): The target audience for the explanation (layperson or law_student)
        
    Returns:
        dict: A dictionary containing the explanation and risks
    """
    try:
        # Define the prompt based on the audience
        if audience == "law_student":
            system_prompt = """You are a legal expert assistant that specializes in explaining legal documents to law students.
            Analyze the legal text provided and respond with a JSON object containing:
            1. A concise legal summary with proper terminology
            2. An identification of potential legal risks or concerns
            3. References to relevant legal principles or statutes when applicable
            
            Format your response as a JSON object with these keys: 
            "explanation", "risks", "legal_principles"
            """
        else:  # layperson
            system_prompt = """You are a legal expert assistant that specializes in explaining legal documents to people without legal training.
            Analyze the legal text provided and respond with a JSON object containing:
            1. A simple, easy-to-understand explanation of what the legal text means
            2. An identification of potential risks or concerns in plain language
            3. A simple rating of how concerning this clause might be (on a scale of 1-5, where 5 is most concerning)
            
            Format your response as a JSON object with these keys: 
            "explanation", "risks", "concern_level"
            """
        
        logging.debug(f"Sending text to OpenAI for analysis. Length: {len(text)}")
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        
        # Extract and parse the response
        response_content = response.choices[0].message.content
        analysis_result = json.loads(response_content)
        
        logging.debug("Successfully received analysis from OpenAI")
        return analysis_result
        
    except Exception as e:
        logging.error(f"Error in analyze_legal_text: {str(e)}")
        # Return a structured error to maintain expected format
        return {
            "explanation": "There was an error analyzing the text. Please try again.",
            "risks": "Unable to determine risks due to an error.",
            "concern_level": 0 if audience == "layperson" else None,
            "legal_principles": [] if audience == "law_student" else None,
            "error": str(e)
        }
