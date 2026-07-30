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

    /* Main feedback container */
    .feedback-text {
        text-align: justify;
        line-height: 1.6;
        font-size: 16px;
    }

    /* Section headings */
    .feedback-text h2 {
        text-align: left;
        margin-top: 18px;
        margin-bottom: 8px;
        font-size: 21px;
        font-weight: 600;
    }

    /* Bullet points */
    .feedback-text ul {
        text-align: justify;
        margin-top: 4px;
        margin-bottom: 10px;
        padding-left: 25px;
    }

    .feedback-text li {
        margin-bottom: 6px;
    }

    /* Better version */
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
# ACADEMIC DISCUSSION RUBRIC
# ---------------------------------------------------------

ACADEMIC_DISCUSSION_RUBRIC = """

Evaluate the response using the TOEFL iBT Writing for an Academic
Discussion scoring scale from 0 to 5.

The score must reflect the student's ACTUAL response.

Do not score a rewritten or improved version.

---------------------------------------------------------
SCORE 5
---------------------------------------------------------

The response is highly effective.

It clearly and effectively contributes to the discussion.

It expresses a clear position or idea and supports it with relevant,
well-developed explanations, reasons, examples, or details.

The response demonstrates strong organization and clear connections
between ideas.

Language use is effective and generally accurate, with appropriate
vocabulary and grammar.

Minor language errors may occur, but they do not significantly affect
clarity, precision, or effectiveness.

---------------------------------------------------------
SCORE 4
---------------------------------------------------------

The response is effective and relevant.

It clearly expresses a position or idea and makes a meaningful
contribution to the discussion.

It addresses the task effectively and engages with the discussion,
including other participants' ideas when appropriate.

The response provides relevant reasons, explanations, examples, or
details.

Development may not be as extensive or sophisticated as a 5, but the
ideas are sufficiently developed for the task.

Language may contain several minor or moderate errors, awkward
expressions, or limitations in vocabulary or grammar, but the response
remains clear and effective overall.

IMPORTANT:

A response can receive a 4 even if it contains several genuine
language errors.

Do NOT automatically assign a 3 simply because the response contains
grammar or vocabulary errors.

A 4 is appropriate when the overall response is effective, relevant,
organized, and understandable, even if the language is not consistently
accurate.

Simple but accurate language can receive a 4.

The student does NOT need sophisticated vocabulary or complex grammar
to receive a 4.

---------------------------------------------------------
SCORE 3
---------------------------------------------------------

The response is generally relevant and understandable but has
noticeable limitations.

The response may:

- provide limited or incomplete development;
- give reasons without sufficient explanation;
- provide relevant ideas but fail to connect them clearly to the main
  argument;
- engage with the discussion only partially;
- contain language errors that sometimes affect clarity or precision;
- demonstrate inconsistent control of grammar or vocabulary.

A score of 3 should generally reflect more substantial limitations than
simply having several language errors.

Do NOT assign a 3 merely because:

- the vocabulary is simple;
- the grammar is not sophisticated;
- the response contains a few or several minor errors;
- the student does not provide formal academic evidence;
- the student uses straightforward language;
- the student does not develop every individual point extensively.

If the response is clearly effective overall and its meaning is easy to
follow despite some language errors, strongly consider a 4 before
assigning a 3.

---------------------------------------------------------
SCORE 2
---------------------------------------------------------

The response demonstrates limited ability to contribute to the
discussion.

Ideas may be unclear, insufficiently developed, repetitive, or only
partially relevant.

The response may fail to address important aspects of the task.

Language errors and limited language control may frequently interfere
with clarity and communication.

---------------------------------------------------------
SCORE 1
---------------------------------------------------------

The response provides very little relevant content or does not
meaningfully contribute to the discussion.

Ideas are severely limited, unclear, or largely irrelevant.

Frequent language problems significantly interfere with communication.

---------------------------------------------------------
SCORE 0
---------------------------------------------------------

The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.

"""


# ---------------------------------------------------------
# EMAIL RUBRIC
# ---------------------------------------------------------

EMAIL_RUBRIC = """

Evaluate the response as a TOEFL iBT Writing "Write an Email" task.

Consider the following areas as part of the overall evaluation:

- Does the writer successfully accomplish the purpose of the email?
- Does the writer address the required points in the task?
- Is the message clear, relevant, and appropriately developed?
- Is the organization appropriate for an email?
- Is the tone appropriate for the intended recipient and situation?
- Is the language generally accurate and effective?
- Does the writer use appropriate vocabulary and sentence structures?

Give ONE overall estimated score from 0 to 5.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.

---------------------------------------------------------
SCORE 5
---------------------------------------------------------

The response is highly effective and successfully accomplishes the
purpose of the email.

It addresses the required points clearly and appropriately.

Ideas are relevant and sufficiently developed for the task.

The organization and tone are appropriate for the intended recipient
and situation.

Language use is generally accurate and effective.

Minor errors may occur but do not significantly affect communication.

---------------------------------------------------------
SCORE 4
---------------------------------------------------------

The response is effective and accomplishes the main purpose of the
email.

It addresses the required points and is generally clear and
appropriate.

Ideas may be somewhat basic or less fully developed than those of a
5-level response.

The organization and tone are generally appropriate.

There may be several noticeable language errors or limitations, but
the message remains clear and effective overall.

IMPORTANT:

A response can receive a 4 even if it contains several genuine
language errors.

Do NOT automatically assign a 3 simply because the response contains
grammar errors, vocabulary limitations, or awkward expressions.

The overall effectiveness of the email is more important than the
presence of isolated or moderate language errors.

---------------------------------------------------------
SCORE 3
---------------------------------------------------------

The response generally accomplishes the task but has noticeable
limitations.

Development may be limited.

Ideas may be basic, repetitive, or insufficiently explained.

One or more parts of the task may be addressed only minimally.

Language control may be inconsistent, with noticeable grammatical
errors, incorrect word forms, awkward expressions, or sentence
structure problems.

The main message is generally understandable, but these problems may
sometimes affect clarity or effectiveness.

A score of 3 should reflect meaningful limitations in the overall
effectiveness of the response, not merely the presence of several
language errors.

---------------------------------------------------------
SCORE 2
---------------------------------------------------------

The response shows limited ability to accomplish the task.

One or more required points may be missing, unclear, or insufficiently
developed.

Ideas may be difficult to follow or only partially relevant.

Frequent language errors and limited language control may significantly
affect clarity and communication.

---------------------------------------------------------
SCORE 1
---------------------------------------------------------

The response demonstrates very limited ability to accomplish the task.

Important parts of the task may be missing or largely irrelevant.

Ideas are severely limited or unclear.

Frequent language problems significantly interfere with communication.

---------------------------------------------------------
SCORE 0
---------------------------------------------------------

The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.

"""


# ---------------------------------------------------------
# UNIVERSAL EVALUATION PRINCIPLES
# ---------------------------------------------------------

GENERAL_EVALUATION_PRINCIPLES = """

=========================================================
UNIVERSAL EVALUATION PRINCIPLES
=========================================================

1. EVALUATE THE SPECIFIC TASK AND RESPONSE
---------------------------------------------------------

First, identify the requirements of the task.

Then evaluate whether the student's response:

- addresses the task;
- fulfills the required communicative purpose;
- responds to the relevant questions or points;
- expresses a clear position, purpose, or message when required;
- provides relevant support, explanation, reasons, examples, or details
  when appropriate;
- contributes original ideas when required;
- engages with other people's ideas when the task requires this;
- maintains appropriate organization;
- uses language that is clear and effective for the task.

Do not apply the same expectations mechanically to every prompt.

The requirements of the specific task should determine what counts as
effective development and support.


2. SCORE THE RESPONSE GLOBALLY
---------------------------------------------------------

Evaluate the overall effectiveness of the response before focusing on
individual language errors.

Consider the combined effect of:

- task fulfillment;
- relevance;
- development;
- organization;
- clarity;
- language control;
- vocabulary;
- grammar;
- appropriateness for the task.

Do not allow one category to automatically determine the score.

Several grammar errors do NOT automatically mean a score of 3.

Simple vocabulary does NOT automatically mean a score of 3.

A response does NOT need sophisticated grammar to receive a 4 or 5.

A response does NOT need formal academic evidence unless the task
specifically requires it.

Judge the response as a whole.


3. DISTINGUISH SCORE 3 FROM SCORE 4 CAREFULLY
---------------------------------------------------------

A score of 4 should be considered when the response is effective
overall, even if it contains some genuine language errors.

A response may receive a 4 when:

- the main purpose or position is clear;
- the response is relevant;
- the student meaningfully addresses the task;
- ideas are adequately supported for the task;
- organization is generally effective;
- the message is clear overall;
- language errors do not significantly interfere with communication.

A response should generally receive a 3 when its limitations are more
substantial and affect the overall effectiveness of the response.

Examples of substantial limitations may include:

- limited or incomplete development;
- insufficient support for important ideas;
- weak or unclear connections between ideas;
- incomplete fulfillment of the task;
- frequent language problems that affect clarity;
- limited control of language that makes the response noticeably less
  effective;
- difficulty communicating the intended meaning consistently.

Do not assign a 3 simply because the student's language is simple.

Do not assign a 3 simply because the student makes several errors.

Do not assign a 4 simply because the student completes every task
requirement.

Use the total quality of the response to determine the score.


4. DO NOT PENALIZE SIMPLE BUT EFFECTIVE LANGUAGE
---------------------------------------------------------

Do not require sophisticated vocabulary or complex grammar for a high
score.

If a student uses simple language that is:

- accurate;
- clear;
- relevant;
- appropriate;
- effective;

do not recommend replacing it with more sophisticated language merely
for stylistic reasons.

Do not automatically change:

"I think..."

to:

"I believe..."

Do not automatically change:

"good"

to:

"beneficial"

Do not automatically change:

"help"

to:

"facilitate"

unless the original wording is genuinely inaccurate, inappropriate,
unclear, or ineffective in context.

Evaluate the language the student chose, not the language you would
personally prefer.


5. DISTINGUISH REAL ERRORS FROM OPTIONAL IMPROVEMENTS
---------------------------------------------------------

Only identify genuine language problems.

These may include:

- grammatical errors;
- subject-verb agreement errors;
- incorrect verb forms;
- incorrect word forms;
- incorrect prepositions;
- incorrect articles when they affect accuracy;
- incorrect sentence structures;
- incorrect word order;
- incorrect pronoun reference;
- inappropriate or inaccurate vocabulary;
- expressions that are genuinely unclear or confusing;
- language that is inappropriate for the context.

Do NOT identify a sentence as an error merely because:

- another version sounds more natural;
- another version is more formal;
- another version is more academic;
- another version is more sophisticated;
- another version is more concise;
- another version sounds more native-like.

If a sentence is grammatically correct and understandable, do not
present an alternative as a correction.


6. DISTINGUISH DIFFERENT TYPES OF LANGUAGE PROBLEMS
---------------------------------------------------------

When identifying a problem, determine what type of problem it is.

Possible categories include:

A. Grammar error

The original is grammatically incorrect.

B. Vocabulary or word-choice error

The word is incorrect or inappropriate for the intended meaning.

C. Precision problem

The language is grammatically correct but does not express the
intended meaning precisely enough.

D. Awkward phrasing

The meaning is understandable, but the structure is noticeably awkward.

E. Clarity problem

The wording makes the intended meaning difficult to understand.

F. Stylistic preference

The original is correct and acceptable, but another version is
possible.

Only categories A-E should normally appear in Language Feedback.

Do not present category F as an error.


7. EVALUATE DEVELOPMENT RELATIVE TO THE TASK
---------------------------------------------------------

Do not use a fixed definition of "well developed" for every task.

The amount and type of development required depends on:

- the task type;
- the task prompt;
- the required response;
- the student's position or purpose;
- the length and complexity of the task.

A response may be adequately developed with a combination of:

- a clear position or purpose;
- relevant reasons;
- explanation;
- examples;
- specific details;

depending on what the particular task requires.

Do not require every reason to be extensively developed.

Do not require formal evidence unless the task requires it.

Do not automatically tell every student to "add more examples."

First determine whether the student already provides sufficient support.

If the student provides examples, evaluate whether the examples are
relevant and effectively connected to the main point.

If the student provides several reasons but does not explain one of them
clearly, recommend improving the explanation of that specific reason.

If the student has adequate development, do not invent a development
problem.


8. IMPROVEMENT FEEDBACK MUST BE RESPONSE-SPECIFIC
---------------------------------------------------------

Give exactly two actionable suggestions.

The suggestions must be based on actual weaknesses in the student's
response.

Before recommending an improvement, check whether the student has
already demonstrated that skill.

If the student already provides examples, do not tell them simply to
"provide examples."

If the student already addresses an opposing view, do not tell them
simply to "address an opposing view."

If the student already explains their ideas adequately, do not claim
that the response lacks development.

Instead, identify the most important remaining limitation.

Suggestions may focus on:

- clearer explanation;
- stronger connections between ideas;
- more relevant support;
- better organization;
- more precise vocabulary;
- improved grammar accuracy;
- clearer sentence structure;
- more complete task fulfillment;

but only when the response genuinely needs improvement in that area.


9. DO NOT INVENT WEAKNESSES
---------------------------------------------------------

Every criticism must be supported by the student's actual response.

Do not invent:

- missing examples;
- missing arguments;
- missing explanations;
- missing task requirements;
- language errors;
- organizational problems.

If the student has already done something successfully, recognize that
fact and do not recommend doing the same thing again.

The evaluation must be based on evidence from the student's actual
response.


10. LANGUAGE FEEDBACK MUST BE PRIORITIZED
---------------------------------------------------------

Give a maximum of 6 corrections.

Do not try to find 6 corrections if fewer genuine problems exist.

Prioritize:

1. errors that affect meaning;
2. repeated grammatical errors;
3. important vocabulary or word-choice problems;
4. errors that are particularly useful for the student to learn;
5. clarity problems that affect communication.

Do not spend all six corrections on minor punctuation.

If there are no meaningful language problems, write:

"No major language errors."


11. CORRECTIONS MUST PRESERVE THE STUDENT'S MEANING
---------------------------------------------------------

Every correction must preserve the original intended meaning.

Do not change the student's argument while correcting language.

Do not introduce new ideas into a correction.

Corrections should improve the student's existing language rather than
replace the student's ideas.


12. THE BETTER VERSION MUST BE AN EDITED VERSION
---------------------------------------------------------

The Better Version is NOT a model answer.

It is NOT a new response created by the AI.

It is NOT an opportunity to demonstrate advanced English.

It is a lightly edited version of the student's original response.

The Better Version must preserve the student's:

- ideas;
- arguments;
- reasons;
- examples;
- opinions;
- purpose;
- personal voice;
- overall structure whenever possible.

The Better Version may:

- correct genuine grammar errors;
- correct incorrect word choices;
- correct incorrect word forms;
- improve unclear sentence structures;
- improve awkward word order;
- improve clarity when necessary;
- make limited organizational adjustments when genuinely needed.

The Better Version must NOT:

- add new arguments;
- add new examples;
- add new evidence;
- add new facts;
- add new reasons;
- add new consequences;
- add new claims;
- introduce information not present in the student's response;
- substantially increase the sophistication of the writing.

Do not delete relevant ideas simply to make the response shorter.

Do not replace correct language with more advanced language.

Do not rewrite the response from scratch.

The final version should be recognizably the student's original writing
with necessary corrections and limited improvements.


13. EVERY SUBSTANTIVE CHANGE SHOULD BE JUSTIFIED
---------------------------------------------------------

The Better Version should generally reflect the Language Feedback.

If a meaningful grammar, vocabulary, precision, or clarity change is
made in the Better Version, it should normally appear in Language
Feedback.

Minor punctuation adjustments do not always need individual feedback.

Do not make unexplained substantive changes to the student's writing.


14. SCORE EXPLANATION MUST BE SPECIFIC
---------------------------------------------------------

The "Why Not the Next Score?" section must explain the actual limitation
that prevents the next score.

Do not use generic statements such as:

- "The vocabulary is not sophisticated enough."
- "The grammar is not complex enough."
- "The response needs more advanced language."

unless this is genuinely affecting the response's effectiveness.

For a 4/5 response, identify the specific limitation that prevents a 5.

For a 3/5 response, identify the specific limitation that prevents a 4.

For a 5/5 response, state that there are no significant limitations
preventing the highest score.

The explanation must be based on the actual response and task.


15. FEEDBACK MUST BE INTERNALLY CONSISTENT
---------------------------------------------------------

The following sections must agree with one another:

- Estimated Score;
- Why Not the Next Score?;
- What You Did Well;
- What to Improve;
- Language Feedback;
- Better Version.

Do not say the student has a language problem in one section and then
say there are no language problems in another.

Do not recommend adding examples if the response already contains
adequate examples.

Do not criticize missing development if the response is adequately
developed.

Do not make changes in the Better Version that are not supported by the
Language Feedback or necessary for clarity.

The evaluation should read as one coherent assessment of the same
student response.


16. DO NOT OVER-CORRECT THE BETTER VERSION
---------------------------------------------------------

The Better Version should contain the minimum changes necessary to
produce a clearer and more accurate version of the student's response.

When deciding whether to change a sentence, ask:

"Is the original actually incorrect, unclear, or significantly awkward?"

If the answer is no, keep the original.

The goal is not to make the student sound like a native speaker.

The goal is to show the student how to improve their own writing.

"""


# ---------------------------------------------------------
# EVALUATION FUNCTION
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


    # -----------------------------------------------------
    # COMPLETE EVALUATION PROMPT
    # -----------------------------------------------------

    evaluation_prompt = f"""

You are an experienced TOEFL Writing teacher and evaluator.

Your job is to evaluate a student's response accurately, fairly,
consistently, and according to the scoring guidelines.

You must evaluate the student's ACTUAL WRITING.

Do not evaluate an imagined improved version.

---------------------------------------------------------
TASK TYPE
---------------------------------------------------------

{task_type}

---------------------------------------------------------
TASK PROMPT
---------------------------------------------------------

{task_prompt}

---------------------------------------------------------
STUDENT RESPONSE
---------------------------------------------------------

{student_response}

---------------------------------------------------------
SCORING GUIDELINES
---------------------------------------------------------

{rubric}

{GENERAL_EVALUATION_PRINCIPLES}


=========================================================
FINAL OUTPUT REQUIREMENTS
=========================================================

Return ONLY the following six sections, in exactly this order:

## Estimated Score: X/5

## Why Not the Next Score?

## What You Did Well

## What to Improve

## Language Feedback

## Better Version


---------------------------------------------------------
ESTIMATED SCORE
---------------------------------------------------------

Give ONE estimated score from 0 to 5.

The score must be based on the student's actual response.

Do not give separate scores for grammar, vocabulary, organization,
development, or task fulfillment.

Do not calculate an average of separate categories.


---------------------------------------------------------
WHY NOT THE NEXT SCORE?
---------------------------------------------------------

Write 2-4 concise sentences.

The explanation must be specific to the actual response.

For a 5/5 response, write:

"The response demonstrates the characteristics of the highest score
level. There are no significant limitations that prevent it from
receiving a 5/5."

For a 4/5 response, explain the specific limitation or limitations that
prevent a 5.

For a 3/5 response, explain the specific limitation or limitations that
prevent a 4.

For a 2/5 response, explain the specific limitation or limitations that
prevent a 3.

For a 1/5 response, explain the specific limitation or limitations that
prevent a 2.

Do not automatically mention sophisticated vocabulary or complex
grammar.

Do not invent a weakness simply because the score is not 5.


---------------------------------------------------------
WHAT YOU DID WELL
---------------------------------------------------------

Give exactly 2 specific strengths.

Use bullet points.

Base both strengths on the student's actual response.

Do not give generic praise.

Do not add a third strength.


---------------------------------------------------------
WHAT TO IMPROVE
---------------------------------------------------------

Give exactly 2 specific and actionable suggestions.

Use bullet points.

Base both suggestions on actual weaknesses.

Do not recommend something the student has already done successfully.

Do not automatically recommend:

- more examples;
- more advanced vocabulary;
- more complex grammar;
- counterarguments.

Only recommend these when they are genuinely relevant to the student's
actual response.


---------------------------------------------------------
LANGUAGE FEEDBACK
---------------------------------------------------------

Give a maximum of 6 genuine and useful corrections.

Use this format:

**Original phrase** → **Correction**

Brief explanation: Explain briefly why the change is needed.

Only include genuine problems.

Do not include stylistic alternatives as errors.

If a phrase is grammatically correct but could be more precise, explain
that it is a precision issue rather than a grammar error.

If there are no meaningful language problems, write:

"No major language errors."


---------------------------------------------------------
BETTER VERSION
---------------------------------------------------------

Provide a lightly improved version of the student's response.

The Better Version must remain recognizably the student's own writing.

Preserve:

- the student's ideas;
- arguments;
- reasons;
- examples;
- opinions;
- purpose;
- personal voice;
- overall structure whenever possible.

Correct genuine errors.

Improve clarity only when necessary.

Do not substantially rewrite the response.

Do not introduce new arguments.

Do not introduce new information.

Do not add new examples.

Do not add new evidence.

Do not add new reasons.

Do not add new conclusions.

Do not make the response significantly more sophisticated than the
original.

Do not delete relevant ideas.

Do not replace correct language with more sophisticated alternatives.

The Better Version should be an EDITED VERSION of the student's
response, not a new model answer.

The Better Version itself must be the final content.

Do not add any explanation after the Better Version.


---------------------------------------------------------
FORMATTING
---------------------------------------------------------

Every heading must begin with exactly two hash symbols followed by a
space.

Every heading must appear on its own separate line.

Leave one blank line between headings and the text that follows.

Leave one blank line between sections.

Use bullet points for exactly 2 strengths.

Use bullet points for exactly 2 improvements.

Use bold only when useful for Original and Correction in Language
Feedback.

Do not create any additional sections.

Do not create a section called "Why?"

Do not create a section called "Language Corrections."

Do not create a section called "Additional Comments."

Do not add text before the first section.

Do not add text after the Better Version.

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
                    "You are a careful, fair, and consistent TOEFL "
                    "Writing evaluator. "
                    "Evaluate the student's actual writing and the "
                    "specific task provided. "
                    "Do not use fixed feedback that is unrelated to "
                    "the student's response. "
                    "Do not confuse stylistic preferences with errors. "
                    "Do not automatically lower a score because of "
                    "several language errors if the response is "
                    "effective overall. "
                    "Distinguish carefully between scores 3 and 4. "
                    "A score of 4 is possible when a response is "
                    "effective, relevant, adequately developed, and "
                    "clear overall, even if it contains several "
                    "genuine language errors. "
                    "Do not require sophisticated vocabulary or "
                    "complex grammar unless the task and response "
                    "genuinely require them. "
                    "The Better Version must be an edited version "
                    "of the student's original response, not a "
                    "rewritten model answer. "
                    "Never add new arguments, examples, facts, "
                    "evidence, or information to the Better Version. "
                    "Preserve the student's ideas and voice. "
                    "Follow the required Markdown output format exactly."
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


                # -------------------------------------------------
                # FORMAT AI RESPONSE FOR DISPLAY
                # -------------------------------------------------

                formatted_evaluation = evaluation

                lines = formatted_evaluation.split(
                    "\n"
                )

                processed_lines = []


                for line in lines:

                    if line.startswith(
                        "## Estimated Score:"
                    ):

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


                    elif line.startswith(
                        "## Better Version"
                    ):

                        processed_lines.append(
                            "<h2>Better Version</h2>"
                        )


                    else:

                        processed_lines.append(
                            line
                        )


                formatted_evaluation = "\n".join(
                    processed_lines
                )


                # -------------------------------------------------
                # FORMAT BOLD TEXT
                # -------------------------------------------------

                formatted_evaluation = re.sub(

                    r"\*\*(.*?)\*\*",

                    r"<strong>\1</strong>",

                    formatted_evaluation

                )


                # -------------------------------------------------
                # FORMAT BULLET POINTS
                # -------------------------------------------------

                formatted_evaluation = re.sub(

                    r"(?m)^\s*-\s+(.*)$",

                    r"<li>\1</li>",

                    formatted_evaluation

                )


                # -------------------------------------------------
                # WRAP CONSECUTIVE LIST ITEMS
                # -------------------------------------------------

                formatted_evaluation = re.sub(

                    r"((?:<li>.*?</li>\s*)+)",

                    r"<ul>\1</ul>",

                    formatted_evaluation

                )


                # -------------------------------------------------
                # REDUCE EXCESSIVE VERTICAL SPACING
                # -------------------------------------------------

                formatted_evaluation = formatted_evaluation.replace(

                    "\n\n",

                    "<br>"

                )


                formatted_evaluation = formatted_evaluation.replace(

                    "\n",

                    "<br>"

                )


                # -------------------------------------------------
                # REMOVE BREAKS AROUND HEADINGS
                # -------------------------------------------------

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


                # -------------------------------------------------
                # REMOVE BREAKS AROUND LISTS
                # -------------------------------------------------

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


                # -------------------------------------------------
                # DISPLAY FEEDBACK
                # -------------------------------------------------

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
