```python
import streamlit as st
from groq import Groq
import re


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

    .feedback-text {
        text-align: justify;
        line-height: 1.6;
        font-size: 16px;
    }

    .feedback-text h2 {
        text-align: left;
        margin-top: 18px;
        margin-bottom: 8px;
        font-size: 21px;
        font-weight: 600;
    }

    .feedback-text ul {
        text-align: justify;
        margin-top: 4px;
        margin-bottom: 10px;
        padding-left: 25px;
    }

    .feedback-text li {
        margin-bottom: 5px;
    }

    .better-version {
        text-align: left;
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

st.title(
    "📝 TOEFL Writing AI Grader"
)

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

st.subheader(
    "TOEFL Task"
)

task_prompt = st.text_area(
    "Paste the TOEFL task or prompt here:",
    height=200,
    placeholder="Paste the complete TOEFL task here..."
)


# ---------------------------------------------------------
# STUDENT RESPONSE
# ---------------------------------------------------------

st.subheader(
    "Your Response"
)

student_response = st.text_area(
    "Paste your TOEFL writing response here:",
    height=300,
    placeholder="Paste your writing response here..."
)


# ---------------------------------------------------------
# ACADEMIC DISCUSSION RUBRIC
# ---------------------------------------------------------

ACADEMIC_DISCUSSION_RUBRIC = """

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

IMPORTANT:

Do not require formal academic research or citations.

Students do not need to provide statistical evidence or research
unless the task explicitly asks for it.

Evaluate the quality of the student's explanation and support based
on what is appropriate for the task.

Do not invent additional requirements that are not present in the
task.

Do not penalize a student simply because they did not discuss a
specific counterargument, long-term consequence, or alternative
solution unless that is necessary to fulfill the actual task.

Do not require "nuanced" arguments for a 5 unless the response
genuinely needs additional development to fully address the task.

A student can receive a 4 or 5 using relatively simple language if
the language is accurate, clear, effective, and appropriate.

Do not require sophisticated vocabulary or complex grammar merely
because the response is aiming for a high score.
"""


# ---------------------------------------------------------
# EMAIL RUBRIC
# ---------------------------------------------------------

EMAIL_RUBRIC = """

Evaluate the response as a TOEFL iBT Writing "Write an Email" task.

Consider:

- Does the writer successfully accomplish the purpose of the email?
- Does the writer address the required points in the task?
- Is the message clear and relevant?
- Are ideas sufficiently developed for the task?
- Is the organization appropriate for an email?
- Is the tone appropriate for the intended recipient?
- Is the language generally accurate and effective?
- Does the writer use appropriate vocabulary and sentence structures?

Give ONE overall estimated score from 0 to 5.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.

Score 5:
The response is highly effective and successfully accomplishes the
purpose of the email. It addresses the required points clearly and
appropriately. Ideas are relevant and sufficiently developed for the
task. The organization and tone are appropriate. Language use is
generally accurate and effective. Minor errors may occur but do not
significantly affect communication.

Score 4:
The response is effective and accomplishes the main purpose of the
email. It addresses the required points and is generally clear and
appropriate. Ideas may be somewhat basic or less fully developed.
The organization and tone are generally appropriate. There may be
some noticeable language errors or limitations, but the message
remains clear and effective overall.

Score 3:
The response generally accomplishes the task and addresses most or
all of the required points, but development may be limited. Ideas
may be basic, repetitive, or insufficiently explained. Language
control is inconsistent, with noticeable grammatical errors,
incorrect word forms, awkward expressions, or sentence structure
problems. The main message is generally understandable.

Score 2:
The response shows limited ability to accomplish the task. One or
more required points may be missing, unclear, or insufficiently
developed. Ideas may be difficult to follow or only partially
relevant. Frequent language errors may significantly affect clarity.

Score 1:
The response demonstrates very limited ability to accomplish the task.
Important parts of the task may be missing or largely irrelevant.
Ideas are severely limited or unclear, and frequent language problems
significantly interfere with communication.

Score 0:
The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.

IMPORTANT:

Do not give a 4 or 5 simply because the student addresses all task
requirements.

However, do not lower a score simply because the student uses simple
but correct language.

Do not require sophisticated vocabulary or complex grammar for a
high score.

A response with several genuine grammatical errors, incorrect verb
forms, subject-verb agreement errors, incorrect prepositions,
incorrect word forms, or unclear expressions should be evaluated
accordingly.

At the same time, do not treat correct but simple language as an
error.
"""


# ---------------------------------------------------------
# STEP 1: EVALUATION
# ---------------------------------------------------------

def evaluate_writing(
    task_type,
    task_prompt,
    student_response
):

    if task_type == "Write for an Academic Discussion":

        rubric = ACADEMIC_DISCUSSION_RUBRIC

    else:

        rubric = EMAIL_RUBRIC


    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Your job is to evaluate a student's response accurately, fairly,
conservatively, and consistently.

TASK TYPE:
{task_type}

TASK PROMPT:
{task_prompt}

STUDENT RESPONSE:
{student_response}

SCORING GUIDELINES:
{rubric}


=========================================================
CORE EVALUATION PRINCIPLES
=========================================================

1. SCORE THE STUDENT'S ACTUAL WRITING.

Evaluate the response exactly as written.

Do not score a hypothetical improved version.

Do not assume what the student intended if the actual writing does
not communicate it.

Do not mentally correct the student's writing before assigning the
score.


=========================================================
2. DO NOT INVENT TASK REQUIREMENTS
=========================================================

Evaluate the actual task prompt.

Do not penalize the student for failing to discuss ideas that the
prompt does not require.

Do not automatically require:

- counterarguments;
- long-term consequences;
- additional perspectives;
- alternative solutions;
- statistical evidence;
- formal research;
- sophisticated analysis;
- multiple examples;

unless these are explicitly required by the task or genuinely needed
to adequately develop the student's own response.

For Academic Discussion, students should express and support an
opinion and contribute to the discussion.

They do not need to address every possible argument.

They do not need to provide formal evidence.

Do not invent a new standard for a score of 5.


=========================================================
3. DISTINGUISH ERRORS FROM STYLE
=========================================================

This is extremely important.

Do NOT identify a sentence as an error simply because you would
personally express it differently.

Do NOT change correct language merely to make it:

- more formal;
- more academic;
- more sophisticated;
- more concise;
- more precise;
- more natural;
- more native-like.

If the student's wording is grammatically correct and understandable,
KEEP IT.

Examples of acceptable language that should NOT automatically be
changed:

"I think..."

"I believe..."

"I agree with Marcus's argument when he says..."

"bikes"

"help"

"good"

Simple language is not automatically incorrect.


=========================================================
4. ONLY IDENTIFY GENUINE LANGUAGE PROBLEMS
=========================================================

Language Feedback should focus only on genuine problems such as:

- grammar errors;
- subject-verb agreement;
- incorrect verb forms;
- incorrect word forms;
- incorrect prepositions;
- incorrect articles when they affect accuracy;
- incorrect sentence structures;
- incorrect word order;
- genuinely unclear wording;
- genuinely incorrect vocabulary;
- language that is inappropriate for the context.

Do not identify a correct sentence as an error simply because another
version sounds better.


=========================================================
5. DO NOT CORRECT THE STUDENT'S IDEAS
=========================================================

The evaluator evaluates language and task performance.

Do not rewrite the student's opinions or claims because they are:

- debatable;
- broad;
- subjective;
- overly general;
- factually questionable;
- not your preferred interpretation.

For example:

"bikes can't be used in winter"

This may be a broad claim, but it is grammatically understandable.

Do not automatically change it to:

"bikes can be difficult or dangerous to use in winter."

That changes the meaning and strength of the student's claim.

If the student's claim is relevant to the discussion, evaluate the
quality of the idea separately from the grammatical correctness of
the sentence.


=========================================================
6. SCORE CONSISTENTLY
=========================================================

Consider the overall combination of:

- task fulfillment;
- relevance;
- development;
- organization;
- language control;
- clarity;
- appropriateness of tone.

Do not give a 4 or 5 simply because the student addresses every
requirement.

Do not give a 3 simply because the ideas are simple.

Do not require advanced vocabulary or complex grammar for a high
score.

The score must reflect the actual quality of the response.


=========================================================
7. LANGUAGE FEEDBACK
=========================================================

Give a maximum of 6 genuine and useful corrections.

Prioritize the most important errors.

If there are fewer than 6 genuine problems, give fewer corrections.

Do not invent corrections to reach 6.

If there are no meaningful language problems, write:

No major language errors.

Use this format:

**Original phrase** → **Correction**

Brief explanation: [short explanation]

IMPORTANT:

Only include a correction if the original contains a genuine language
problem.

Do not include optional stylistic improvements as corrections.

If the original is understandable but awkward, clearly state that it
is understandable but awkward rather than calling it a grammar error.


=========================================================
8. BETTER VERSION PREPARATION
=========================================================

The Better Version will be created in a separate second editing step.

Therefore, DO NOT create or write the Better Version now.

Instead, identify only the genuine corrections that should be applied
to the student's writing.

The next editing step will use ONLY these approved corrections.

This is critical.

Do not suggest corrections that are merely stylistic.

Do not suggest replacing correct vocabulary with synonyms.

Do not suggest changing the student's ideas.

=========================================================
9. REQUIRED OUTPUT
=========================================================

Return ONLY these five sections:

## Estimated Score: X/5

## Why Not the Next Score?

## What You Did Well

## What to Improve

## Language Feedback

Do not include:

- Better Version;
- additional comments;
- model answers;
- alternative rewrites.

=========================================================
SECTION REQUIREMENTS
=========================================================

## Estimated Score: X/5

Give ONE estimated score from 0 to 5.

---------------------------------------------------------

## Why Not the Next Score?

Explain briefly why the response did not receive the next higher
score.

Write 2-4 concise sentences.

The explanation must be consistent with the actual score.

Do not invent weaknesses that are not present.

Do not criticize the student for using simple language if it is
accurate.

---------------------------------------------------------

## What You Did Well

Give exactly 2 specific strengths.

Use bullet points.

Base both strengths on the student's actual response.

Do not give generic praise.

---------------------------------------------------------

## What to Improve

Give exactly 2 specific and actionable suggestions.

Use bullet points.

Focus on the two most important improvements that would help the
student improve.

The suggestions must be appropriate for the student's actual score.

Do not automatically tell every student to use more advanced
vocabulary or complex grammar.

---------------------------------------------------------

## Language Feedback

Give a maximum of 6 genuine corrections.

Use:

**Original phrase** → **Correction**

Brief explanation: [short explanation]

If there are no meaningful language problems, write:

No major language errors.

Do not create a Better Version in this step.
"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": (
                    "You are a careful, fair, and conservative TOEFL "
                    "Writing evaluator. "
                    "Evaluate the student's actual writing. "
                    "Distinguish genuine language errors from stylistic "
                    "preferences. "
                    "Do not invent task requirements. "
                    "Do not require sophisticated vocabulary or complex "
                    "grammar for high scores. "
                    "Do not correct the student's opinions or claims. "
                    "Identify only genuine language problems. "
                    "Do not create a Better Version. "
                    "Follow the required output format exactly."
                )
            },

            {
                "role": "user",
                "content": evaluation_prompt
            }

        ],

        temperature=0.05,

        max_tokens=1800

    )


    return response.choices[0].message.content


# ---------------------------------------------------------
# STEP 2: STRICT MINIMAL-DIFF EDITOR
# ---------------------------------------------------------

def create_better_version(
    student_response,
    language_feedback
):

    editing_prompt = f"""
You are a STRICT MINIMAL-DIFF English editor.

Your task is to correct the student's original response using ONLY
the genuine language corrections identified in the Language Feedback.

You are NOT a writing tutor in this step.

You are NOT rewriting the response.

You are NOT improving the response.

You are NOT making the student sound more academic.

You are NOT making the student sound more natural.

You are NOT making the student sound more sophisticated.

You are performing a MINIMAL-DIFF EDIT.

=========================================================
STUDENT'S ORIGINAL RESPONSE
=========================================================

{student_response}


=========================================================
APPROVED LANGUAGE FEEDBACK
=========================================================

{language_feedback}


=========================================================
ABSOLUTE RULES
=========================================================

RULE 1:

Start with the student's original response.

The default action is to COPY the student's original response.


RULE 2:

Change ONLY genuine language errors identified in the Language
Feedback.

Do not make any additional changes.


RULE 3:

Every substantive change in the Better Version must correspond to a
correction explicitly identified in the Language Feedback.


RULE 4:

Do NOT add new:

- ideas;
- arguments;
- examples;
- explanations;
- evidence;
- claims;
- transitions;
- conclusions;
- supporting details;
- information.


RULE 5:

Do NOT replace correct words with synonyms.

For example, do not change:

"think" → "believe"

"bikes" → "bicycles"

"says" → "argues"

"help" → "assist"

"good" → "beneficial"

unless the original word is genuinely incorrect in context.


RULE 6:

Do NOT change correct grammar.

For example:

"I agree with Marcus's argument when he says..."

is acceptable.

Do not change it to:

"I agree with Marcus's argument that..."


RULE 7:

Do NOT change the student's meaning.

Do not change:

- the strength of a claim;
- the certainty of a claim;
- the scope of a claim;
- the student's opinion;
- the student's argument.


RULE 8:

Do NOT correct factual claims or opinions.

For example:

"bikes can't be used in winter"

may be a broad claim, but do not rewrite it as:

"bikes can be difficult or dangerous to use in winter."

That changes the meaning.


RULE 9:

Do not add phrases such as:

"beyond the cost"

"however"

"for this reason"

"in addition"

"as a result"

"this demonstrates that"

unless those exact words are already in the student's original
response.

Do not add transitions.


RULE 10:

Do not combine or restructure sentences unless this is strictly
necessary to correct a genuine grammatical error.


RULE 11:

If the Language Feedback says that a phrase is merely awkward but
understandable, do NOT automatically rewrite it.

Only change it if the correction is clearly identified as necessary.


RULE 12:

If the Language Feedback says:

"No major language errors."

Return the student's original response EXACTLY as written.


RULE 13:

If there are only two genuine corrections, make only those two
corrections.

Do not search for additional ways to improve the response.


RULE 14:

Punctuation may be corrected when necessary for grammatical
correctness.

Do not make unnecessary stylistic punctuation changes.


=========================================================
FINAL VERIFICATION
=========================================================

Before returning the Better Version, compare it with the student's
original response.

Ask:

1. Did I add any new information?

2. Did I add any new argument?

3. Did I add any new example?

4. Did I add any new transition?

5. Did I replace a correct word with a synonym?

6. Did I change the student's meaning?

7. Did I change a sentence that was already grammatically correct?

8. Did I make a change that was NOT explicitly identified in the
Language Feedback?

If the answer to any of these questions is YES, undo that change.

The Better Version should look almost identical to the original.

MINIMAL EDITING IS ALWAYS PREFERRED.

=========================================================
OUTPUT
=========================================================

Return ONLY the corrected version of the student's response.

Do not include:

- a heading;
- an explanation;
- comments;
- bullet points;
- quotation marks;
- "Better Version";
- introductory text.
"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": (
                    "You are a strict minimal-diff editor. "
                    "Copy the student's original response and make "
                    "only the explicitly approved genuine language "
                    "corrections. "
                    "Do not rewrite. "
                    "Do not add information. "
                    "Do not add arguments. "
                    "Do not add examples. "
                    "Do not add transitions. "
                    "Do not replace correct words with synonyms. "
                    "Do not change the student's meaning. "
                    "Every substantive change must correspond to an "
                    "approved correction. "
                    "Return only the corrected response."
                )
            },

            {
                "role": "user",
                "content": editing_prompt
            }

        ],

        temperature=0.0,

        max_tokens=1800

    )


    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# FORMAT EVALUATION FOR DISPLAY
# ---------------------------------------------------------

def format_evaluation(
    evaluation,
    better_version
):

    # Remove any accidental Better Version section
    # generated by the evaluation model.

    evaluation = re.split(
        r"##\s*Better Version",
        evaluation,
        flags=re.IGNORECASE
    )[0].strip()


    # Convert headings

    lines = evaluation.split("\n")

    processed_lines = []


    for line in lines:

        if line.startswith("## Estimated Score:"):

            heading_text = line.replace(
                "## ",
                "",
                1
            )

            processed_lines.append(
                f"<h2>{heading_text}</h2>"
            )


        elif line.startswith(
            "## Why Not the Next Score?"
        ):

            processed_lines.append(
                "<h2>Why Not the Next Score?</h2>"
            )


        elif line.startswith(
            "## What You Did Well"
        ):

            processed_lines.append(
                "<h2>What You Did Well</h2>"
            )


        elif line.startswith(
            "## What to Improve"
        ):

            processed_lines.append(
                "<h2>What to Improve</h2>"
            )


        elif line.startswith(
            "## Language Feedback"
        ):

            processed_lines.append(
                "<h2>Language Feedback</h2>"
            )


        else:

            processed_lines.append(
                line
            )


    formatted_evaluation = "\n".join(
        processed_lines
    )


    # -----------------------------------------------------
    # BOLD TEXT
    # -----------------------------------------------------

    formatted_evaluation = re.sub(
        r"\*\*(.*?)\*\*",
        r"<strong>\1</strong>",
        formatted_evaluation
    )


    # -----------------------------------------------------
    # BULLET POINTS
    # -----------------------------------------------------

    formatted_evaluation = re.sub(
        r"(?m)^\s*-\s+(.*)$",
        r"<li>\1</li>",
        formatted_evaluation
    )


    formatted_evaluation = re.sub(
        r"((?:<li>.*?</li>\s*)+)",
        r"<ul>\1</ul>",
        formatted_evaluation
    )


    # -----------------------------------------------------
    # SPACING
    # -----------------------------------------------------

    formatted_evaluation = formatted_evaluation.replace(
        "\n\n",
        "<br>"
    )

    formatted_evaluation = formatted_evaluation.replace(
        "\n",
        "<br>"
    )


    # Remove breaks around headings

    formatted_evaluation = re.sub(
        r"<br>\s*(<h2>)",
        r"\1",
        formatted_evaluation
    )

    formatted_evaluation = re.sub(
        r"(</h2>)\s*<br>",
        r"\1",
        formatted_evaluation
    )


    # Remove breaks around lists

    formatted_evaluation = re.sub(
        r"<br>\s*<ul>",
        "<ul>",
        formatted_evaluation
    )

    formatted_evaluation = re.sub(
        r"</ul>\s*<br>",
        "</ul>",
        formatted_evaluation
    )


    # -----------------------------------------------------
    # ADD BETTER VERSION
    # -----------------------------------------------------

    better_version_html = f"""
    <h2>Better Version</h2>

    <div class="better-version">
    {better_version.replace(chr(10), "<br>")}
    </div>
    """


    formatted_evaluation = (
        formatted_evaluation
        + better_version_html
    )


    return formatted_evaluation


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

                # -------------------------------------------------
                # STEP 1
                # EVALUATE AND IDENTIFY GENUINE ERRORS
                # -------------------------------------------------

                evaluation = evaluate_writing(
                    task_type,
                    task_prompt,
                    student_response
                )


                # -------------------------------------------------
                # EXTRACT LANGUAGE FEEDBACK
                # -------------------------------------------------

                language_feedback_match = re.search(
                    r"##\s*Language Feedback\s*(.*)",
                    evaluation,
                    flags=re.IGNORECASE | re.DOTALL
                )


                if language_feedback_match:

                    language_feedback = (
                        language_feedback_match
                        .group(1)
                        .strip()
                    )

                else:

                    language_feedback = (
                        "No major language errors."
                    )


                # -------------------------------------------------
                # STEP 2
                # CREATE STRICT MINIMAL-DIFF VERSION
                # -------------------------------------------------

                better_version = create_better_version(
                    student_response,
                    language_feedback
                )


                # -------------------------------------------------
                # FORMAT EVERYTHING
                # -------------------------------------------------

                formatted_evaluation = format_evaluation(
                    evaluation,
                    better_version
                )


                # -------------------------------------------------
                # DISPLAY
                # -------------------------------------------------

                st.success(
                    "Evaluation complete!"
                )


                st.markdown(
                    f"""
                    <div class="feedback-text">
                    {formatted_evaluation}
                    </div>
                    """,
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
```

