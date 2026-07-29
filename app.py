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
# CUSTOM STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Justify paragraphs and list text */
    .stMarkdown p {
        text-align: justify;
        line-height: 1.6;
    }

    .stMarkdown li {
        text-align: justify;
        line-height: 1.6;
    }

    /* Improve readability of headings */
    .stMarkdown h2 {
        margin-top: 1.5rem;
        margin-bottom: 0.7rem;
    }

    /* Improve spacing */
    .stMarkdown {
        font-size: 16px;
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

    # ---------------------------------------------------------
    # RUBRIC: ACADEMIC DISCUSSION
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # RUBRIC: WRITE AN EMAIL
    # ---------------------------------------------------------

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

Give ONE estimated overall score from 0 to 5 based on the overall
effectiveness of the response.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.

IMPORTANT:

A response should NOT receive a lower score simply because the
student could theoretically add more details, examples, explanations,
or supporting information.

First determine whether the student has sufficiently fulfilled the
actual requirements of the task.

If all required points are addressed clearly and sufficiently,
do not claim that the student needs more examples or more development
unless the lack of development genuinely prevents effective
communication or affects the scoring criteria.

Do not require multiple examples unless the task specifically
requires them.

Do not confuse "the student could say more" with "the student has
not sufficiently fulfilled the task."
"""

    # ---------------------------------------------------------
    # MAIN EVALUATION PROMPT
    # ---------------------------------------------------------

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

Do not ask a student to add additional examples or explanations
if the task requirement has already been sufficiently fulfilled.

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

IMPORTANT:

If the student has fulfilled all explicit task requirements,
do not invent a missing requirement.

Do not claim that a response lacks development simply because it
could contain additional optional information.

Optional additional examples, explanations, or details should NOT
be treated as score-limiting weaknesses when the task has already
been sufficiently fulfilled.


=========================================================
2. EVALUATE DEVELOPMENT IN CONTEXT
=========================================================

Evaluate whether the student's ideas are sufficiently developed
for THIS PARTICULAR TASK.

Do not use a fixed idea that every response must contain multiple
examples, extensive explanations, or detailed evidence.

Consider what the student actually needs to communicate in order
to successfully accomplish the task.

For example, if a student is asked to describe one aspect of a
program that could be improved, and the student:

- clearly identifies the problem,
- explains how it affects someone,
- and suggests one or more possible solutions,

then the requirement may already be sufficiently developed.

Do NOT lower the score simply because the student could provide
additional details.

Before saying that an idea needs more development, check whether
the student has already explained or supported that idea elsewhere
in the response.

Do not ask the student to explain something that they have already
explained.

Do not introduce new ideas that are unrelated to the student's
original response just to make the response seem more developed.

Evaluate the effectiveness and sufficiency of the student's
development, not the maximum amount of information they could
possibly include.

IMPORTANT SCORING DISTINCTION:

If a response fulfills the task requirements but contains
noticeable grammatical errors, limited language control, or
sentence structure problems, the score should reflect those actual
language limitations.

Do NOT incorrectly claim that the response is weaker because it
needs "more examples" when the actual reason it falls below the
next score level is language accuracy or language control.

Likewise, do not use lack of development as an excuse to lower a
score when the student's ideas are already sufficiently developed
for the task.


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

A response that fulfills the task but contains frequent or noticeable
language errors should be evaluated according to the effect and
frequency of those errors.

Do not ignore language problems simply because the task requirements
are fulfilled.

At the same time, do not invent language problems that are not
actually present.


=========================================================
4. UNDERSTAND WHAT A 5/5 MEANS
=========================================================

Do not assume that a 5/5 response must be perfect.

A response can receive 5/5 even if it contains:

- a minor grammatical error,
- a slightly awkward expression,
- simple but accurate vocabulary,
- a sentence that could be stylistically improved,
- or a detail that could optionally be expanded.

A 5/5 response should be highly effective and successfully fulfill
the task.

Minor imperfections do not automatically prevent a 5/5.

Do not lower a score because the response could be made "even better"
through optional stylistic improvements.

Only identify score-limiting weaknesses when they genuinely affect
the effectiveness of the response according to the scoring criteria.

Simple vocabulary is NOT automatically a weakness.

Simple sentence structures are NOT automatically a weakness.

A response should not be downgraded simply because it does not use
advanced or sophisticated vocabulary if the language is accurate,
clear, and effective.


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

However, do NOT force yourself to invent a weakness.

If, after carefully evaluating the task requirements and the rubric,
the response actually demonstrates the characteristics of the next
higher score, give the higher score.

Do not lower a score merely because there are optional ways to make
the response longer, more detailed, or more sophisticated.

For a 5/5 response, explain why the response demonstrates the
characteristics of the highest score level.

IMPORTANT:

When explaining why a response did not receive the next score,
identify the REAL score-limiting factor.

Possible factors may include:

- incomplete task fulfillment,
- insufficient development that genuinely affects effectiveness,
- unclear organization,
- inappropriate tone,
- frequent grammatical errors,
- limited language control,
- unclear meaning,
- repetitive or irrelevant ideas.

Do NOT automatically use:

- "needs more examples"
- "needs more details"
- "needs more sophisticated vocabulary"
- "needs more complex sentence structures"

unless these are genuinely necessary according to the task and
scoring criteria.


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

Do not present stylistic alternatives as errors.


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

If a sentence is grammatically correct but could be expressed in a
more sophisticated way, do not list it as a correction.

If a sentence is simple but correct, leave it alone.


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

When a response contains several genuine language problems,
prioritize the problems that are most important for improving
accuracy and language control.


=========================================================
9. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH
=========================================================

A student should not receive a lower score simply because they
use simple vocabulary or grammar.

Simple, accurate, clear language is better than unnecessarily
complex language with errors.

Do not encourage students to use sophisticated vocabulary merely
for the sake of sounding advanced.

Do not describe simple but correct vocabulary as a weakness.

Do not describe simple but correct sentence structures as a
weakness.

If a response is weaker because of language, identify the actual
problem, such as:

- grammatical inaccuracy,
- incorrect word choice,
- limited control,
- unclear sentence structure,
- or frequent errors.

Do not replace "simple" with "weak."


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

If the main weakness is language accuracy, give language-focused
advice.

If the main weakness is task fulfillment, give task-focused advice.

If the main weakness is development, identify the specific idea
that genuinely needs development.

Do not give generic advice that does not match the actual response.


=========================================================
12. THE BETTER VERSION MUST BE NECESSARY
=========================================================

Do not rewrite the student's response unnecessarily.

The Better Version should primarily demonstrate how the student's
actual response could be improved based on genuine problems.

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

IMPORTANT:

Do not automatically add new examples, explanations, supporting
details, or arguments to the Better Version.

If the student has already fulfilled all task requirements,
focus the revision on genuine language problems and necessary
clarity improvements.

If the response is a lower-level response, the Better Version may
include reasonable improvements in organization, clarity, and
development only when those improvements are genuinely needed
to demonstrate a stronger response.

However, do not transform a student's response into an unrealistically
advanced model answer.

The Better Version should remain recognizably based on the student's
original response.


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
- and the overall quality of the response.

If language problems are an important reason for the score,
mention them specifically.

Do not claim that the student needs more examples or development
unless this is genuinely a score-limiting issue.

## Why Not the Next Score?

For scores 1-4, explain the specific limitations that genuinely
prevent the response from receiving the next higher score.

This section must be based on the task requirements and the
scoring criteria.

Do NOT invent a weakness simply because the student could add
more information.

Do NOT say that the response needs more examples or explanations
if the task requirements have already been sufficiently fulfilled.

Do NOT say that the student needs more sophisticated vocabulary
simply because the vocabulary is simple.

Do NOT say that the student needs more complex sentence structures
simply because the sentences are simple.

If the actual limitation is language accuracy or language control,
say so clearly and refer to the actual errors.

If the response genuinely demonstrates the characteristics of
the next higher score, assign the higher score instead.

For a score of 5/5, write:

"This response demonstrates the characteristics of the highest
score level. There are no significant limitations that prevent
it from receiving a 5/5."

## What You Did Well

Identify the most important strengths in the student's response.

Give specific examples from the student's writing.

Connect the strengths to the task requirements whenever possible.

Do not praise something the student did not actually do.

Do not give generic praise.

## What to Improve

Give specific, actionable suggestions based on genuine limitations
in the response.

Focus on the changes that would most help the student reach the
next score level.

Do not invent weaknesses.

If the response is already very strong, explain that only minor
improvements are needed.

Do not recommend adding information that is already present.

Do not recommend additional examples simply because more examples
are possible.

If the main weakness is language accuracy, focus the suggestions
on language accuracy.

If the main weakness is task fulfillment, focus the suggestions
on task fulfillment.

If the main weakness is development, identify the specific
development problem.

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

The "Why" explanation must explain the actual language problem.

Do not say that a correction is necessary because it is:

- more sophisticated,
- more formal,
- more academic,
- more natural-sounding,

unless the original expression is genuinely inappropriate,
unclear, or incorrect.

## Better Version

Only provide a revised version if it adds genuine pedagogical value.

If the original is already clear and effective, state:

"Your original response is already clear and effective.
No substantial revision is necessary."

If a revision is useful, keep it close to the student's original
ideas, voice, and language level.

Correct genuine errors first.

Improve clarity or organization only when necessary.

Do not add new arguments or ideas.

Do not add optional examples simply to make the response longer.

Do not unnecessarily replace correct vocabulary or grammar.

Do not transform a basic but correct response into an advanced
native-speaker model.

Keep the entire evaluation concise, specific, accurate,
and student-friendly.
"""

    # ---------------------------------------------------------
    # CALL GROQ
    # ---------------------------------------------------------

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and fair TOEFL Writing evaluator. "
                    "Your priority is accurate evaluation, not rewriting. "
                    "Follow the provided scoring criteria carefully. "
                    "Evaluate task fulfillment before suggesting additional "
                    "development. "
                    "Do not confuse stylistic preferences with language errors. "
                    "Do not penalize simple but correct English. "
                    "Do not invent weaknesses, errors, or missing task requirements. "
                    "When a response is weaker because of language accuracy, "
                    "identify the actual language problems rather than claiming "
                    "that optional additional details are required."
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
