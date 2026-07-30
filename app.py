import streamlit as st
from groq import Groq
import re
import difflib


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="TOEFL Writing AI Grader",
    page_icon="📝",
    layout="centered"
)


# =========================================================
# CUSTOM STYLING
# =========================================================

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
        margin-top: 4px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CONNECT TO GROQ
# =========================================================

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


# =========================================================
# TITLE
# =========================================================

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


# =========================================================
# TASK SELECTION
# =========================================================

task_type = st.selectbox(
    "Choose your TOEFL Writing task:",
    [
        "Write an Email",
        "Write for an Academic Discussion"
    ]
)


# =========================================================
# TASK PROMPT
# =========================================================

st.subheader(
    "TOEFL Task"
)

task_prompt = st.text_area(
    "Paste the TOEFL task or prompt here:",
    height=200,
    placeholder="Paste the complete TOEFL task here..."
)


# =========================================================
# STUDENT RESPONSE
# =========================================================

st.subheader(
    "Your Response"
)

student_response = st.text_area(
    "Paste your TOEFL writing response here:",
    height=300,
    placeholder="Paste your writing response here..."
)


# =========================================================
# RUBRICS
# =========================================================

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
may be somewhat basic or incomplete. Language errors, limited
vocabulary, or sentence structure problems may sometimes affect
clarity, but the main meaning is generally understandable.

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

A high score does NOT require:
- sophisticated vocabulary;
- complex grammar;
- formal research;
- statistics;
- citations;
- multiple counterarguments;
- highly nuanced analysis;
- advanced academic terminology.

Evaluate the student's actual response according to the task.
Do not invent additional requirements.
"""


EMAIL_RUBRIC = """

Evaluate the response as a TOEFL iBT Writing "Write an Email" task.

Consider:

- successful accomplishment of the purpose;
- coverage of required task points;
- clarity and relevance;
- development appropriate to the task;
- organization appropriate for an email;
- tone appropriate for the recipient and situation;
- language accuracy and effectiveness;
- vocabulary and sentence structure.

Give ONE overall estimated score from 0 to 5.

Score 5:
The response is highly effective and successfully accomplishes
the purpose of the email. It addresses the required points clearly
and appropriately. Ideas are relevant and sufficiently developed.
The organization and tone are appropriate. Language is generally
accurate and effective. Minor errors may occur but do not
significantly affect communication.

Score 4:
The response is effective and accomplishes the main purpose.
It addresses the required points and is generally clear and
appropriate. Ideas may be somewhat basic or less fully developed.
The organization and tone are generally appropriate. Some
language errors or limitations may be noticeable, but the message
remains clear and effective overall.

Score 3:
The response generally accomplishes the task and addresses most
or all required points, but development may be limited. Ideas may
be basic, repetitive, or insufficiently explained. Language control
is inconsistent, with noticeable grammatical errors, incorrect
word forms, awkward expressions, or sentence structure problems.
The main message is generally understandable.

Score 2:
The response shows limited ability to accomplish the task. One or
more required points may be missing, unclear, or insufficiently
developed. Ideas may be difficult to follow or only partially
relevant. Frequent language errors may significantly affect clarity.

Score 1:
The response demonstrates very limited ability to accomplish the
task. Important parts may be missing or largely irrelevant. Ideas
are severely limited or unclear, and frequent language problems
significantly interfere with communication.

Score 0:
The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.

Do not require sophisticated vocabulary or complex grammar for a
high score. Accurate simple language can receive a high score.
"""


# =========================================================
# MAIN EVALUATION FUNCTION
# =========================================================

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

Your job is to evaluate a student's writing accurately, fairly,
conservatively, and consistently.

You must evaluate the student's actual writing.

You must NOT rewrite the student's ideas.

You must NOT make the student sound more academic simply because
you prefer academic language.

You must NOT improve the student's argument.

You must NOT change the student's meaning.

=========================================================
TASK TYPE
=========================================================

{task_type}

=========================================================
TASK PROMPT
=========================================================

{task_prompt}

=========================================================
STUDENT RESPONSE
=========================================================

{student_response}

=========================================================
SCORING RUBRIC
=========================================================

{rubric}

=========================================================
CORE PRINCIPLE 1: SCORE THE ACTUAL RESPONSE
=========================================================

Score exactly what the student wrote.

Do not score what the student probably intended to write.

Do not mentally correct grammar before scoring.

Do not imagine additional ideas that the student could have included.

Do not give credit for improvements that appear only in the
Better Version.

=========================================================
CORE PRINCIPLE 2: EVALUATE THE ACTUAL TASK
=========================================================

Use the task prompt to determine what the student needs to do.

Do not invent additional requirements.

For Academic Discussion, the student should express and support
an opinion and contribute to the discussion.

The student does NOT automatically need:

- a counterargument;
- a rebuttal;
- a second example;
- formal evidence;
- statistics;
- research;
- a long-term consequence;
- a solution;
- a nuanced analysis;

unless the task itself requires these things or they are genuinely
necessary to develop the response adequately.

Do not lower a score simply because the student did not include
something the task did not require.

=========================================================
CORE PRINCIPLE 3: SIMPLE LANGUAGE IS NOT AN ERROR
=========================================================

Do not replace correct simple language with more sophisticated
language.

These are NOT automatically errors:

"I think..."

"I believe..."

"I agree with..."

"help"

"good"

"bad"

"bikes"

"older adults"

"people"

"important"

A simpler expression can be completely appropriate.

Do not change a correct expression simply because a more academic
or sophisticated alternative exists.

=========================================================
CORE PRINCIPLE 4: THREE DIFFERENT CATEGORIES
=========================================================

For every possible language issue, decide which category applies.

CATEGORY A: GENUINE ERROR

The language is grammatically incorrect, incorrectly formed, or
clearly inappropriate in context.

Examples include:

- incorrect verb forms;
- subject-verb agreement errors;
- incorrect prepositions;
- incorrect word forms;
- incorrect sentence structures;
- incorrect articles when they affect accuracy;
- incorrect word order;
- clearly incorrect vocabulary;
- language that creates genuine confusion.

These may be corrected.

CATEGORY B: AWKWARD BUT UNDERSTANDABLE

The meaning is clear, but the expression is less natural or
awkward.

Do NOT automatically treat this as a grammar error.

If you mention it, explicitly say:

"The meaning is understandable, but the phrasing is awkward."

Only include it in Language Feedback if the change would be
genuinely useful for the student's development.

CATEGORY C: ACCEPTABLE LANGUAGE

The sentence is grammatically correct and understandable.

Do NOT change it.

Do NOT include it in Language Feedback.

=========================================================
CORE PRINCIPLE 5: DO NOT CHANGE MEANING
=========================================================

This is one of the most important rules.

Never change the student's:

- opinion;
- claim;
- argument;
- degree of certainty;
- degree of strength;
- scope;
- factual claim;
- personal example;
- interpretation.

For example, if a student writes:

"Bikes can't be used in winter."

Do NOT automatically change this to:

"Bikes can be difficult or dangerous to use in winter."

The second sentence changes the strength and meaning of the
student's claim.

Even if the original claim seems too broad, it is still the
student's claim.

Evaluate the idea separately from the language.

Do not correct ideas merely because you disagree with them or
would express them differently.

=========================================================
CORE PRINCIPLE 6: DO NOT CONFUSE STYLE WITH ERROR
=========================================================

Do NOT correct language merely because you prefer:

- a different synonym;
- a more formal expression;
- a more academic expression;
- a more sophisticated expression;
- a more concise expression;
- a more natural expression;
- a more native-like expression.

For example:

"I think investing in buses is important."

Do NOT automatically change this to:

"I believe that investment in public transportation is essential."

The original may be completely acceptable.

=========================================================
CORE PRINCIPLE 7: LANGUAGE FEEDBACK MUST BE TRACEABLE
=========================================================

Only identify genuine and useful corrections.

Maximum: 6 corrections.

If there are fewer than 6 genuine errors, give fewer.

Do NOT invent errors to fill the list.

Do NOT include a correct sentence as a correction.

Do NOT write:

Original → No correction needed.

That is NOT a correction.

If there are no meaningful errors, write:

No major language errors.

Every correction must contain:

**Original phrase** → **Correction**

Brief explanation: [short explanation]

The correction must fix a genuine language problem.

=========================================================
CORE PRINCIPLE 8: PUNCTUATION
=========================================================

Correct punctuation only when it is necessary for grammatical
correctness or clarity.

Do not change punctuation simply for stylistic preference.

Do not turn every missing comma into a major language error.

Prioritize meaningful errors over minor punctuation issues.

=========================================================
CORE PRINCIPLE 9: BETTER VERSION
=========================================================

The Better Version is NOT a model answer.

It is NOT a response rewritten to receive 5/5.

It is NOT a more sophisticated version.

It is NOT a stronger argument.

It is NOT an improved essay.

It is the student's own response with ONLY genuine language
corrections applied.

The Better Version must preserve:

- all original ideas;
- all original arguments;
- all original examples;
- all original claims;
- the student's opinion;
- the student's meaning;
- the student's approximate language level;
- the student's personal voice;
- the student's original structure whenever possible.

=========================================================
CORE PRINCIPLE 10: ZERO-ADDITION RULE
=========================================================

The Better Version must NOT add:

- new arguments;
- new examples;
- new evidence;
- new explanations;
- new details;
- new claims;
- new counterarguments;
- new conclusions;
- new transitions;
- new vocabulary merely for sophistication.

If a sentence is correct, leave it unchanged.

If an idea is simple, leave it simple.

If an argument is incomplete, do not complete it.

If an example is basic, do not improve it.

If the student did not say it, do not add it.

=========================================================
CORE PRINCIPLE 11: ZERO-SUBSTITUTION RULE
=========================================================

Do not replace correct words with synonyms.

Do NOT automatically change:

think → believe

say → argue

help → assist

bikes → bicycles

good → beneficial

important → significant

people → individuals

unless the original word is genuinely incorrect in context.

=========================================================
CORE PRINCIPLE 12: ZERO-MEANING-CHANGE RULE
=========================================================

Before producing the Better Version, compare every change against
the original.

For every change, ask:

1. Was the original genuinely incorrect?

2. Was this exact problem identified in Language Feedback?

3. Does the correction preserve the original meaning?

4. Does the correction preserve the original strength of the claim?

5. Does the correction preserve the student's opinion?

6. Did I add any information?

7. Did I add any argument?

8. Did I add any example?

9. Did I make the language more sophisticated unnecessarily?

If any answer indicates a problem, DO NOT make the change.

=========================================================
CORE PRINCIPLE 13: BETTER VERSION MUST BE MINIMAL
=========================================================

The Better Version should look almost identical to the original
when the original contains only a few errors.

For example, if the student has two genuine grammar errors,
correct those two errors.

Do not rewrite the entire response.

Do not improve every sentence.

Do not change vocabulary that is already correct.

Do not add supporting ideas.

=========================================================
CORE PRINCIPLE 14: SCORE AND LANGUAGE FEEDBACK MUST AGREE
=========================================================

The score and Language Feedback must be consistent.

Do not say the response contains "minor language errors" if the
Language Feedback identifies only stylistic preferences.

Do not say "No major language errors" and then provide multiple
language corrections.

Do not give a 4 or 5 merely because the student completed the task.

Do not give a lower score merely because the student uses simple
but accurate language.

=========================================================
REQUIRED OUTPUT
=========================================================

Return EXACTLY these six sections:

## Estimated Score: X/5

## Why Not the Next Score?

## What You Did Well

## What to Improve

## Language Feedback

## Better Version

=========================================================
SECTION 1: ESTIMATED SCORE
=========================================================

Give ONE score from 0 to 5.

=========================================================
SECTION 2: WHY NOT THE NEXT SCORE?
=========================================================

Write 2-4 concise sentences.

Explain the actual reason the response did not receive the next
higher score.

Do not invent weaknesses.

Do not require sophistication.

For a 5/5 response, write:

"The response demonstrates the characteristics of the highest score
level. There are no significant limitations that prevent it from
receiving a 5/5."

=========================================================
SECTION 3: WHAT YOU DID WELL
=========================================================

Give exactly 2 specific strengths.

Use bullet points.

Base them on the actual response.

=========================================================
SECTION 4: WHAT TO IMPROVE
=========================================================

Give exactly 2 specific and actionable suggestions.

Use bullet points.

Focus on the two most important improvements for this particular
response.

Do not automatically recommend advanced vocabulary.

Do not automatically recommend complex grammar.

=========================================================
SECTION 5: LANGUAGE FEEDBACK
=========================================================

Maximum 6 genuine corrections.

Use:

**Original phrase** → **Correction**

Brief explanation: [short explanation]

Do not include stylistic preferences.

Do not include "No correction needed" as a correction.

If there are no meaningful errors, write:

No major language errors.

=========================================================
SECTION 6: BETTER VERSION
=========================================================

Start from the student's original response.

Apply ONLY the genuine corrections identified in Language Feedback.

Do NOT make any other changes.

The Better Version must be as close as possible to the original.

Return the final corrected response only.

=========================================================
FINAL INTERNAL CHECK
=========================================================

Before returning the answer, silently compare the Better Version
with the original.

Remove any change that:

- adds information;
- adds an argument;
- adds an example;
- changes meaning;
- changes the strength of a claim;
- changes the student's opinion;
- replaces correct vocabulary with a synonym;
- improves style without correcting an error;
- was not identified as a genuine correction;
- makes the response more sophisticated unnecessarily.

The Better Version must be a MINIMAL-DIFF correction of the
student's original response.
"""


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": (
                    "You are a conservative TOEFL Writing evaluator "
                    "and strict minimal-diff editor. "
                    "Evaluate the student's actual writing. "
                    "Do not invent task requirements. "
                    "Do not confuse style with error. "
                    "Do not change correct language. "
                    "Do not change the student's meaning. "
                    "Do not improve or strengthen the student's "
                    "arguments. "
                    "Identify only genuine language errors. "
                    "The Better Version must remain extremely close "
                    "to the student's original response. "
                    "Never add information or new ideas. "
                    "Follow the required six-section format exactly."
                )
            },

            {
                "role": "user",
                "content": evaluation_prompt
            }

        ],

        temperature=0.0,

        max_tokens=2400
    )


    return response.choices[0].message.content.strip()


# =========================================================
# FORMAT AI RESPONSE
# =========================================================

def format_evaluation(evaluation):

    # Remove accidental code fences
    evaluation = evaluation.replace(
        "```markdown",
        ""
    ).replace(
        "```",
        ""
    ).strip()


    # Convert headings
    lines = evaluation.split("\n")

    processed_lines = []


    for line in lines:

        stripped = line.strip()


        if stripped.startswith(
            "## Estimated Score:"
        ):

            heading_text = stripped.replace(
                "## ",
                "",
                1
            )

            processed_lines.append(
                f"<h2>{heading_text}</h2>"
            )


        elif stripped.startswith(
            "## Why Not the Next Score?"
        ):

            processed_lines.append(
                "<h2>Why Not the Next Score?</h2>"
            )


        elif stripped.startswith(
            "## What You Did Well"
        ):

            processed_lines.append(
                "<h2>What You Did Well</h2>"
            )


        elif stripped.startswith(
            "## What to Improve"
        ):

            processed_lines.append(
                "<h2>What to Improve</h2>"
            )


        elif stripped.startswith(
            "## Language Feedback"
        ):

            processed_lines.append(
                "<h2>Language Feedback</h2>"
            )


        elif stripped.startswith(
            "## Better Version"
        ):

            processed_lines.append(
                "<h2>Better Version</h2>"
            )


        else:

            processed_lines.append(
                line
            )


    formatted = "\n".join(
        processed_lines
    )


    # Bold
    formatted = re.sub(
        r"\*\*(.*?)\*\*",
        r"<strong>\1</strong>",
        formatted
    )


    # Bullet points
    formatted = re.sub(
        r"(?m)^\s*-\s+(.*)$",
        r"<li>\1</li>",
        formatted
    )


    # Wrap consecutive list items
    formatted = re.sub(
        r"((?:<li>.*?</li>\s*)+)",
        r"<ul>\1</ul>",
        formatted
    )


    # Spacing
    formatted = formatted.replace(
        "\n\n",
        "<br>"
    )

    formatted = formatted.replace(
        "\n",
        "<br>"
    )


    # Remove excessive breaks
    formatted = re.sub(
        r"<br>\s*(<h2>)",
        r"\1",
        formatted
    )

    formatted = re.sub(
        r"(</h2>)\s*<br>",
        r"\1",
        formatted
    )

    formatted = re.sub(
        r"<br>\s*<ul>",
        "<ul>",
        formatted
    )

    formatted = re.sub(
        r"</ul>\s*<br>",
        "</ul>",
        formatted
    )


    return formatted


# =========================================================
# EVALUATE BUTTON
# =========================================================

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


                # Display success message
                st.success(
                    "Evaluation complete!"
                )


                # Format and display
                formatted_evaluation = format_evaluation(
                    evaluation
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

                error_message = str(e)


                if "429" in error_message:

                    st.error(
                        "The AI service has temporarily reached "
                        "its usage limit. Please wait and try again "
                        "later."
                    )

                    st.warning(
                        "This is a Groq API rate-limit issue, "
                        "not an error in your writing or app."
                    )

                else:

                    st.error(
                        "Something went wrong while evaluating "
                        "your response."
                    )

                    st.code(
                        error_message
                    )
