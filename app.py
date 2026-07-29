import streamlit as st
from groq import Groq

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="TOEFL Writing AI Grader",
    page_icon="📝",
    layout="centered"
)

# ---------------------------------------------------------
# CONNECT TO GROQ
# ---------------------------------------------------------

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error(
        "The Groq API key could not be found. "
        "Please check your Streamlit Secrets."
    )
    st.stop()

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("📝 TOEFL Writing AI Grader")

st.write(
    "Practice your TOEFL Writing skills and receive AI-powered "
    "feedback based on TOEFL scoring criteria."
)

st.info(
    "This tool provides an AI-estimated practice score. "
    "It is not an official ETS score."
)

# ---------------------------------------------------------
# TASK SELECTION
# ---------------------------------------------------------

task_type = st.selectbox(
    "Choose your TOEFL Writing task:",
    [
        "Write an Email",
        "Write for an Academic Discussion"
    ]
)

# ---------------------------------------------------------
# TASK PROMPT
# ---------------------------------------------------------

st.subheader("TOEFL Task")

task_prompt = st.text_area(
    "Paste the TOEFL task or prompt here:",
    height=200,
    placeholder="Paste the complete TOEFL task here..."
)

# ---------------------------------------------------------
# STUDENT RESPONSE
# ---------------------------------------------------------

st.subheader("Your Response")

student_response = st.text_area(
    "Paste your response here:",
    height=300,
    placeholder="Paste your TOEFL writing response here..."
)

# ---------------------------------------------------------
# EVALUATION FUNCTION
# ---------------------------------------------------------

def evaluate_writing(task_type, task_prompt, student_response):

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Evaluate the student's writing response carefully.

TASK TYPE:
{task_type}

TASK PROMPT:
{task_prompt}

STUDENT RESPONSE:
{student_response}

Evaluate the response based on:

1. TASK ACHIEVEMENT
- Does the student address the task?
- Does the response answer the prompt appropriately?
- Are ideas relevant and developed?

2. ORGANIZATION AND COHERENCE
- Is the response logically organized?
- Are ideas connected clearly?
- Are transitions used effectively?

3. LANGUAGE USE
- Grammar accuracy
- Sentence structure
- Vocabulary range and precision
- Word choice

4. CLARITY
- Is the student's meaning clear?
- Do language errors interfere with communication?

Provide your evaluation using this structure:

## Estimated Score
Give an estimated TOEFL Writing score and briefly explain the score.

## Task Achievement
Explain how effectively the student addressed the task.
Use specific examples from the response.

## Organization and Coherence
Comment on organization, development, and connections between ideas.

## Language Use
Comment on grammar, vocabulary, sentence structure, and word choice.

## What You Did Well
Give 3 specific strengths based on the student's actual response.

## What You Should Improve
Give 3 specific and practical suggestions.

## Corrections
Identify up to 5 important errors.

For each error, use:

Original:
Correction:
Explanation:

## Improved Version
Write an improved version of the student's response.
Keep the student's original ideas and meaning.
Do not introduce completely new ideas.

Be supportive and constructive.
Avoid generic feedback.
Use specific examples from the student's response.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert English teacher "
                    "and TOEFL Writing evaluator."
                )
            },
            {
                "role": "user",
                "content": evaluation_prompt
            }
        ],
        temperature=0.2,
        max_tokens=3000
    )

    return response.choices[0].message.content


# ---------------------------------------------------------
# EVALUATE BUTTON
# ---------------------------------------------------------

if st.button("🔍 Evaluate My Writing", type="primary"):

    if not task_prompt.strip():

        st.warning(
            "Please enter the TOEFL task or prompt."
        )

    elif not student_response.strip():

        st.warning(
            "Please enter your writing response."
        )

    else:

        with st.spinner(
            "Evaluating your writing..."
        ):

            try:

                evaluation = evaluate_writing(
                    task_type,
                    task_prompt,
                    student_response
                )

                st.success(
                    "Evaluation complete!"
                )

                st.markdown(
                    evaluation
                )

            except Exception as e:

                st.error(
                    "Something went wrong while evaluating "
                    "your response."
                )

                st.code(
                    str(e)
                )
