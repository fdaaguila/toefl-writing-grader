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
    "Practice your TOEFL Writing skills and receive "
    "AI-powered feedback based on TOEFL scoring criteria."
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
# EVALUATION PROMPT
# ---------------------------------------------------------

def evaluate_writing(task_type, task_prompt, student_response):

    if task_type == "Write for an Academic Discussion":

        rubric = """
Evaluate the response using the TOEFL iBT Writing for an Academic
Discussion scoring scale from 0 to 5.

Score 5:
The response is highly effective. It clearly contributes to the
discussion, expresses ideas clearly, and provides relevant and well-
developed explanations or examples. Language use is appropriate and
generally accurate, with a good range of vocabulary and grammar.
Minor errors may occur but do not affect communication.

Score 4:
The response is effective and relevant. It clearly expresses a position
and contributes meaningfully to the discussion. Ideas are adequately
developed and supported. There may be some errors or limitations in
language use, but they generally do not interfere with communication.

Score 3:
The response is generally relevant and understandable but may be
limited in development, explanation, or support. The contribution to
the discussion may be somewhat basic or incomplete. Language errors,
limited vocabulary, or sentence structure problems may sometimes
affect clarity, but the main meaning is generally understandable.

Score 2:
The response shows limited ability to contribute to the discussion.
Ideas may be unclear, insufficiently developed, repetitive, or only
partially relevant. Language errors and limited language control may
make the response difficult to understand in places.

Score 1:
The response provides very little relevant content or does not
meaningfully contribute to the discussion. Ideas are severely limited
or unclear, and frequent language problems significantly interfere
with communication.

Score 0:
The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response
to the task.
"""

    else:

        rubric = """
Evaluate the response as a TOEFL iBT Writing "Write an Email" task.

Consider the following areas as part of the overall evaluation:

- Does the writer successfully accomplish the purpose of the email?
- Does the writer address the required points in the task?
- Is the message clear, relevant, and appropriately developed?
- Is the organization appropriate for an email?
- Is the tone appropriate for the intended recipient and situation?
- Is the language generally accurate and effective?
- Does the writer use appropriate vocabulary and sentence structures?

Give an estimated score from 0 to 5 based on the overall effectiveness
of the response.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.
"""

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Your job is to evaluate a student's response carefully and fairly.

TASK TYPE:
{task_type}

TASK PROMPT:
{task_prompt}

STUDENT RESPONSE:
{student_response}

SCORING GUIDELINES:
{rubric}

IMPORTANT EVALUATION RULES:

- Give ONE overall estimated score from 0 to 5.
- Do not give a score from 0 to 30.
- Do not calculate the score by averaging separate categories.
- Base the score on the student's actual response.
- Do not invent problems that are not present.
- Do not penalize the student simply for using simple language.
- Do not reward unnecessarily complex vocabulary or grammar.
- Focus on whether the language is effective for the task.
- Consider the student's ideas, development, relevance, organization,
  and language together when assigning the overall score.
- The score must be consistent with the rubric above.
- Keep the feedback concise and useful for a student.
- Do not write a long essay about the student's performance.
- Do not require formal research or evidence unless the task requires it.
- For Academic Discussion, the student should engage with the discussion
  and support their position, but formal academic evidence is not required.
- Do not rewrite the student's response into an unrealistically advanced
  level.
- Keep the improved version close to the student's original ideas and
  approximate language level.

Return ONLY the following sections:

## Estimated Score: X/5

## Why?
Write 2-3 concise sentences explaining why the response fits this
score according to the rubric.

## What You Did Well
- Give exactly 2 specific strengths from the student's response.

## What to Improve
- Give exactly 2 specific and actionable suggestions that would help
  the student improve their performance.

## Language Corrections
Give a maximum of 3 important corrections.

For each correction, use:

Original:
Correction:
Why:

Only include meaningful errors or improvements.
Do not correct every minor punctuation mistake.

If there are no important errors, write:
"No major language errors."

## Better Version
Write a concise improved version of the student's response.

Keep:
- The student's original main ideas.
- The student's original position or purpose.
- A similar level of complexity.

Improve:
- Clarity.
- Organization.
- Important grammar or vocabulary problems.

Do not add completely new arguments.
Do not make the response unnecessarily sophisticated.

Keep the entire evaluation concise and student-friendly.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and fair TOEFL Writing evaluator. "
                    "Follow the provided scoring criteria exactly."
                )
            },
            {
                "role": "user",
                "content": evaluation_prompt
            }
        ],
        temperature=0.2,
        max_tokens=1800
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
