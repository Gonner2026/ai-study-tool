from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class TopicRequest(BaseModel):
    topic: str

# Function to call OpenAI API
def ask_openai(prompt: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful medical tutor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")

# --- Routes ---

@app.post("/step1-pathophys")
def step1_pathophys(request: TopicRequest):
    prompt = f"""Summarize the pathophysiology, clinical features, diagnosis, treatment, key buzzwords, mnemonic, and example presentation of {request.topic} for USMLE Step 1.
Respond in markdown with bold section headers."""
    return ask_openai(prompt)

@app.post("/step1-anki")
def step1_anki(request: TopicRequest):
    prompt = f"""Create 5 Anki-style Cloze flashcards for USMLE Step 1 about {request.topic} using the {{c1::...}} format."""
    return ask_openai(prompt)

@app.post("/step1-questions")
def step1_questions(request: TopicRequest):
    prompt = f"""You are an NBME item writer for the USMLE Step 1 exam.

Using the following topic: {request.topic}

Write TWO board-style foundational science MCQs that include:
- Header: "#GPT (Foundational)"
- Clinical vignette
- One of these lead-ins: "Which of the following is the most likely cause/mechanism/etc?"
- 5 homogeneous answer choices labeled A–E
- The correct answer labeled only in the explanation (do not mark above)
- A 2–3 sentence tutor-style explanation of how to approach the question
- A markdown table comparing why each incorrect answer is wrong and what clinical clue would have made it correct
- A summary of why the correct answer is right
- Label the tested competency and writing principle used
- End each question with '---'

Make sure each question tests foundational understanding (e.g. enzymes, pathophysiology, mechanisms, cytokines, lesions).
Format in Markdown."""
    return ask_openai(prompt)

@app.post("/step2-overview")
def step2_overview(request: TopicRequest):
    prompt = f"""Give a clinical overview of {request.topic} for USMLE Step 2 CK including presentation, key labs/imaging, diagnosis, and first-line treatment.
Respond in markdown with bolded section titles."""
    return ask_openai(prompt)

@app.post("/step2-questions")
def step2_questions(request: TopicRequest):
    prompt = f"""You are an NBME item writer for the USMLE Step 2 CK exam.

Using the following topic: {request.topic}

Write TWO clinical vignette MCQs that include:
- Header: "#GPT (Clinical)"
- Clinical scenario with labs/imaging if needed
- Lead-in such as "What is the next best step in management?" or "What is the most appropriate pharmacotherapy?"
- 5 answer choices labeled A–E
- Correct answer explained (but not marked in the choices)
- A 2–3 sentence tutor-style explanation of the reasoning process
- A markdown table explaining why the other 4 answer choices are incorrect
- A brief educational summary explaining why the correct answer is best
- Label the clinical competency tested and writing principles used
- End each question with '---'

Ensure questions follow NBME exam standards and resemble actual USMLE practice questions.
Format in Markdown."""
    return ask_openai(prompt)

@app.post("/differential-builder")
def differential_builder(request: TopicRequest):
    prompt = f"""A patient presents with: {request.topic}
Generate:
- Top 5 differential diagnoses
- Key distinguishing clinical features for each
- Classic USMLE buzzwords
- One-liner diagnosis clue per condition
Respond in markdown with bold headers."""
    return ask_openai(prompt)

@app.post("/management-tree")
def management_tree(request: TopicRequest):
    prompt = f"""Create a simplified USMLE Step 2 CK management algorithm for: {request.topic}.
Include:
- Initial steps
- Key labs/imaging
- First-line treatment
- Escalation steps
- When to refer or hospitalize
Use bullet points with bold headers and arrows (→) to show decision flow."""
    return ask_openai(prompt)

@app.post("/case-breakdown")
def case_breakdown(request: TopicRequest):
    prompt = f"""Break down the following case topic for a USMLE Step 2 CK student: {request.topic}
Include:
- Likely Diagnosis
- Key clinical clues
- Diagnostic steps
- Management steps
- High-yield teaching point
- 2 Anki-style cloze flashcards
Respond in markdown."""
    return ask_openai(prompt)

@app.post("/vignette-breakdown")
def vignette_breakdown(request: TopicRequest):
    prompt = f"""You are a USMLE tutor. A student presents this case:
{request.topic}
Provide:
- Key Buzzwords
- Diagnosis
- Pathophysiology
- Next Step in Management (USMLE-style)
- High-Yield Pearl
- Anki-style Flashcards in cloze {{c1::...}} format
Respond in markdown."""
    return ask_openai(prompt)

@app.post("/quick-differential")
def quick_differential(request: TopicRequest):
    prompt = f"""Topic: {request.topic}
Generate:
- 5 most likely differential diagnoses
- Key distinguishing clinical features for each
- One-liner USMLE-style diagnosis clues
- Mnemonic if applicable
Respond in markdown."""
    return ask_openai(prompt)

@app.post("/anki-generator")
def anki_generator(request: TopicRequest):
    prompt = f"""Topic: {request.topic}
Create 5 Anki-style cards in the following format:
- Question:
- Answer:
- Explanation:
- Tag: [e.g., Path, Immuno, Nephro]
Use concise language suitable for Step 1/2 review."""
    return ask_openai(prompt)

@app.post("/ask-anything")
def ask_anything(request: TopicRequest):
    prompt = f"""The user asks: {request.topic}
Please provide a thoughtful, helpful answer. Use markdown formatting if needed."""
    return ask_openai(prompt)
