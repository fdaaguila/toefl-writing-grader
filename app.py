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

    /* Main text */
    .stMarkdown p,
    .stMarkdown li {
        text-align: justify;
        line-height: 1.65;
    }

    /* Headings */
    .stMarkdown h2 {
        margin-top: 1.5rem;
        margin-bottom: 0.7rem;
    }

    /* Evaluation result container */
    .evaluation-box {
        padding: 10px 5px;
    }

    /* Improve spacing between sections */
    .stMarkdown {
        margin-bottom: 8px;
    }

    /* Make score stand out */
    .score-highlight {
        font-size: 1.35rem;
        font-weight: 700;
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

    # -----------------------------------------------------
    # SCORING RUBRIC
    # -----------------------------------------------------

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

Give ONE estimated overall score from 0 to 5.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.

The overall score must reflect the combined quality of the response.
Completing all task requirements does NOT automatically guarantee a
4 or 5. However, fulfilling the task requirements should also NOT
be penalized simply because the student could theoretically provide
more information.

Evaluate the response according to the quality expected at each
score level.
"""

    # -----------------------------------------------------
    # EVALUATION PROMPT
    # -----------------------------------------------------

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Your job is to evaluate a student's response accurately, fairly,
and pedagogically.

Your evaluation must be based on:

1. The specific task prompt.
2. The appropriate scoring criteria.
3. The student's actual writing.
4. The overall effectiveness of the response.

Do NOT evaluate a rewritten or improved version of the response.

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

At the same time, do not assume that completing every task requirement
automatically makes a response a 4 or 5.

Task fulfillment is ONE important part of the evaluation. The final
score must also reflect the quality of development, language control,
clarity, organization, and overall effectiveness described in the
scoring guidelines.


=========================================================
2. EVALUATE DEVELOPMENT IN CONTEXT
=========================================================

Evaluate whether the student's ideas are sufficiently developed
for THIS PARTICULAR TASK.

Do not use a fixed rule that every response must contain:

- multiple examples,
- extensive explanations,
- formal evidence,
- highly detailed support,
- sophisticated arguments,
- or long paragraphs.

Consider what the student actually needs to communicate in order
to successfully accomplish THIS task.

For example, if a student is asked to describe one aspect of a
program that could be improved, and the student:

- clearly identifies the problem,
- explains how it affects someone,
- and suggests one or more possible solutions,

then the requirement may already be sufficiently developed.

Do NOT lower the score simply because the student could provide
additional optional details.

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

IMPORTANT:

"More detail would be possible" is NOT automatically the same as
"the response is insufficiently developed."

Only identify limited development when the lack of development
genuinely affects the effectiveness of the response or is relevant
to the score level.


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

However, task fulfillment alone does not automatically justify a
high score.

A response may fulfill every explicit task requirement and still
receive a lower score if:

- language errors are frequent or affect clarity,
- ideas are unclear or insufficiently developed,
- organization makes the message difficult to follow,
- the tone is inappropriate,
- the response is only partially understandable,
- or the overall effectiveness is limited.

Conversely, a response with simple language can still receive a
high score if the language is accurate, clear, effective, and
appropriate for the task.

Use the scoring rubric to determine the final score.


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

Do not require sophisticated vocabulary or complex grammar for a 5/5.

Simple but accurate language can receive a 5/5 when it is effective
for the task.


=========================================================
5. CALIBRATE SCORES CAREFULLY
=========================================================

Use the following general principles when distinguishing score levels.

SCORE 5:

The response is highly effective.

It successfully fulfills the task, communicates clearly, and
demonstrates strong overall control of language.

Minor errors or awkward expressions may occur, but they do not
meaningfully reduce effectiveness.

Do not lower a 5 to a 4 merely because the student could add more
details or use more sophisticated vocabulary.

SCORE 4:

The response is effective overall.

It fulfills the task and communicates its ideas clearly, but there
are noticeable limitations that genuinely distinguish it from the
highest level.

Possible limitations may include:

- some language errors,
- occasional awkward expressions,
- somewhat limited development,
- some limitations in organization,
- or less consistent language control.

However, do NOT invent limitations simply to justify a 4.

Do not say that a response is a 4 because it "could use more detail"
if the task has already been sufficiently fulfilled and the ideas
are adequately developed.

SCORE 3:

The response is generally understandable and relevant but has
meaningful limitations.

These may include:

- noticeable grammatical errors,
- limited language control,
- limited development,
- basic or incomplete support,
- awkward or unclear expressions,
- repetitive language,
- or weaknesses in organization.

A response may fulfill all explicit task requirements and still
receive a 3 if the overall language control or effectiveness is
clearly below the level expected for a 4.

Do not automatically give a 4 simply because all task requirements
are present.

At the same time, do not give a 3 simply because the language is
simple.

Simple language is acceptable if it is accurate and effective.

SCORE 2:

The response demonstrates limited ability.

There are substantial problems with one or more of the following:

- task fulfillment,
- clarity,
- development,
- organization,
- language control,
- or relevance.

The response may be understandable in places but has significant
limitations that prevent effective communication.

SCORE 1:

The response demonstrates very limited ability.

The content is severely limited, unclear, largely irrelevant,
or difficult to understand because of frequent language problems.

SCORE 0:

Use 0 only when the response meets the conditions described in
the scoring guidelines, such as being blank, copied from the prompt,
completely irrelevant, not written in English, or not providing a
meaningful response.

Do not give 0 simply because the writing contains many errors.


=========================================================
6. JUSTIFY THE SCORE
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

The reason for the score must be consistent with the actual response.

For example, do NOT say:

"Your response needs more examples"

if the task did not require additional examples and the student's
ideas are already sufficiently developed.

Do NOT say:

"Your vocabulary needs to be more sophisticated"

if the student's vocabulary is simple but accurate and effective.

Do NOT say:

"Your language needs to be more varied"

unless limited language variety genuinely affects the effectiveness
of the response or is relevant to the scoring criteria.


=========================================================
7. DO NOT CONFUSE STYLE WITH ERROR
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

IMPORTANT DISTINCTION:

A sentence can be:

A. Grammatically incorrect.

B. Grammatically correct but somewhat awkward or less natural.

C. Grammatically correct and natural.

Do not treat B as if it were A.

If a sentence is understandable but somewhat awkward, identify it
as a minor language issue only if it is genuinely useful for the
student to learn.

Do not exaggerate the seriousness of minor awkwardness.


=========================================================
8. LANGUAGE FEEDBACK
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

Example:

"My younger sister like the stories."

Correction:

"My younger sister likes the stories."

B. MINOR LANGUAGE ISSUE

The language is understandable but slightly unclear, vague,
awkward, or less natural in a way that is worth teaching.

Example:

"My siblings like very much the reading program."

This is understandable, but the word order is unnatural.

A possible correction is:

"My siblings really like the reading program."

However, do NOT describe the original as completely
"grammatically incorrect" if the main problem is unnatural
word order.

C. STYLE

The sentence is correct, but another version is possible.

Only A and meaningful examples of B should appear as corrections.

Do NOT present category C as an error.


=========================================================
9. DO NOT USE A FIXED NUMBER OF CORRECTIONS
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
corrections.

IMPORTANT:

Do not correct correct sentences.

Do not provide a stylistic alternative and label it as a correction.

Do not rewrite every sentence merely because a native speaker might
phrase it differently.


=========================================================
10. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH
=========================================================

A student should not receive a lower score simply because they
use simple vocabulary or grammar.

Simple, accurate, clear language is better than unnecessarily
complex language with errors.

Do not encourage students to use sophisticated vocabulary merely
for the sake of sounding advanced.

Do not recommend "more varied vocabulary" unless limited vocabulary
actually affects clarity, precision, or effectiveness.

Do not recommend "more complex sentence structures" simply because
the student uses simple sentences.

Recommend greater complexity only when the student's language
control or development genuinely limits the response.


=========================================================
11. DO NOT REQUIRE FORMAL EVIDENCE UNLESS THE TASK REQUIRES IT
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
12. GIVE SPECIFIC AND ACTIONABLE FEEDBACK
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

Suggestions must be appropriate for the student's actual score level.

For a low-scoring response, prioritize the most important problems
first, such as:

- completing missing task requirements,
- improving basic clarity,
- correcting frequent grammatical errors,
- or making the main message understandable.

For a mid-level response, focus on genuine limitations that prevent
a higher score.

For a high-level response, focus only on minor improvements that
would genuinely strengthen the response.

Do not give the same advice to every student regardless of score.


=========================================================
13. THE BETTER VERSION MUST BE NECESSARY
=========================================================

Do not rewrite the student's response unnecessarily.

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

The Better Version must be appropriate for the student's score.

For a score of 1 or 2:

Focus on making the response understandable, relevant, and complete.
Correct the most important language problems.
Address missing task requirements if necessary.
Do not transform the response into advanced English.

For a score of 3:

Correct genuine language problems and improve clarity or development
only where necessary to demonstrate what would move the response
toward a 4.

Do not add unnecessary sophisticated vocabulary or completely new
ideas.

For a score of 4:

Make only targeted changes that address the actual limitations
preventing a 5.

Do not rewrite the response simply to make it sound more native-like.

For a score of 5:

If the response is already effective, do not rewrite it.

State:

"Your original response is already clear and effective.
No substantial revision is necessary."

Do not create an artificial revision simply because the section
is called "Better Version."


=========================================================
14. FINAL QUALITY CHECK BEFORE RESPONDING
=========================================================

Before producing the evaluation, silently check:

1. Did I evaluate the exact task requirements?
2. Did I score the student's actual response?
3. Did I distinguish task fulfillment from overall score?
4. Did I avoid inventing missing development?
5. Did I avoid requiring unnecessary examples?
6. Did I distinguish genuine errors from stylistic alternatives?
7. Did I avoid penalizing simple but correct English?
8. Did I identify only genuine language problems?
9. Is the Better Version appropriate for the student's score?
10. Does the explanation for the score match the actual weaknesses?
11. If I gave a 4, is there a genuine reason it is not a 5?
12. If I gave a 3, is there a genuine reason it is not a 4?
13. If I gave a 2, is there a genuine reason it is not a 3?
14. Am I recommending changes that the student has already made?
15. Am I recommending more detail only because I personally prefer
more detail, or because the task/rubric genuinely requires it?

If a response genuinely demonstrates the next score level,
assign the higher score.

Do not lower scores simply to create a "Why Not the Next Score?"
explanation.


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

Do not mention weaknesses that do not genuinely affect the score.

## Why Not the Next Score?

For scores 1-4, explain the specific limitations that genuinely
prevent the response from receiving the next higher score.

This section must be based on the task requirements and the
scoring criteria.

Do NOT invent a weakness simply because the student could add
more information.

Do NOT say that the response needs more examples or explanations
if the task requirements have already been sufficiently fulfilled.

Do NOT say that the vocabulary needs to be more sophisticated
unless this genuinely affects the score.

Do NOT say that the grammar needs to be more complex unless this
genuinely affects the score.

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

## What to Improve

Give specific, actionable suggestions based on genuine limitations
in the response.

Focus on the changes that would most help the student reach the
next score level.

Do not invent weaknesses.

If the response is already very strong, explain that only minor
improvements are needed.

Do not recommend adding information that is already present.

Do not recommend more sophisticated vocabulary or grammar unless
the current language genuinely limits the response.

## Language Feedback

Identify all meaningful language problems that are relevant to
the student's performance.

For each issue, use:

Original:
Correction:
Why:

Only include genuine errors or meaningful language issues.

Do not include stylistic alternatives.

Distinguish between:

- genuine grammatical errors,
- minor language issues,
- and stylistic alternatives.

Only the first two should be included.

If there are no meaningful language problems, write:

"No major language errors."

## Better Version

Only provide a revised version if it adds genuine pedagogical value.

If the original is already clear and effective, state:

"Your original response is already clear and effective.
No substantial revision is necessary."

If a revision is useful, keep it close to the student's original
ideas, voice, and language level.

Do not make unnecessary stylistic changes.

Do not add completely new arguments or ideas.

The revision should be appropriate for the student's score level.

Keep the entire evaluation concise, specific, accurate,
and student-friendly.
"""

    # -----------------------------------------------------
    # CALL GROQ
    # -----------------------------------------------------

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and fair TOEFL Writing evaluator. "
                    "Follow the provided scoring criteria carefully. "
                    "Your priority is accurate evaluation and useful "
                    "teaching feedback, not rewriting. "
                    "Never confuse stylistic preferences with genuine "
                    "language errors. "
                    "Never invent weaknesses, missing requirements, "
                    "or language problems. "
                    "Do not automatically lower a score because a "
                    "student could theoretically add more information. "
                    "Do not automatically give a high score simply because "
                    "the student mentions every task requirement."
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
