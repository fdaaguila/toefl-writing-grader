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
    "Paste your TOEFL writing response here:",
    height=300,
    placeholder="Paste your writing response here..."
)

# ---------------------------------------------------------
# EVALUATION FUNCTION
# ---------------------------------------------------------

def evaluate_writing(task_type, task_prompt, student_response):

    if task_type == "Write for an Academic Discussion":

        rubric = """
Evaluate the response using the TOEFL iBT Writing for an Academic
Discussion scoring scale from 0 to 5.

Score 5:
The response is highly effective. It clearly contributes to the
discussion, expresses ideas clearly, and provides relevant and
well-developed explanations or examples. Language use is appropriate
and generally accurate, with a good range of vocabulary and grammar.
Minor errors may occur but do not affect communication.

Score 4:
The response is effective and relevant. It clearly expresses a
position and contributes meaningfully to the discussion. Ideas are
adequately developed and supported. There may be some errors or
limitations in language use, but they generally do not interfere
with communication.

Score 3:
The response is generally relevant and understandable but may be
limited in development, explanation, or support. The contribution
to the discussion may be somewhat basic or incomplete. Language
errors, limited vocabulary, or sentence structure problems may
sometimes affect clarity, but the main meaning is generally
understandable.

Score 2:
The response shows limited ability to contribute to the discussion.
Ideas may be unclear, insufficiently developed, repetitive, or only
partially relevant. Language errors and limited language control
may make the response difficult to understand in places.

Score 1:
The response provides very little relevant content or does not
meaningfully contribute to the discussion. Ideas are severely
limited or unclear, and frequent language problems significantly
interfere with communication.

Score 0:
The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.
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

Your job is to evaluate a student's response accurately and fairly.

TASK TYPE:
{task_type}

TASK PROMPT:
{task_prompt}

STUDENT RESPONSE:
{student_response}

SCORING GUIDELINES:
{rubric}

IMPORTANT EVALUATION PRINCIPLES:

1. SCORE THE RESPONSE AS IT IS.

Evaluate the student's actual writing, not a rewritten or improved
version.

2. DO NOT CONFUSE STYLE WITH ERROR.

This is extremely important.

Do NOT identify a sentence as an error simply because you would
personally express it differently.

Do NOT change language merely to make it:
- more formal
- more sophisticated
- more academic
- more concise
- more elegant
- more native-like

If the student's sentence is grammatically correct, clear, natural
enough for the context, and appropriate for the task, leave it alone.

For example, these are acceptable and should NOT be treated as
errors:

"I think that it would make a big difference."

"I believe that it would make a significant difference."

Both are grammatically correct. The second is simply a stylistic
alternative.

Likewise:

"One thing that can be improved is how fast the stories are read."

should NOT automatically be changed to:

"One aspect that could be improved is the speed at which the stories
are read."

The original sentence is clear and grammatically acceptable.

3. ONLY CORRECT REAL PROBLEMS.

Language corrections should focus on:
- grammatical errors
- incorrect word choice
- incorrect word forms
- incorrect verb forms
- missing or incorrect articles when they affect accuracy
- sentence structure problems
- expressions that are genuinely unnatural or confusing
- language that is inappropriate for the context

Do not correct a sentence simply because you prefer another style.

4. PRIORITIZE ACCURACY OVER SOPHISTICATION.

A student should not receive a lower score because they use simple
but accurate language.

Do not encourage students to replace simple correct expressions
with unnecessarily sophisticated vocabulary.

5. DO NOT OVER-CORRECT.

Give a maximum of 3 language corrections.

If the response contains fewer than 3 genuine language problems,
give fewer corrections.

If there are no meaningful language problems, write:

"No major language errors."

6. EXPLAIN WHY A CORRECTION IS NECESSARY.

Every correction must identify a genuine language problem.

Do not use explanations such as:
- "This sounds more sophisticated."
- "This improves vocabulary."
- "This is more formal."

unless the original is genuinely inappropriate for the task.

7. THE BETTER VERSION MUST STAY CLOSE TO THE ORIGINAL.

Do not rewrite the student's response simply to make it sound like
a native speaker wrote it.

Do not replace correct expressions with stylistic alternatives.

Only make changes that:
- correct genuine errors
- improve clarity when necessary
- improve organization when genuinely needed
- address missing task requirements

Keep the student's original ideas, voice, and approximate language
level.

8. DO NOT REQUIRE "EVIDENCE" UNLESS THE TASK REQUIRES IT.

For Academic Discussion, students should explain or support their
ideas, but they do not need formal academic evidence or research.

Use terms such as "explanation," "support," or "development" rather
than "evidence" when appropriate.

9. DO NOT INVENT PROBLEMS.

Base all feedback on the student's actual response.

10. DO NOT GIVE A 0-30 SCORE.

Give ONE overall estimated score from 0 to 5.

Return ONLY the following sections:

## Estimated Score: X/5

## Why?

Write 2-3 concise sentences explaining why the response fits this
score according to the scoring guidelines.

## What You Did Well

Give exactly 2 specific strengths based on the student's actual
response.

## What to Improve

Give exactly 2 specific and actionable suggestions.

Focus on the changes that would most help the student improve their
performance.

## Language Corrections

Give a maximum of 3 genuine language corrections.

For each correction, use:

Original:
Correction:
Why:

Only include real errors or problems with clarity, accuracy, or
appropriateness.

Do NOT include stylistic alternatives.

If there are no important errors, write:

"No major language errors."

## Better Version

Write a concise improved version of the student's response.

Keep the student's:
- original ideas
- original meaning
- approximate language level
- personal voice

Do not unnecessarily replace correct vocabulary or grammar.

Only change language when there is a clear reason to do so.

Do not add new arguments or ideas.

Keep the evaluation concise and student-friendly.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and fair TOEFL Writing evaluator. "
                    "Your priority is accurate evaluation, not rewriting. "
                    "Do not confuse stylistic preferences with language errors."
                )
            },
            {
                "role": "user",
                "content": evaluation_prompt
            }
        ],
        temperature=0.1,
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
