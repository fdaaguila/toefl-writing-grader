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

    /* Justified paragraphs */
    .justified-text {
        text-align: justify;
        line-height: 1.6;
    }

    /* Section headings */
    .feedback-heading {
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }

    /* Score display */
    .score-display {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* Feedback box */
    .feedback-box {
        text-align: justify;
        line-height: 1.6;
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
- Does the writer address all required points in the task?
- Is the message clear, relevant, and appropriately developed?
- Is the organization appropriate for an email?
- Is the tone appropriate for the intended recipient and situation?
- Is the language generally accurate and effective?
- Does the writer use appropriate vocabulary and sentence structures?

Give ONE estimated score from 0 to 5 based on the overall effectiveness
of the response.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.

A high score requires the response to be effective overall, not merely
complete. A response may fulfill every task requirement and still
receive a lower score if frequent language problems, weak language
control, unclear communication, or insufficient development reduce
its effectiveness.

However, do not lower a score simply because the response could
optionally include more information. Judge development according to
what is reasonably necessary to accomplish the specific task.
"""

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Your job is to evaluate a student's response accurately, fairly,
and pedagogically.

Evaluate the student's ACTUAL response as it is written.

Do not evaluate an imaginary improved version.

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
does NOT mean that longer responses automatically receive higher
scores.

Do not lower a score simply because the student could theoretically
add more information.

At the same time, if the response is genuinely too brief or does
not sufficiently explain an idea required by the task, this may
affect the score.

Judge task fulfillment and development in context.


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
- and suggests one possible solution,

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

However, task completion alone does NOT automatically guarantee
a score of 4 or 5.

If the response fulfills the task but contains frequent grammatical
errors, incorrect verb forms, incorrect word choices, awkward
sentence structures, or inconsistent language control, these
problems may justify a lower score.

The frequency, seriousness, and effect of language problems must
be considered in relation to the overall response.


=========================================================
4. UNDERSTAND THE DIFFERENCE BETWEEN SCORE BANDS
=========================================================

Use the following principles when distinguishing score levels.

5/5:
The response is highly effective overall. It fulfills the task
requirements, communicates ideas clearly, and demonstrates strong
control of language. Minor errors or awkward expressions may occur,
but they do not significantly reduce effectiveness.

Do not require perfection for a 5/5.

A 5/5 response may contain:
- a minor grammatical error,
- a slightly awkward expression,
- simple but accurate vocabulary,
- a sentence that could be stylistically improved,
- or a detail that could optionally be expanded.

Do not lower a score because the response could be made "even better"
through optional stylistic improvements.

4/5:
The response is effective overall and fulfills the task. Ideas are
relevant and adequately developed. Language is generally accurate
and clear, although there may be some noticeable errors or
limitations.

A 4/5 response should generally demonstrate effective communication
with reasonably consistent language control.

Do not assign 4/5 simply because every task requirement is present.

If multiple genuine language errors occur across the response,
especially errors involving verb forms, subject-verb agreement,
sentence structure, word choice, or other basic language control,
consider whether these errors are frequent enough to place the
response at 3/5 instead.

3/5:
The response generally fulfills the task and the main message is
understandable, but the response may be basic, limited in
development, or demonstrate inconsistent language control.

A 3/5 response may contain several genuine grammar or language
problems, such as:
- subject-verb agreement errors,
- incorrect verb forms,
- missing articles,
- incorrect prepositions,
- incorrect plural forms,
- awkward or inaccurate word combinations,
- sentence structure problems,
- or unnatural expressions.

These problems do not necessarily make the response impossible
to understand, but they may reduce its overall effectiveness.

If a response contains multiple genuine language errors across
several sentences, do not automatically give it 4/5 merely because
all task requirements are addressed.

2/5:
The response demonstrates limited ability to accomplish the task.
Ideas may be insufficiently developed, unclear, repetitive, or
partially relevant. Language problems are frequent and may make
the response difficult to understand in places.

1/5:
The response provides very little relevant content or does not
meaningfully accomplish the task. Ideas are severely limited or
unclear, and frequent language problems significantly interfere
with communication.

0/5:
Use 0 only when the response meets the rubric's conditions for a
zero score, such as being blank, copied from the prompt, completely
irrelevant, not written in English, or otherwise not providing a
meaningful response.


=========================================================
5. JUSTIFY THE SCORE ACCURATELY
=========================================================

After assigning the score, explain specifically why the response
fits that score.

Your explanation must refer to the actual task requirements and
the student's actual response.

Do not give generic explanations that could apply to any student.

Most importantly, determine whether the response genuinely falls
below the next score level.

For scores 1-4, explain the specific limitations that prevent the
response from receiving the next higher score.

However, do NOT force yourself to invent a weakness.

If the response actually demonstrates the characteristics of the
next higher score, give the higher score.

Do not lower a score merely because there are optional ways to make
the response longer, more detailed, or more sophisticated.

For a 5/5 response, explain why the response demonstrates the
characteristics of the highest score level.

The explanation of the score must be consistent with the language
feedback.

For example, if the response contains several genuine grammatical
errors across multiple sentences, do not describe the language
as "generally accurate" without qualification.

Likewise, do not claim that language errors significantly affect
communication if the errors are minor and the message remains
consistently clear.


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

IMPORTANT:

Some expressions may be understandable but awkward.

Distinguish between:

A. REAL ERROR
The language is grammatically incorrect or uses an incorrect
word, form, structure, or expression.

B. MEANINGFUL LANGUAGE ISSUE
The language is understandable but sufficiently awkward, unclear,
or inaccurate that it is worth teaching and correcting.

C. STYLE
The sentence is correct, but another version is possible.

Only A and meaningful examples of B should appear in Language
Feedback.

Do NOT present category C as an error.

Do not call a sentence "grammatically incorrect" when it is only
awkward or stylistically less natural.


=========================================================
7. LANGUAGE FEEDBACK
=========================================================

Identify language problems only when they are genuinely relevant.

Consider:

- grammar errors
- incorrect word choice
- incorrect word forms
- incorrect verb forms
- subject-verb agreement
- article errors when relevant
- preposition errors
- sentence structure problems
- unclear or confusing language
- genuinely unnatural expressions
- inappropriate language for the context

Pay particular attention to repeated patterns.

If the student makes the same type of error several times, this
may indicate inconsistent language control and should be reflected
in the score when appropriate.

For example, if a student writes:

"My siblings like very much the reading program."

This is understandable, but the word order is awkward. It may be
corrected as:

"My siblings really like the reading program."

Do NOT describe the original as completely incomprehensible.

If a student writes:

"They enjoy read books and listen stories."

This contains genuine grammatical problems. After "enjoy," the
gerund form is required, and "listen" normally requires "to" before
the object.

A correction would be:

"They enjoy reading books and listening to stories."

If a student writes:

"My younger sister like the stories."

This contains a genuine subject-verb agreement error.

A correction would be:

"My younger sister likes the stories."

If a student writes:

"the stories are too fast"

this may be understandable, but the expression is not the most
accurate way to describe the pace of storytelling.

A more precise correction may be:

"the stories are read too quickly."

However, do not treat every understandable expression as a serious
error.

The severity of each issue must be judged in context.


=========================================================
8. DO NOT USE A FIXED NUMBER OF CORRECTIONS
=========================================================

Do NOT give a predetermined number of corrections.

The number of corrections must depend entirely on the student's
actual writing.

If there are no meaningful language problems, say:

"No major language errors."

If there are one or two meaningful problems, identify only those.

If there are several meaningful problems, identify the most
important ones that would help the student improve.

Do not invent corrections simply to provide more feedback.

Do not correct every minor punctuation issue unless it represents
a repeated or important problem.

The goal is useful and accurate feedback, not a long list of
feedback items.

When there are multiple genuine errors, prioritize errors that:

1. occur repeatedly,
2. demonstrate a pattern of weak language control,
3. affect clarity,
4. or are important for the student's level.

Do not prioritize stylistic improvements over genuine errors.


=========================================================
9. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH
=========================================================

A student should not receive a lower score simply because they
use simple vocabulary or grammar.

Simple, accurate, clear language is better than unnecessarily
complex language with errors.

Do not encourage students to use sophisticated vocabulary merely
for the sake of sounding advanced.

Do not require advanced vocabulary or complex sentence structures
when simple language communicates the idea effectively.


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

Suggestions should match the student's actual score level.

For a 3/5 response with genuine language problems, prioritize
language accuracy and control before recommending advanced
vocabulary or extensive additional development.

For a 4/5 response, focus on the specific limitations that prevent
a 5/5 rather than automatically demanding more examples.

For a 5/5 response, do not invent improvements merely to make the
feedback longer.


=========================================================
12. THE BETTER VERSION MUST STAY CLOSE TO THE ORIGINAL
=========================================================

The Better Version is a teaching tool.

It should demonstrate how the student's own response could be
improved while preserving the student's original communication.

Do NOT rewrite the student's response into a completely different
email or essay.

Do NOT change the structure unnecessarily.

Do NOT replace correct language simply because another version
sounds more sophisticated.

Do NOT remove ideas that the student included.

Do NOT introduce completely new arguments.

Do NOT change the student's intended meaning.

Keep the student's:

- original ideas,
- original meaning,
- approximate language level,
- personal voice,
- and overall organization whenever possible.

The Better Version SHOULD:

- correct genuine grammar errors,
- correct incorrect verb forms,
- correct subject-verb agreement,
- correct incorrect word forms,
- correct important word choice problems,
- improve clarity when necessary,
- improve organization only when genuinely needed,
- and address a missing task requirement only if one actually exists.

The Better Version MAY add a SMALL amount of useful development
when this would genuinely help demonstrate how the student could
reach the next score level.

However, optional additions must be clearly connected to the
student's original ideas.

For example, if the student says that stories are read too quickly,
a useful addition might briefly explain that reading more slowly
would help children understand the stories.

Do NOT add unrelated ideas, new arguments, invented personal
experiences, or sophisticated content that the student did not
suggest.

If the student's response is already clear and effective, write:

"Your original response is already clear and effective.
No substantial revision is necessary."

If a revision is useful, make the FEWEST changes necessary to
correct genuine problems and demonstrate meaningful improvement.

Do not turn a 3/5 student's response into a completely polished
5/5 response.

The Better Version should remain recognizably the student's
original response.


=========================================================
13. IMPORTANT CONSISTENCY CHECK
=========================================================

Before producing the final evaluation, silently check that:

- The score matches the actual quality of the response.
- The score is consistent with the rubric.
- The explanation of the score is consistent with the Language
  Feedback.
- The What to Improve section does not criticize something the
  student already did successfully.
- The Better Version does not unnecessarily rewrite correct
  language.
- The Better Version does not introduce unrelated ideas.
- The Better Version does not make the student's writing
  unrealistically advanced.
- Stylistic preferences are not presented as errors.
- Genuine repeated language problems are not ignored.
- Task fulfillment is not confused with language quality.
- Additional development is not demanded when the task has already
  been sufficiently fulfilled.
- The response is not given a higher score simply because all task
  requirements are present.
- The response is not given a lower score simply because it could
  theoretically be longer or more sophisticated.


=========================================================
REQUIRED FEEDBACK FORMAT
=========================================================

Return ONLY the following sections.

## Estimated Score: X/5

## Why?

Write 2-4 concise sentences explaining why the response fits this
score.

Refer specifically to:

- the task requirements,
- how effectively the student fulfills them,
- the development of the ideas,
- and the overall quality of the language.

The explanation must accurately reflect the student's actual
language control.

## Why Not the Next Score?

For scores 1-4, explain the specific limitations that genuinely
prevent the response from receiving the next higher score.

This section must be based on the task requirements and the
scoring criteria.

Do NOT invent a weakness simply because the student could add
more information.

Do NOT say that the response needs more examples or explanations
if the task requirements have already been sufficiently fulfilled.

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

Do not recommend adding information that is already present.

For a response with genuine language problems, identify the
language patterns the student should practice.

For a response with sufficient task fulfillment but weak language
control, do not incorrectly focus only on adding more ideas.

For a response that is already very strong, explain that only
minor improvements are needed.

## Language Feedback

Identify all meaningful language problems that are relevant to
the student's performance.

For each issue, use exactly:

Original:
Correction:
Why:

Only include genuine errors or meaningful language issues.

Do not include stylistic alternatives.

Do not label a stylistic preference as an error.

If there are no meaningful language problems, write:

"No major language errors."

## Better Version

Provide a revised version that stays as close as reasonably possible
to the student's original response.

Correct genuine language problems.

Preserve the student's original ideas, meaning, voice, approximate
language level, and organization.

Do not unnecessarily rewrite correct sentences.

Do not make the response artificially advanced.

Do not add unrelated arguments or invented information.

A small amount of additional development is acceptable only when
it is directly connected to the student's original ideas and would
genuinely demonstrate how to improve the response.

If no substantial revision is necessary, write:

"Your original response is already clear and effective.
No substantial revision is necessary."

Keep the entire evaluation concise, specific, accurate,
consistent, and student-friendly.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and fair TOEFL Writing evaluator. "
                    "Follow the provided scoring criteria exactly. "
                    "Your priority is accurate evaluation, not rewriting. "
                    "Distinguish task fulfillment from language quality. "
                    "Do not confuse stylistic preferences with language errors. "
                    "Do not invent weaknesses. "
                    "Evaluate the student's actual response, not an improved version. "
                    "Keep the Better Version close to the student's original."
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
# FORMAT FEEDBACK FOR DISPLAY
# ---------------------------------------------------------

def format_feedback(text):

    # Convert markdown headings into styled HTML headings.
    text = text.replace(
        "## Estimated Score:",
        '<div class="feedback-heading">Estimated Score:'
    )

    text = text.replace(
        "## Why?",
        '<div class="feedback-heading">Why?</div>'
    )

    text = text.replace(
        "## Why Not the Next Score?",
        '<div class="feedback-heading">Why Not the Next Score?</div>'
    )

    text = text.replace(
        "## What You Did Well",
        '<div class="feedback-heading">What You Did Well</div>'
    )

    text = text.replace(
        "## What to Improve",
        '<div class="feedback-heading">What to Improve</div>'
    )

    text = text.replace(
        "## Language Feedback",
        '<div class="feedback-heading">Language Feedback</div>'
    )

    text = text.replace(
        "## Better Version",
        '<div class="feedback-heading">Better Version</div>'
    )

    # Bold important labels.
    text = text.replace(
        "Original:",
        "<strong>Original:</strong>"
    )

    text = text.replace(
        "Correction:",
        "<strong>Correction:</strong>"
    )

    text = text.replace(
        "Why:",
        "<strong>Why:</strong>"
    )

    # Italicize the standard no-error message.
    text = text.replace(
        "No major language errors.",
        "<em>No major language errors.</em>"
    )

    # Preserve line breaks while applying justified alignment.
    text = text.replace("\n\n", "<br><br>")
    text = text.replace("\n", "<br>")

    return f'<div class="feedback-box">{text}</div>'


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

                formatted_evaluation = format_feedback(
                    evaluation
                )

                st.markdown(
                    formatted_evaluation,
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
