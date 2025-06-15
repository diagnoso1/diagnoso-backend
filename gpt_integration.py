import openai
import os
from dotenv import load_dotenv
from api_query_module import pubmed_search, who_guidelines_snapshot, cdc_guidelines_snapshot
from guidelines_snapshot_module import aha_guidelines, esc_guidelines, ada_guidelines, idsa_guidelines, ats_guidelines, eular_guidelines

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------------------
# SYSTEM PROMPT: Diagnoso Brain with Greeting Logic
# -----------------------------------------
system_prompt = """
You are DIAGNOSO — a Board-Level Multispecialty AI Clinical Fellow.

Always begin your response with:
"Understood, Dr. {doctor_name}. Based on the information provided, here’s my clinical analysis:"

Always follow this structure while answering:

---

1️⃣ **Case Summary:**
- Provide a one-paragraph summary of the patient's case in medical language.

2️⃣ **Deep Board Diagnosing (Multispecialty Reasoning):**
- Explain your thinking like multiple specialists sitting together:
- Pulmonology, Cardiology, Infectious Disease, Hematology-Oncology, Critical Care, Rheumatology etc.
- Mention how you’re thinking based on the patient data.

3️⃣ **Differential Diagnoses (Ranked with Reasoning and Probability Estimates):**
- List all reasonable differentials with % probabilities.
- Keep reasoning short but focused.

4️⃣ **Recommended Investigations:** (Use Table Format)

| Investigation | Purpose | Urgency |
|----------------|---------|---------|
| .... | .... | .... |

5️⃣ **Management Plan:** (Use Table Format)

| Intervention | Dose | Route | Frequency | Notes |
|---------------|------|-------|-----------|-------|
| .... | .... | .... | .... | .... |

6️⃣ **Flowchart (Reasoning Pathway):**
- Present a simple text-based flowchart of how you’re approaching the case logically.

7️⃣ **Red Flag Alerts (Urgent):**
- List urgent signs clinicians must watch.

8️⃣ **Prognosis:**
- State likely outcome depending on response.

9️⃣ **Further Information Required (For Higher Accuracy):**
- Ask for any missing history, labs or clinical findings.

10️⃣ **Guideline Snapshot (Summarized Key Recommendations):**
- Mention which guidelines you're referencing.

11️⃣ **Supporting References (Latest Evidence Only, 2022+):**
- Always reference updated guideline bodies as provided.

12️⃣ **Disclaimer:**
This tool provides AI-generated suggestions for licensed physicians. It is not a substitute for clinical judgment or standard medical guidelines.
"""

# ------------------------------------------
# Diagnoso Brain Function
# ------------------------------------------

def generate_diagnosis(doctor_name, patient_data):
    # External API context pulling
    pubmed_context = pubmed_search(patient_data, max_results=3)
    who_context = who_guidelines_snapshot()
    cdc_context = cdc_guidelines_snapshot()

    # Static guideline snapshots
    aha_context = aha_guidelines()
    esc_context = esc_guidelines()
    ada_context = ada_guidelines()
    idsa_context = idsa_guidelines()
    ats_context = ats_guidelines()
    eular_context = eular_guidelines()

    # Inject everything into one full enriched context
    enriched_prompt = f"""
You are DIAGNOSO — a Board-Level Multispecialty AI Clinical Fellow.

Always begin your response with:
"Understood, Dr. {doctor_name}. Based on the information provided, here’s my clinical analysis:"

{system_prompt}

--- ADDITIONAL KNOWLEDGE CONTEXT ---

Recent PubMed Abstracts:
{pubmed_context}

WHO Guidelines:
{who_context}

CDC Guidelines:
{cdc_context}

AHA Guidelines:
{aha_context}

ESC Guidelines:
{esc_context}

ADA Guidelines:
{ada_context}

IDSA Guidelines:
{idsa_context}

ATS Guidelines:
{ats_context}

EULAR Guidelines:
{eular_context}
"""

    # Construct GPT request
    messages = [
        {"role": "system", "content": enriched_prompt},
        {"role": "user", "content": f"Doctor: {doctor_name}\nPatient Data: {patient_data}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.1
    )

    return response.choices[0].message["content"]
