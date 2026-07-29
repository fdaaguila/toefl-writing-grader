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
    /* Justify the main feedback text */
    .feedback-text {
        text-align: justify;
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    /* Keep headings readable and not oversized */
    .feedback-heading {
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.6rem;
    }

    /* Language feedback labels */
    .feedback-label {
        font-weight: 600;
    }

    /* Better version */
    .better-version {
        text-align: left;
        line-height: 1.6;
        white-space: pre-wrap;
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

Your job is to evaluate a student's response accurately and fairly,
using the specific task prompt, the scoring guidelines, and the
student's actual writing.

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

1. SCORE THE RESPONSE AS IT IS.

Evaluate the student's actual writing, not a rewritten or improved
version.

Base the score on the response that the student actually submitted.

Do not give a higher score because the response could be improved
through rewriting.

Do not give a lower score simply because the student could
theoretically add more information.

Evaluate whether the response is sufficiently effective for THIS
specific task.

=========================================================

2. START WITH THE TASK REQUIREMENTS
=========================================================

Carefully analyze the specific task prompt before assigning a score.

Identify every explicit requirement that the student was asked to
fulfill.

For example, if the task asks the student to:

- explain what the siblings enjoyed,
- describe one aspect that could be improved,
- offer to help with future events,

check each requirement individually.

Determine whether each requirement is:

- Not addressed
- Partially addressed
- Sufficiently addressed
- Fully and effectively addressed

Task fulfillment is a central part of the evaluation.

Do not penalize a student for failing to provide information that
the task does not require.

Do not ask the student to add additional examples or explanations
if the task requirement has already been sufficiently fulfilled.

A response does not need multiple examples for a requirement unless
the task specifically asks for them.

Do not confuse:

"The student could say more"

with:

"The student has not sufficiently fulfilled the task."

These are NOT the same.

The instruction "Write as much as you can and in complete sentences"
does not mean that longer responses automatically receive higher
scores.

Do not lower a score simply because more information could be added.

=========================================================

3. EVALUATE DEVELOPMENT IN CONTEXT
=========================================================

Evaluate whether the student's ideas are sufficiently developed
for THIS PARTICULAR TASK.

Do not use a fixed rule that every response must contain multiple
examples, extensive explanations, or detailed evidence.

Consider what the student actually needs to communicate in order
to successfully accomplish the task.

If a student is asked to describe one aspect that could be improved,
and the student clearly identifies the problem and gives a reasonable
suggestion, do not automatically require additional examples.

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

4. SCORE CONSISTENTLY ACROSS ALL SCORE BANDS
=========================================================

Use the scoring guidelines to distinguish among score levels.

A response should not receive a 4 or 5 simply because it fulfills
all task requirements.

A response may fulfill every task requirement and still receive a
lower score if language control, clarity, development, or overall
effectiveness genuinely limits the response.

At the same time, do not lower a score simply because the response
uses simple but correct language.

For a score of 3, consider whether the response is generally
understandable and relevant but contains limitations in development
or noticeable language problems.

For a score of 4, consider whether the response is effective and
relevant, with generally accurate language and adequate development.

For a score of 5, consider whether the response is highly effective,
clear, relevant, and sufficiently developed, with language that is
generally accurate and appropriate.

Do not use "more sophisticated vocabulary" as an automatic reason
to lower a score.

Do not use "more examples" as an automatic reason to lower a score.

The reason for the score must be grounded in the actual scoring
criteria and the actual student response.

=========================================================

5. JUSTIFY THE SCORE ACCURATELY
=========================================================

After assigning the score, explain specifically why the response
fits that score.

Refer to the actual task requirements and the student's actual
writing.

Do not give generic explanations that could apply to any student.

For scores 1-4, explain what specific limitations genuinely prevent
the response from receiving the next higher score.

Do not invent a weakness simply because the student could add more
information.

If the response genuinely demonstrates the characteristics of the
next higher score, assign the higher score.

For a score of 5, explain why the response demonstrates the
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

If the student's sentence is grammatically correct, clear, natural
enough for the context, and appropriate for the task, leave it alone.

For example:

"I think that it would make a big difference."

is correct and should NOT be changed simply because:

"I believe that it would make a significant difference."

sounds more advanced.

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

Distinguish carefully between:

A. REAL ERROR

The language is incorrect.

B. MINOR LANGUAGE ISSUE

The language is understandable but slightly unclear, vague,
awkward, or less natural in a way that is genuinely useful to teach.

C. STYLE

The sentence is correct, but another version is possible.

Only A and meaningful examples of B should appear as corrections.

Do NOT present category C as an error.

If the original is understandable but awkward, explicitly say that
it is awkward or unnatural rather than falsely describing it as
grammatically incorrect.

For example:

"My siblings like very much the reading program."

can reasonably be identified as awkward or unnatural word order.

Do not claim that it is completely ungrammatical if the meaning is
clear.

=========================================================

8. DO NOT USE A FIXED NUMBER OF CORRECTIONS
=========================================================

Do not invent corrections.

The number of corrections must depend on the student's actual writing.

If there are no meaningful language problems, write:

"No major language errors."

If there are one or two meaningful problems, identify only those.

If there are several meaningful problems, identify the most important
ones that would help the student improve.

Do not correct every minor punctuation issue unless it represents
a repeated or important problem.

Prioritize corrections that are:

- frequent,
- important,
- clearly incorrect,
- or particularly useful for the student's development.

=========================================================

9. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH
=========================================================

A student should not receive a lower score simply because they use
simple vocabulary or grammar.

Simple, accurate, clear language is better than unnecessarily
complex language with errors.

Do not encourage students to use sophisticated vocabulary merely
for the sake of sounding advanced.

=========================================================

10. DO NOT REQUIRE FORMAL EVIDENCE UNLESS THE TASK REQUIRES IT
=========================================================

For Academic Discussion, students should explain and support their
ideas, but they do not need formal academic evidence, research, or
citations.

Use terms such as:

- explanation
- support
- development
- example

when appropriate.

Do not criticize a student for lacking "evidence" unless the task
specifically requires evidence.

=========================================================

11. GIVE SPECIFIC AND ACTIONABLE FEEDBACK
=========================================================

Feedback must help the student understand exactly what they did well
and what they need to do differently.

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

=========================================================

12. THE BETTER VERSION MUST BE MINIMALLY INVASIVE
=========================================================

The Better Version is a teaching tool, not a complete rewrite.

This is extremely important.

Preserve the student's original:

- ideas,
- meaning,
- organization,
- approximate language level,
- personal voice,
- and wording whenever that wording is already acceptable.

Make ONLY the changes that are genuinely necessary or clearly
pedagogically useful.

Prioritize, in this order:

1. Correct genuine grammar errors.
2. Correct incorrect word forms or word choice.
3. Correct unclear expressions when necessary.
4. Make small changes that improve clarity.
5. Make small organizational changes only when genuinely needed.
6. Address a missing task requirement only if one is actually missing.

Do NOT rewrite the response simply to make it sound more native-like.

Do NOT replace correct language with more sophisticated alternatives.

Do NOT change sentences merely because another version sounds better.

Do NOT add new arguments or ideas.

Do NOT add detailed examples that the student did not originally
include unless clearly necessary to demonstrate how the student
could improve a genuinely underdeveloped idea.

If the response is a score 1 or 2, the Better Version may contain
more substantial corrections if necessary for clarity and task
fulfillment.

If the response is a score 3, preserve the student's original
content and make targeted corrections to the most important language
problems.

If the response is a score 4 or 5, make only minimal corrections,
if any.

The Better Version should look like a realistic improved version
that THIS STUDENT could produce after receiving feedback.

Do not transform a 3/5 response into a completely different,
highly advanced 5/5 response.

If the student's original response is already clear and effective,
write:

"Your original response is already clear and effective.
No substantial revision is necessary."

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
- and the overall quality of the response.

Do not say that the response needs more examples or explanations
unless that is genuinely necessary for the score.

## Why Not the Next Score?

For scores 1-4, explain the specific limitations that genuinely
prevent the response from receiving the next higher score.

Base this explanation on the task requirements and scoring criteria.

Do not invent a weakness simply because the student could add more
information.

Do not automatically say that the response needs more examples,
more detail, or more sophisticated vocabulary.

If the main limitation is language control, explain that clearly.

If the main limitation is development, explain exactly what is missing.

If the response genuinely demonstrates the characteristics of the
next higher score, assign the higher score instead.

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

If the response is already very strong, explain that only minor
improvements are needed.

## Language Feedback

Identify meaningful language problems that are relevant to the
student's performance.

Do not force a fixed number of corrections.

For each issue, use exactly this format:

Original:
Correction:
Why:

Only include genuine errors or meaningful language issues.

If the original is understandable but awkward, distinguish this
from a grammatical error.

Do not include stylistic alternatives as corrections.

If there are no meaningful language problems, write:

"No major language errors."

## Better Version

Provide a revised version only if it adds genuine pedagogical value.

The revision must be minimally invasive.

Preserve the student's original ideas, meaning, organization,
approximate language level, and personal voice.

Correct genuine errors and make only necessary improvements.

Do not rewrite the response simply to make it sound more advanced
or native-like.

Do not replace correct language with stylistic alternatives.

Do not add completely new arguments or ideas.

For a strong response, make minimal changes or state:

"Your original response is already clear and effective.
No substantial revision is necessary."

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
                    "Follow the provided scoring criteria exactly. "
                    "Your priority is accurate evaluation, not rewriting. "
                    "Do not confuse stylistic preferences with language errors. "
                    "Evaluate the student's actual response as written. "
                    "The Better Version must be minimally invasive and must "
                    "preserve the student's original ideas, meaning, voice, "
                    "organization, and approximate language level. "
                    "Do not invent weaknesses or unnecessary corrections."
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
# DISPLAY EVALUATION
# ---------------------------------------------------------

def display_evaluation(evaluation):

    sections = evaluation.split("## ")

    for section in sections:

        if not section.strip():
            continue

        lines = section.strip().split("\n", 1)

        heading = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""

        # Score heading
        if heading.startswith("Estimated Score"):
            st.markdown(
                f'<div class="feedback-heading">{heading}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="feedback-text">{content}</div>',
                unsafe_allow_html=True
            )

        # Standard feedback sections
        elif heading in [
            "Why?",
            "Why Not the Next Score?",
            "What You Did Well",
            "What to Improve"
        ]:

            st.markdown(
                f'<div class="feedback-heading">{heading}</div>',
                unsafe_allow_html=True
            )

            formatted_content = content.replace(
                "\n\n",
                "</p><p>"
            ).replace(
                "\n",
                "<br>"
            )

            st.markdown(
                f'<div class="feedback-text"><p>{formatted_content}</p></div>',
                unsafe_allow_html=True
            )

        # Language Feedback
        elif heading == "Language Feedback":

            st.markdown(
                '<div class="feedback-heading">Language Feedback</div>',
                unsafe_allow_html=True
            )

            # Split individual corrections
            correction_blocks = content.split("\n\n")

            for block in correction_blocks:

                if not block.strip():
                    continue

                formatted_block = block

                formatted_block = formatted_block.replace(
                    "Original:",
                    '<span class="feedback-label">Original:</span>'
                )

                formatted_block = formatted_block.replace(
                    "Correction:",
                    '<span class="feedback-label">Correction:</span>'
                )

                formatted_block = formatted_block.replace(
                    "Why:",
                    '<span class="feedback-label">Why:</span>'
                )

                formatted_block = formatted_block.replace(
                    "\n",
                    "<br>"
                )

                st.markdown(
                    f'<div class="feedback-text">{formatted_block}</div>',
                    unsafe_allow_html=True
                )

        # Better Version
        elif heading == "Better Version":

            st.markdown(
                '<div class="feedback-heading">Better Version</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="better-version">{content}</div>',
                unsafe_allow_html=True
            )


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

                display_evaluation(
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
