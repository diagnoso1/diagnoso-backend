from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from gpt_integration import system_prompt

# Load environment variables
load_dotenv()

# Initialize OpenAI client (new SDK format)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class ClinicalInput(BaseModel):
    doctor_name: str
    patient_data: str

@app.post("/diagnose")
async def diagnose(clinical_input: ClinicalInput):
    messages = [
        {"role": "system", "content": system_prompt()},
        {"role": "user", "content": f"Doctor Name: {clinical_input.doctor_name}\nPatient Data: {clinical_input.patient_data}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.1
        )
        reply = response.choices[0].message.content

    except Exception as e:
        print(f"OpenAI Error: {e}")
        return {"error": str(e)}

    return {"result": reply}
