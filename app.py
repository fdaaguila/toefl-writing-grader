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

Your job is to evaluate a student's response accurately, fairly,
and pedagogically.

TASK TYPE:
{task_type}

TASK PROMPT:
{task_prompt}

STUDENT RESPONSE:
{student_response}

SCORING GUIDELINES:
{rubric}

=========================================================
IMPORTANT EVALUATION PRINCIPLES
=========================================================

1. EVALUATE THE STUDENT'S ACTUAL RESPONSE

Evaluate what the student actually wrote.

Do not evaluate a rewritten or improved version.

Base every comment on evidence from the student's response.

Do not invent weaknesses, errors, or missing information.

---------------------------------------------------------

2. THE SCORE MUST BE JUSTIFIED

Give ONE overall estimated score from 0 to 5.

The score must be consistent with the scoring guidelines.

Do not give a score from 0 to 30.

Do not calculate the score by averaging separate categories.

After assigning the score, explain specifically why the response
fits that score.

Most importantly, explain:

"Why did this response receive this score instead of the next
higher score?"

For example, if the response receives 4/5, clearly explain what
specific limitations prevent it from being a 5/5.

If the response receives 3/5, explain what prevents it from being
a 4/5.

If the response receives 5/5, explain why there are no significant
limitations that prevent the highest score.

Use specific examples from the student's response whenever possible.

Do not give generic explanations that could apply to any student.

---------------------------------------------------------

3. DO NOT CONFUSE STYLE WITH ERROR

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

If the student's sentence is grammatically correct, clear,
natural enough for the context, and appropriate for the task,
leave it alone.

For example:

"I think that it would make a big difference."

is correct and should NOT be changed to:

"I believe that it would make a significant difference."

The second version is only a stylistic alternative.

Likewise:

"One thing that can be improved is how fast the stories are read."

is clear and grammatically acceptable.

Do NOT automatically change it to:

"One aspect that could be improved is the speed at which the
stories are read."

That is a stylistic alternative, not a necessary correction.

---------------------------------------------------------

4. IDENTIFY MEANINGFUL LANGUAGE PROBLEMS

Identify language problems only when they are genuinely relevant.

Consider:

- grammar errors
- incorrect word choice
- incorrect word forms
- incorrect verb forms
- article errors when relevant
- sentence structure problems
- unclear or confusing language
- genuinely unnatural expressions
- inappropriate language for the context

Distinguish between:

A. REAL ERROR
The language is incorrect.

B. MINOR LANGUAGE ISSUE
The language is understandable but slightly unclear, vague,
awkward, or less natural in a way that is worth teaching.

C. STYLE
The sentence is correct, but another version is possible.

Only A and meaningful examples of B should appear as corrections.

Do NOT present category C as an error.

---------------------------------------------------------

5. DO NOT USE A FIXED NUMBER OF CORRECTIONS

Do NOT give a predetermined number of corrections.

The number of corrections must depend entirely on the student's
actual writing.

If there are no meaningful language problems, say:

"No major language errors."

If there are one or two meaningful problems, identify only those.

If there are several meaningful problems, identify the important
ones that would help the student improve.

Do not invent corrections simply to reach a target number.

Do not correct every minor punctuation issue unless it represents
a repeated or important problem.

---------------------------------------------------------

6. GIVE ACTIONABLE FEEDBACK

Feedback must help the student understand exactly what to do
differently.

Avoid vague advice such as:

"Develop your ideas more."

Instead, explain:

- which idea is underdeveloped
- where it appears in the response
- what information or explanation is missing
- how the student could develop it

Use examples from the student's actual response.

---------------------------------------------------------

7. DO NOT REQUIRE FORMAL EVIDENCE UNLESS THE TASK REQUIRES IT

For Academic Discussion, students should explain and support
their ideas, but they do not need formal academic evidence,
research, or citations.

Use terms such as:

- explanation
- support
- development
- example

when appropriate.

---------------------------------------------------------

8. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH

A student should not receive a lower score simply because they
use simple vocabulary or grammar.

Simple, accurate, clear language is better than unnecessarily
complex language with errors.

Do not encourage students to use sophisticated vocabulary merely
for the sake of sounding advanced.

---------------------------------------------------------

9. THE BETTER VERSION MUST BE NECESSARY

Do not rewrite the student's response unnecessarily.

If the original response is already clear and effective, say so.

If a revised version is useful, make only changes that:

- correct genuine errors
- improve clarity when necessary
- improve organization when genuinely needed
- address missing task requirements
- demonstrate how the student could reach the next score level

Preserve the student's:

- original ideas
- original meaning
- approximate language level
- personal voice

Do not replace correct language with stylistic alternatives.

Do not add completely new arguments or ideas.

=========================================================
REQUIRED FEEDBACK FORMAT
=========================================================

Return ONLY the following sections:

## Estimated Score: X/5

## Why?

Write 2-3 concise sentences explaining why the response fits this
score.

Include specific evidence from the student's response.

## Why Not the Next Score?

Explain the specific limitations that prevent the response from
receiving the next higher score.

This section is REQUIRED for scores 1-4.

Be specific and refer to the student's actual response.

For example, do not simply say:

"Your ideas need more development."

Instead, explain which idea needs more development and what the
student could add or explain.

If the response receives 5/5, write:

"This response demonstrates the characteristics of the highest
score level. There are no significant limitations that prevent it
from receiving a 5/5."

## What You Did Well

Identify the most important strengths in the student's response.

Give specific examples from the student's writing.

Do not praise something the student did not actually do.

## What to Improve

Give specific, actionable suggestions based on the limitations
identified above.

Focus on the changes that would most help the student reach the
next score level.

Do not invent weaknesses.

If the response is already very strong, explain that only minor
improvements are needed.

## Language Feedback

Identify all meaningful language problems that are relevant to
the student's performance.

For each issue, use:

Original:
Correction:
Why:

Only include genuine errors or meaningful language issues.

Do not include stylistic alternatives.

If there are no meaningful language problems, write:

"No major language errors."

## Better Version

Only provide a revised version if it adds genuine pedagogical value.

If the original is already clear and effective, state:

"Your original response is already clear and effective. No
substantial revision is necessary."

If a revision is useful, keep it close to the student's original
ideas, voice, and language level.

Do not make unnecessary stylistic changes.

Keep the entire evaluation concise, specific, and student-friendly.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and fair TOEFL Writing evaluator. "
                    "Your priority is accurate scoring and useful teaching "
                    "feedback, not rewriting. "
                    "Never confuse stylistic preferences with errors. "
                    "Never invent weaknesses or corrections."
                )
            },
            {
                "role": "user",
                "content": evaluation_prompt
            }
        ],
        temperature=0.1,
        max_tokens=2200
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
