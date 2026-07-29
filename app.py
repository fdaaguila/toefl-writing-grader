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
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .feedback-container {
        text-align: justify;
        line-height: 1.6;
    }

    .feedback-container h2 {
        text-align: left;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .feedback-container p {
        text-align: justify;
    }

    .feedback-container li {
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
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
and pedagogically. Your evaluation must be based on the specific
task prompt, the appropriate scoring criteria, and the student's
actual writing.

TASK TYPE:
{task_type}

TASK PROMPT:
{task_prompt}

STUDENT RESPONSE:
{student_response}

SCORING GUIDELINES:
{rubric}


=========================================================
1. START WITH THE TASK REQUIREMENTS
=========================================================

Before assigning a score, carefully analyze the specific task prompt.

Identify every explicit requirement that the student was asked to
fulfill.

For example, if the task says:

"Explain what your siblings have enjoyed about the program.
Describe one aspect of the program that could be improved.
Offer to help with future events."

then evaluate whether the student:

1. Explains what the siblings enjoyed.
2. Describes one aspect that could be improved.
3. Offers to help with future events.

Check whether each requirement is:

- Not addressed
- Partially addressed
- Sufficiently addressed
- Fully and effectively addressed

Pay close attention to the exact wording of the task.

TASK FULFILLMENT IS A CENTRAL PART OF THE EVALUATION.

Do not penalize a student for failing to provide information that
the task does not require.

Do not ask a student to add additional examples or explanations if
the task requirement has already been sufficiently fulfilled.

A response does not need multiple examples for a requirement unless
the task specifically asks for them.

Do not confuse:

"The student could say more"

with:

"The student has not sufficiently fulfilled the task."

These are NOT the same.

The instruction "Write as much as you can and in complete sentences"
means that the student should provide a complete and sufficiently
developed response. It does NOT mean that longer responses should
automatically receive higher scores.

Do not lower a score simply because the student could theoretically
add more information.


=========================================================
2. EVALUATE DEVELOPMENT IN CONTEXT
=========================================================

Evaluate whether the student's ideas are sufficiently developed
for THIS PARTICULAR TASK.

Do not use a fixed rule that every response must contain multiple
examples, extensive explanations, or detailed evidence.

Consider what the student actually needs to communicate in order
to successfully accomplish the task.

For example, if a student is asked to describe one aspect of a
program that could be improved, and the student:

- clearly identifies the problem,
- explains how it affects someone,
- and suggests a possible solution,

then the requirement may already be sufficiently developed.

Do NOT lower the score simply because the student could provide
additional details.

Before saying that an idea needs more development, check whether
the student has already explained or supported that idea elsewhere
in the response.

Do not ask a student to explain something that they have already
explained.

Do not introduce new ideas that are unrelated to the student's
original response just to make the response seem more developed.

Evaluate the effectiveness and sufficiency of the student's
development, not the maximum amount of information they could
possibly include.


=========================================================
3. SCORE THE RESPONSE AS IT IS
=========================================================

Evaluate the student's actual writing.

Do not evaluate a rewritten or improved version.

Base every comment on evidence from the student's response.

Do not invent weaknesses, errors, missing information, or
unfulfilled requirements.

Give ONE overall estimated score from 0 to 5.

Do not give a score from 0 to 30.

Do not calculate the score by averaging separate categories.

The score should reflect the overall effectiveness of the response
in relation to the task and the scoring criteria.

A response that fully addresses the task requirements with relevant,
clear, and sufficiently developed ideas should not be downgraded
simply because additional information could be added.


=========================================================
4. UNDERSTAND WHAT EACH SCORE LEVEL MEANS
=========================================================

The score must reflect the actual characteristics of the student's
response.

Do not assume that a 5/5 response must be perfect.

A response can receive 5/5 even if it contains:

- a minor grammatical error,
- a slightly awkward expression,
- simple but accurate vocabulary,
- a sentence that could be stylistically improved,
- or a detail that could optionally be expanded.

A 5/5 response should be highly effective and successfully fulfill
the task. Minor imperfections do not automatically prevent a 5/5.

A 4/5 response should be effective overall but may have limitations
that genuinely distinguish it from a highly effective 5/5 response.

A 3/5 response should generally address the task and be
understandable, but it may show meaningful limitations in
development, language control, clarity, organization, or effectiveness.

A 2/5 response should show more substantial limitations. The ideas
may be insufficiently developed, unclear, repetitive, partially
relevant, or difficult to understand in places.

A 1/5 response should show severe limitations in relevant content,
task fulfillment, clarity, development, or language control.

Do not automatically give a higher score because the student
addressed every task requirement.

Task fulfillment is important, but the overall score must also
reflect the quality and effectiveness of the response.

Do not automatically give a lower score because the student uses
simple vocabulary or grammar.

Simple but accurate English is acceptable.

Do not lower a score because the response could be made "even better"
through optional stylistic improvements.


=========================================================
5. JUSTIFY THE SCORE
=========================================================

After assigning the score, explain specifically why the response
fits that score.

Your explanation must refer to the actual task requirements and
the student's response.

Do not give generic explanations that could apply to any student.

Most importantly, determine whether the response genuinely falls
below the next score level.

For scores 1-4, explain what specific limitations prevent the
response from receiving the next higher score.

The limitation must be a REAL limitation in the student's response.

Do NOT force yourself to invent a weakness.

Do NOT say that the student needs more examples simply because
examples could theoretically be added.

Do NOT say that the student needs more explanation if the task
requirements have already been sufficiently fulfilled.

Do NOT say that the student needs more sophisticated vocabulary
if the existing vocabulary is accurate and effective.

Do NOT say that the student needs more complex grammar merely
because more complex grammar is possible.

If, after carefully evaluating the task requirements and the rubric,
the response actually demonstrates the characteristics of the next
higher score, give the higher score.

For a 5/5 response, explain why the response demonstrates the
characteristics of the highest score level.


=========================================================
6. DO NOT CONFUSE STYLE WITH ERROR
=========================================================

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


=========================================================
7. LANGUAGE FEEDBACK
=========================================================

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


=========================================================
8. DO NOT USE A FIXED NUMBER OF CORRECTIONS
=========================================================

Do NOT give a predetermined number of corrections.

The number of corrections must depend entirely on the student's
actual writing.

If there are no meaningful language problems, say:

"No major language errors."

If there are one or two meaningful problems, identify only those.

If there are several meaningful problems, identify the important
ones that would help the student improve.

Do not invent corrections simply to provide more feedback.

Do not correct every minor punctuation issue unless it represents
a repeated or important problem.

The goal is useful and accurate feedback, not a long list of
feedback items.


=========================================================
9. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH
=========================================================

A student should not receive a lower score simply because they
use simple vocabulary or grammar.

Simple, accurate, clear language is better than unnecessarily
complex language with errors.

Do not encourage students to use sophisticated vocabulary merely
for the sake of sounding advanced.

Do not tell a student to use "more advanced vocabulary" unless
limited vocabulary genuinely prevents the student from expressing
their meaning clearly or effectively.

Do not tell a student to use "more complex sentence structures"
unless sentence structure limitations genuinely affect the quality
or effectiveness of the response.


=========================================================
10. DO NOT REQUIRE FORMAL EVIDENCE UNLESS THE TASK REQUIRES IT
=========================================================

For Academic Discussion, students should explain and support
their ideas, but they do not need formal academic evidence,
research, or citations.

Use terms such as:

- explanation
- support
- development
- example

when appropriate.

Do not use "evidence" as a criticism unless the task specifically
requires evidence.


=========================================================
11. GIVE SPECIFIC AND ACTIONABLE FEEDBACK
=========================================================

Feedback must help the student understand exactly what they did
well and what they need to do differently.

Avoid vague advice such as:

"Develop your ideas more."

Instead, explain:

- which idea needs improvement,
- where it appears in the response,
- what is missing,
- and how the student could improve it.

Use specific examples from the student's actual response.

Do not recommend changes that the student has already successfully
made elsewhere in the response.

Most importantly, suggestions must be appropriate to the student's
actual score level.

For a 1/5 or 2/5 response, focus on fundamental problems that
prevent the response from being effective, such as task fulfillment,
clarity, organization, development, or serious language problems.

For a 3/5 response, focus on the specific limitations that prevent
the response from being consistently effective. Do not automatically
tell the student to add more examples or use more sophisticated
language.

For a 4/5 response, focus on the relatively limited weaknesses that
prevent the response from being highly effective.

For a 5/5 response, do not invent improvements simply to give the
student something to fix. If only optional stylistic improvements
are possible, say that no substantial improvement is necessary.


=========================================================
12. THE BETTER VERSION MUST BE NECESSARY AND SCORE-APPROPRIATE
=========================================================

Do not rewrite the student's response unnecessarily.

The Better Version must demonstrate how the student's actual
response could be improved based on genuine weaknesses.

The revision must be appropriate to the student's score.

For a 1/5 response, the revision may require substantial changes
to clarity, organization, task fulfillment, development, and
language, while preserving the student's intended meaning whenever
possible.

For a 2/5 response, the revision may make several necessary changes
to improve task fulfillment, clarity, development, organization,
and language accuracy.

For a 3/5 response, make only the changes that genuinely address
the limitations preventing a higher score. Do not automatically
add extensive new examples, sophisticated vocabulary, or complex
grammar.

For a 4/5 response, make relatively minor but meaningful changes
that address the specific limitations preventing a 5/5.

For a 5/5 response, do not rewrite the response simply to make it
sound more sophisticated.

If the original response is already clear and effective, say:

"Your original response is already clear and effective.
No substantial revision is necessary."

If a revised version is useful, make only changes that:

- correct genuine errors,
- improve clarity when necessary,
- improve organization when genuinely needed,
- address a missing task requirement,
- or demonstrate how the student could reach the next score level.

Preserve the student's:

- original ideas,
- original meaning,
- approximate language level,
- and personal voice.

Do not replace correct language with stylistic alternatives.

Do not add completely new arguments or ideas.

Do not turn a student's response into an unrealistically advanced
model answer.

The Better Version should be a teaching tool, not a completely
different essay or email.


=========================================================
REQUIRED FEEDBACK FORMAT
=========================================================

Return ONLY the following sections:

## Estimated Score: X/5

## Why?

Write 2-4 concise sentences explaining why the response fits
this score.

Refer specifically to:

- the task requirements,
- how effectively the student fulfills them,
- the development of the ideas,
- language control,
- and the overall quality of the response.

Do not mention weaknesses that are not actually present.

## Why Not the Next Score?

For scores 1-4, explain the specific limitations that genuinely
prevent the response from receiving the next higher score.

This section must be based on the task requirements and the
scoring criteria.

The explanation must identify REAL score-limiting weaknesses.

Do NOT invent a weakness simply because the student could add
more information.

Do NOT say that the response needs more examples or explanations
if the task requirements have already been sufficiently fulfilled.

Do NOT recommend more sophisticated vocabulary or grammar unless
the current language genuinely limits the response.

For a score of 5/5, write:

"This response demonstrates the characteristics of the highest
score level. There are no significant limitations that prevent
it from receiving a 5/5."

## What You Did Well

Identify the most important strengths in the student's response.

Give specific examples from the student's writing.

Connect the strengths to the task requirements whenever possible.

Do not praise something the student did not actually do.

## What to Improve

Give specific, actionable suggestions based on genuine limitations
in the response.

Focus on the changes that would most help the student reach the
next score level.

Make sure the suggestions match the student's actual score.

Do not automatically recommend:

- more examples,
- more details,
- more sophisticated vocabulary,
- or more complex grammar

unless these are genuinely necessary to reach the next score level.

Do not invent weaknesses.

If the response is already very strong, explain that only minor
improvements are needed.

Do not recommend adding information that is already present.

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

The revision must address the student's actual weaknesses and
must be appropriate for the student's score level.

Do not automatically make the response longer.

Do not automatically add examples.

Do not automatically use more advanced vocabulary.

Do not automatically use more complex grammar.

If the original is already clear and effective, state:

"Your original response is already clear and effective.
No substantial revision is necessary."

If a revision is useful, keep it close to the student's original
ideas, voice, meaning, and approximate language level.

Do not make unnecessary stylistic changes.

Keep the entire evaluation concise, specific, accurate,
and student-friendly.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and fair TOEFL Writing evaluator. "
                    "Your priority is accurate evaluation, not rewriting. "
                    "Do not confuse stylistic preferences with language errors. "
                    "Never invent weaknesses, missing task requirements, "
                    "or language corrections. "
                    "The student's score must be based on the actual response "
                    "and the specific task requirements."
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

                # -------------------------------------------------
                # DISPLAY FEEDBACK
                # -------------------------------------------------

                st.markdown(
                    f'<div class="feedback-container">{evaluation}</div>',
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(
                    "Something went wrong while evaluating "
                    "your response."
                )

                st.code(
                    str(e)
                )
