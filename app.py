import streamlit as st
import google.generativeai as genai

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="TOEFL Writing AI Grader",
    page_icon="📝",
    layout="centered"
)

# ---------------------------------------------------------
# CONNECT TO GEMINI
# ---------------------------------------------------------

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error(
        "The Gemini API key could not be found. "
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

    model = genai.GenerativeModel(
        "gemini-2.0-flash"
    )

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Your task is to evaluate a student's TOEFL Writing response.

TASK TYPE:
{task_type}

TASK PROMPT:
{task_prompt}

STUDENT RESPONSE:
{student_response}

Evaluate the response using the following criteria:

1. TASK ACHIEVEMENT
- Does the student fully address the task?
- Are all parts of the prompt answered?
- Are the ideas relevant and sufficiently developed?

2. ORGANIZATION AND COHERENCE
- Is the response logically organized?
- Are ideas connected clearly?
- Are transitions and relationships between ideas effective?

3. LANGUAGE USE
- Grammar accuracy
- Sentence structure
- Vocabulary range and precision
- Appropriate word choice

4. COMMUNICATION
- Is the meaning clear?
- Are errors serious enough to interfere with understanding?

Provide the evaluation in this exact structure:

## Estimated Score
Give an estimated TOEFL Writing score and explain briefly why.

## Task Achievement
Give specific feedback about how well the student answered the task.

## Organization and Coherence
Give specific feedback about organization, paragraphing, and connections between ideas.

## Language Use
Identify important grammar, vocabulary, and sentence structure issues.

## What You Did Well
Give 3 specific strengths from the student's actual response.

## What You Should Improve
Give 3 specific and practical areas for improvement.

## Corrections
Identify up to 5 important errors.
For each one, show:
- Original
- Correction
- Explanation

## Improved Version
Write an improved version of the student's response.
Keep the student's original ideas as much as possible.
Do not introduce completely new ideas.

Be supportive and constructive.
Do not give generic feedback.
Use specific examples from the student's response.
"""

    response = model.generate_content(evaluation_prompt)

    return response.text


# ---------------------------------------------------------
# EVALUATE BUTTON
# ---------------------------------------------------------

if st.button("🔍 Evaluate My Writing", type="primary"):

    if not task_prompt.strip():
        st.warning("Please enter the TOEFL task or prompt.")

    elif not student_response.strip():
        st.warning("Please enter your writing response.")

    else:

        with st.spinner("Evaluating your writing..."):

            try:

                evaluation = evaluate_writing(
                    task_type,
                    task_prompt,
                    student_response
                )

                st.success("Evaluation complete!")

                st.markdown(evaluation)

            except Exception as e:

                st.error(
                    "Something went wrong while evaluating your response."
                )

                st.code(str(e))
