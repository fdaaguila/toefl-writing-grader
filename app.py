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

    /* Justified text for AI feedback */
    .stMarkdown {
        text-align: justify;
        line-height: 1.6;
    }

    /* Improve readability of headings */
    .stMarkdown h2 {
        margin-top: 1.5rem;
        margin-bottom: 0.6rem;
    }

    /* Improve readability of text areas */
    textarea {
        line-height: 1.5 !important;
    }

    /* Improve readability of information boxes */
    .stAlert {
        line-height: 1.5;
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

    client = Groq(
        api_key=api_key
    )

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

def evaluate_writing(
    task_type,
    task_prompt,
    student_response
):

    # -----------------------------------------------------
    # ACADEMIC DISCUSSION RUBRIC
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
not written in English, or does not provide a meaningful response.
"""

    # -----------------------------------------------------
    # EMAIL RUBRIC
    # -----------------------------------------------------

    else:

        rubric = """
Evaluate the response as a TOEFL iBT Writing "Write an Email" task.

Consider the following areas as part of the overall evaluation:

1. TASK FULFILLMENT

Does the writer successfully accomplish the purpose of the email?

Does the writer address all the required points in the task?

2. DEVELOPMENT

Are the required ideas sufficiently explained or supported for
THIS PARTICULAR TASK?

Do not automatically require multiple examples or extensive
explanations.

Do not lower the score simply because the student could theoretically
say more.

3. ORGANIZATION

Is the message logically organized and easy to follow?

4. TONE AND APPROPRIATENESS

Is the tone appropriate for the intended recipient and situation?

5. LANGUAGE CONTROL

Is the language accurate and effective?

Consider:

- grammar
- sentence structure
- word choice
- word forms
- verb forms
- subject-verb agreement
- articles
- clarity
- naturalness
- vocabulary control

A response with frequent grammatical errors, awkward expressions,
or incorrect structures should not receive the highest scores simply
because all task requirements are addressed.

TASK FULFILLMENT AND LANGUAGE CONTROL MUST BOTH BE CONSIDERED.

A student can fully address every task requirement and still receive
a 3/5 if language problems or limited language control significantly
reduce the overall effectiveness of the response.

Likewise, a student should not receive a lower score simply because
their language is simple if it is accurate, clear, and effective.

Give ONE overall estimated score from 0 to 5.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.

Do not average separate categories mathematically.

The final score must reflect the overall effectiveness of the
response.
"""


    # -----------------------------------------------------
    # EVALUATION PROMPT
    # -----------------------------------------------------

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Your job is to evaluate a student's response accurately, fairly,
and pedagogically.

You must evaluate the student's ACTUAL RESPONSE.

Do not evaluate a rewritten or improved version.

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

For each requirement, determine whether it is:

- Not addressed
- Partially addressed
- Sufficiently addressed
- Fully and effectively addressed

Pay close attention to the exact wording of the task.

TASK FULFILLMENT IS IMPORTANT.

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
does NOT mean that longer responses automatically receive higher
scores.

Do not lower a score simply because the student could theoretically
add more information.


=========================================================
2. EVALUATE DEVELOPMENT IN CONTEXT
=========================================================

Evaluate whether the student's ideas are sufficiently developed
for THIS PARTICULAR TASK.

Do not use a fixed rule that every response must contain:

- multiple examples
- extensive explanations
- detailed evidence
- sophisticated arguments

Consider what the student actually needs to communicate in order
to successfully accomplish THIS task.

If a student has:

- clearly identified the required point,
- explained it sufficiently,
- and provided relevant support,

then the requirement may already be sufficiently developed.

Do NOT lower the score simply because the student could provide
additional optional details.

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

The score should reflect the OVERALL EFFECTIVENESS of the response
in relation to the task and the scoring criteria.

IMPORTANT:

A response may fulfill every task requirement and still receive
a 3/5 or lower if language problems significantly limit its
effectiveness.

Do NOT automatically give a 4/5 or 5/5 simply because all task
requirements are present.

Conversely, do NOT lower a score simply because the response is
short, simple, or could optionally contain more information.

The final score must reflect the balance of:

- task fulfillment
- development
- organization
- appropriateness
- language control
- overall effectiveness


=========================================================
4. MANDATORY SCORE CALIBRATION
=========================================================

Use the following examples to calibrate the score.

EXAMPLE A — SCORE 5/5

A response fully addresses the task, is sufficiently developed for
the specific task, and is clear and effective.

It may contain one or two minor errors, but those errors do not
show a consistent lack of language control and do not meaningfully
reduce the overall effectiveness of the response.

SCORE: 5/5


EXAMPLE B — SCORE 4/5

A response fully addresses the task and is generally effective.

The ideas are adequately developed.

There may be some language errors, but they are occasional rather
than frequent, and they do not noticeably reduce the overall
effectiveness of the response.

The response demonstrates generally effective language control.

SCORE: 4/5


EXAMPLE C — SCORE 3/5

A response may fully address ALL task requirements and STILL receive
3/5.

For example, consider a response containing language such as:

"My siblings like very much the reading program."

"They enjoy read books and listen stories."

"My younger sister like the stories."

"She don't understand everything."

"I think the program can improve because the librarian should read
more slowly."

The reader can understand the main message.

The student may successfully fulfill every task requirement.

The tone may be appropriate.

The ideas may be sufficiently developed for the task.

HOWEVER, this response contains MULTIPLE GENUINE LANGUAGE PROBLEMS
ACROSS MULTIPLE SENTENCES, including:

- unnatural or incorrect word order
- incorrect verb forms
- subject-verb agreement errors
- incorrect auxiliary verb forms
- missing grammatical elements
- awkward or unnatural expressions

These problems occur repeatedly throughout the response.

They demonstrate INCONSISTENT LANGUAGE CONTROL.

Therefore, this response should receive 3/5, NOT 4/5.

DO NOT give this type of response 4/5 simply because:

- all task requirements are addressed;
- the main message is understandable;
- the tone is appropriate;
- the student provided enough information;
- the student used complete sentences.

Task fulfillment alone does NOT justify a 4/5.

Understandability alone does NOT justify a 4/5.

If the response contains multiple noticeable language errors across
several sentences, and those errors demonstrate inconsistent
language control, the score should normally be 3/5.

SCORE: 3/5


EXAMPLE D — SCORE 2/5

A response may address some or even most task requirements but
receive 2/5 when language problems are frequent enough to make
understanding difficult in several places, or when ideas are
seriously limited, unclear, repetitive, or insufficiently relevant.

SCORE: 2/5


=========================================================
5. MANDATORY SCORING DECISION PROCESS
=========================================================

Before assigning the final score, silently complete these five steps.

STEP 1 — TASK FULFILLMENT

Determine whether the student fulfilled each explicit task
requirement.

STEP 2 — DEVELOPMENT

Determine whether the ideas are sufficiently developed for THIS
specific task.

Do not demand optional information.

STEP 3 — LANGUAGE CONTROL

Evaluate language control independently.

Identify genuine problems in:

- grammar
- verb forms
- subject-verb agreement
- word forms
- sentence structure
- word choice
- articles
- clarity
- naturalness

Determine whether the problems are:

- isolated
- occasional
- repeated
- frequent
- present across multiple sentences

STEP 4 — OVERALL EFFECT OF LANGUAGE

Determine whether the student's language control is consistent.

IMPORTANT:

Do NOT ask only:

"Can I understand the student's message?"

Also ask:

"Does the student demonstrate the level of language control expected
for this score?"

A response can be understandable and still receive 3/5.

A response can fulfill all task requirements and still receive 3/5.

A response can have appropriate tone and organization and still
receive 3/5.

STEP 5 — FINAL SCORE

Assign the score based on the TOTAL PERFORMANCE.

If task fulfillment is strong but language control is consistently
weak, the final score MUST reflect the language weakness.

Do NOT allow successful task fulfillment to automatically raise
the score to 4/5 or 5/5.

Do NOT allow understandability to automatically raise the score
to 4/5.

Do NOT allow the fact that the student has "answered everything"
to automatically raise the score to 4/5.

The score must reflect BOTH:

1. What the student communicates.
2. How effectively and accurately the student communicates it.


=========================================================
6. SCORE BANDS
=========================================================

5/5:

The response is highly effective.

It fulfills the task requirements fully and effectively.

Ideas are sufficiently developed for the task.

Language is generally accurate and effective.

Minor errors may occur, but they do not meaningfully reduce the
overall effectiveness of the response.

Do NOT give 5/5 if repeated or noticeable language errors affect
overall effectiveness.

4/5:

The response is effective and relevant.

The task requirements are fulfilled.

Ideas are adequately developed.

Language is generally accurate and effective.

There may be some errors or limitations, but they are generally
occasional and do not noticeably reduce overall effectiveness.

IMPORTANT:

Do NOT give 4/5 merely because the task requirements are fulfilled.

Do NOT give 4/5 merely because the response is understandable.

If the response contains MULTIPLE NOTICEABLE grammatical errors
across several sentences, recurring subject-verb agreement errors,
repeated incorrect verb forms, or repeated awkward expressions
that demonstrate inconsistent language control, consider 3/5.

3/5:

The response is generally relevant and understandable.

The main task requirements may be fulfilled.

However, the response may contain:

- limited development
- basic organization
- frequent grammatical errors
- recurring subject-verb agreement errors
- incorrect verb forms
- awkward or unnatural expressions
- limited language control
- repeated errors across several sentences

The main meaning is generally understandable, but the response does
not consistently demonstrate the language control expected for a
higher score.

IMPORTANT:

A response can receive 3/5 even if it successfully addresses ALL
task requirements.

Full task fulfillment does NOT automatically mean 4/5.

Understandability does NOT automatically mean 4/5.

2/5:

The response demonstrates limited ability.

The response may partially address the task or may address the task
but have substantial problems with development, relevance,
organization, or language control.

Language problems may frequently interfere with clarity.

1/5:

The response provides very little relevant content or does not
meaningfully accomplish the task.

Ideas may be severely limited or unclear.

Frequent language problems significantly interfere with
communication.

0/5:

The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.


=========================================================
7. UNDERSTAND WHAT A 5/5 MEANS
=========================================================

Do not assume that a 5/5 response must be perfect.

A response can receive 5/5 even if it contains:

- a minor grammatical error
- a slightly awkward expression
- simple but accurate vocabulary
- a sentence that could stylistically be improved
- a detail that could optionally be expanded

However, a 5/5 response should NOT contain repeated or noticeable
language errors that affect overall effectiveness.

Do not lower a score because the response could be made "even better"
through optional stylistic improvements.

Only identify score-limiting weaknesses when they genuinely affect
the effectiveness of the response according to the scoring criteria.


=========================================================
8. JUSTIFY THE SCORE
=========================================================

After assigning the score, explain specifically why the response
fits that score.

Your explanation must refer to:

- the actual task requirements
- the student's actual response
- development
- language control
- overall effectiveness

Do not give generic explanations that could apply to any student.

Most importantly, determine whether the response genuinely falls
below the next score level.

For scores 1-4, explain what specific limitations prevent the
response from receiving the next higher score.

However, do NOT force yourself to invent a weakness.

If the response actually demonstrates the characteristics of the
next higher score, give the higher score.

Do not lower a score merely because there are optional ways to make
the response longer, more detailed, or more sophisticated.

For a 5/5 response, explain why the response demonstrates the
characteristics of the highest score level.


=========================================================
9. DO NOT CONFUSE STYLE WITH ERROR
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
10. LANGUAGE FEEDBACK
=========================================================

Identify language problems only when they are genuinely relevant.

Consider:

- grammar errors
- incorrect word choice
- incorrect word forms
- incorrect verb forms
- subject-verb agreement
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

B. MEANINGFUL LANGUAGE ISSUE

The language is understandable but noticeably awkward, unclear,
or unnatural in a way that is worth teaching.

Example:

"My siblings like very much the reading program."

This is understandable, but the word order is awkward.

A possible correction is:

"My siblings really like the reading program."

C. STYLE

The sentence is correct, but another version is possible.

Do NOT present category C as an error.

Only A and meaningful examples of B should appear as corrections.


=========================================================
11. DO NOT USE A FIXED NUMBER OF CORRECTIONS
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


=========================================================
12. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH
=========================================================

A student should not receive a lower score simply because they
use simple vocabulary or grammar.

Simple, accurate, clear language is better than unnecessarily
complex language with errors.

Do not encourage students to use sophisticated vocabulary merely
for the sake of sounding advanced.

However, distinguish clearly between:

SIMPLE BUT CORRECT LANGUAGE

and

SIMPLE LANGUAGE WITH FREQUENT ERRORS.

Simple language should not be penalized.

Frequent grammatical errors MUST be considered when determining
the overall score.


=========================================================
13. DO NOT REQUIRE FORMAL EVIDENCE UNLESS THE TASK REQUIRES IT
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
14. GIVE SPECIFIC AND ACTIONABLE FEEDBACK
=========================================================

Feedback must help the student understand exactly what they did
well and what they need to do differently.

Avoid vague advice such as:

"Develop your ideas more."

Instead, explain:

- which idea needs improvement
- where it appears in the response
- what is missing
- how the student could improve it

Use specific examples from the student's actual response.

Do not recommend changes that the student has already successfully
made elsewhere in the response.

If the main weakness is language accuracy, focus the improvement
advice on language accuracy.

Do NOT automatically recommend more examples or more development
when the task requirements are already sufficiently fulfilled.


=========================================================
15. THE BETTER VERSION MUST BE NECESSARY AND CONSISTENT
=========================================================

The Better Version must reflect the student's actual score and
actual weaknesses.

This is extremely important.

Do NOT say:

"Your original response is already clear and effective.
No substantial revision is necessary."

if you have identified genuine language errors that should be
corrected.

If the response contains genuine language errors, the Better Version
MUST correct those errors.

If the response has weaknesses that genuinely limit its score,
the Better Version should demonstrate how to address those
weaknesses while remaining close to the student's original writing.

For a weaker response, prioritize:

1. Completing missing task requirements.
2. Correcting genuine grammar errors.
3. Correcting incorrect word forms or verb forms.
4. Correcting subject-verb agreement.
5. Improving unclear or confusing sentences.
6. Improving organization when necessary.
7. Adding development only when the task genuinely requires it.

For a stronger response, make fewer changes.

Preserve the student's:

- original ideas
- original meaning
- approximate language level
- personal voice

Do not replace correct language with stylistic alternatives.

Do not add completely new arguments or ideas.

Do not make a 3/5 response sound like a C1 or C2 student.

The Better Version should demonstrate an improvement appropriate
to the student's actual score level.


=========================================================
16. MANDATORY CONSISTENCY CHECK
=========================================================

Before producing the final evaluation, silently check for
contradictions.

If you identify genuine language errors in "Language Feedback":

- the score must reflect those errors when they meaningfully affect
  overall effectiveness;
- "What to Improve" should acknowledge the most important language
  problems;
- the "Better Version" must correct those genuine errors.

Do NOT say both:

"The response contains several language errors"

and:

"No substantial revision is necessary."

Do NOT say:

"The response needs more development"

if the task requirements have already been sufficiently developed.

Do NOT recommend adding examples simply because more examples
are theoretically possible.

The feedback must be internally consistent.


=========================================================
REQUIRED FEEDBACK FORMAT
=========================================================

Return ONLY the following sections:

## Estimated Score: X/5

## Why?

Write 2-4 concise sentences explaining why the response fits
this score.

Refer specifically to:

- the task requirements
- how effectively the student fulfills them
- the development of the ideas
- language control
- the overall quality of the response

## Why Not the Next Score?

For scores 1-4, explain the specific limitations that genuinely
prevent the response from receiving the next higher score.

This section must be based on the task requirements and the
scoring criteria.

Do NOT invent a weakness simply because the student could add
more information.

Do NOT say that the response needs more examples or explanations
if the task requirements have already been sufficiently fulfilled.

If the main limitation is language accuracy or language control,
say so clearly and identify the actual problems.

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

If the main weakness is language accuracy, focus on language
accuracy.

If the main weakness is task fulfillment, focus on task fulfillment.

If the main weakness is development, focus on development.

Do not invent weaknesses.

Do not recommend adding information that is already present.

Do not automatically recommend more examples or more sophisticated
vocabulary.


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

Provide a revised version when the student's original contains
genuine errors or when a revision adds genuine pedagogical value.

If the original is already clear, accurate, and effective, state:

"Your original response is already clear and effective.
No substantial revision is necessary."

IMPORTANT:

Do NOT use that statement if you identified genuine errors
that should be corrected.

If a revision is useful:

- correct genuine errors
- improve clarity when necessary
- improve organization when genuinely needed
- address missing task requirements
- demonstrate improvements appropriate to the student's score level

Keep the revision close to the student's original ideas,
voice, and language level.

Do not make a 3/5 response sound like an advanced native speaker.

Do not add completely new arguments or ideas.

Keep the entire evaluation concise, specific, accurate,
internally consistent, and student-friendly.
"""


    # -----------------------------------------------------
    # SEND TO GROQ
    # -----------------------------------------------------

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": (
                    "You are a careful and fair TOEFL Writing evaluator. "
                    "Your priority is accurate scoring and useful teaching "
                    "feedback, not rewriting. "
                    "Evaluate task fulfillment and language control separately "
                    "before assigning the overall score. "
                    "Do not confuse stylistic preferences with genuine errors. "
                    "Do not invent weaknesses or corrections. "
                    "Task fulfillment does not automatically justify a high score. "
                    "Understandability does not automatically justify a 4/5. "
                    "If multiple genuine language errors occur across several "
                    "sentences and demonstrate inconsistent language control, "
                    "the response should normally be scored 3/5 rather than 4/5. "
                    "If you identify genuine language errors, make sure the "
                    "score, improvement advice, language feedback, and better "
                    "version are internally consistent."
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

if st.button(
    "🔍 Evaluate My Writing",
    type="primary"
):

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
