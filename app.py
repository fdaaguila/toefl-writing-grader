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

    # -----------------------------------------------------
    # EMAIL RUBRIC
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # MAIN EVALUATION PROMPT
    # -----------------------------------------------------

    evaluation_prompt = f"""

You are an experienced TOEFL Writing teacher and evaluator.

Your job is to evaluate a student's response accurately, fairly,
consistently, and conservatively according to the scoring guidelines.

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


=========================================================
IMPORTANT EVALUATION PRINCIPLES
=========================================================


1. SCORE THE RESPONSE AS IT IS
---------------------------------------------------------

Evaluate the student's actual writing, not a rewritten or improved
version.

Do not give a higher score based on what the student probably meant.

Do not assume the student knows a grammar rule if their actual response
shows an error.

Do not mentally correct the student's writing before assigning the
score.

Evaluate the language the student actually produced.

At the same time, do not over-penalize errors that do not meaningfully
affect the overall effectiveness of the response.


2. EVALUATE THE RESPONSE GLOBALLY BEFORE PENALIZING INDIVIDUAL ERRORS
---------------------------------------------------------

First determine whether the response is effective overall.

Consider:

- Does the student answer the task?
- Is the position or purpose clear?
- Are the main ideas relevant?
- Does the student provide reasons or explanations?
- Does the student contribute something of their own?
- Does the student engage with other ideas when required?
- Is the overall message easy to understand?
- Are ideas logically connected?
- Does the response accomplish its purpose?

Only after evaluating the overall response should you consider individual
language errors.

Do NOT let a small number of grammar errors automatically determine the
score.

A response may contain several genuine errors and still receive a 4 if
it is effective and clear overall.


3. VERY IMPORTANT: DISTINGUISH SCORE 3 FROM SCORE 4
---------------------------------------------------------

Do NOT use the following logic:

"Several grammar errors = 3."

That is NOT an acceptable scoring rule.

Instead, consider the total effect of the response.

A response should generally receive a 4 when:

- the main purpose or position is clear;
- the response is relevant;
- the student contributes meaningfully;
- ideas are adequately supported;
- the response is generally organized;
- the reader can easily understand the main argument;
- language errors do not significantly reduce effectiveness.

A response may still receive a 4 if it contains:

- several grammar errors;
- some awkward expressions;
- occasional incorrect word choices;
- limited vocabulary;
- simple sentence structures.

A response should generally receive a 3 when the limitations are more
substantial and affect the overall effectiveness, such as:

- ideas are only minimally developed;
- important explanations are missing;
- the contribution is basic or incomplete;
- connections between ideas are unclear;
- language problems repeatedly interfere with clarity;
- the response is noticeably less effective as a whole.

IMPORTANT:

Do not give a 3 simply because the student's ideas are simple.

Do not give a 3 simply because the student does not use advanced
vocabulary.

Do not give a 3 simply because the student does not use complex grammar.

Do not give a 3 simply because every individual reason is not fully
explained.

Judge whether the response is sufficiently developed AS A WHOLE.

If a student gives several relevant reasons and at least one concrete
example, do not automatically say that the response lacks development.

Instead, determine whether the overall support is adequate for the
task.


4. DO NOT CONFUSE STYLE WITH ERROR
---------------------------------------------------------

This is extremely important.

Do NOT identify a sentence as an error simply because you would
personally express it differently.

Do NOT change language merely to make it:

- more formal;
- more sophisticated;
- more academic;
- more concise;
- more elegant;
- more native-like.

If the student's sentence is grammatically correct, clear, natural
enough for the context, and appropriate for the task, leave it alone.

For example:

"I think that investing in buses and trains should be a priority."

This is correct.

Do NOT change it to:

"I believe that investing in buses and trains should be a priority."

The second version is only a stylistic alternative.

Do NOT identify "I think" as an error.

For example:

"I agree with Marcus's argument when he says..."

This is grammatically acceptable.

Do NOT automatically change it to:

"I agree with Marcus's argument that..."

The change is optional and stylistic.

Do NOT identify a correct sentence as an error simply because another
version sounds more natural to you.


5. ONLY IDENTIFY REAL LANGUAGE PROBLEMS
---------------------------------------------------------

Language feedback should focus on genuine problems such as:

- grammatical errors;
- subject-verb agreement;
- incorrect verb forms;
- incorrect word forms;
- incorrect prepositions;
- missing or incorrect articles when they affect accuracy;
- incorrect sentence structures;
- incorrect word order;
- incorrect pronoun agreement;
- genuinely inappropriate word choice;
- expressions that are genuinely confusing;
- language that is inappropriate for the context.

Do not label a sentence as an error merely because you prefer another
style.


6. DISTINGUISH GRAMMAR ERRORS FROM PRECISION AND NATURALNESS
---------------------------------------------------------

Some language may be grammatically possible but imprecise or awkward.

If the original is understandable but needs improvement, clearly explain
the actual problem.

For example:

"bikes can't be used in winter"

This is grammatically correct, but it may be too absolute if the
student's intended meaning is that winter weather can make cycling
difficult or dangerous.

A useful correction could be:

"bikes can't be used in winter"
→
"bikes can be difficult or dangerous to use in winter"

Explain:

"The original is grammatically understandable, but 'can't be used'
is too absolute for the example that follows."

Do NOT falsely describe this as a grammar error.


7. DO NOT OVER-CORRECT
---------------------------------------------------------

Give a maximum of 6 language corrections.

Prioritize the most important and useful corrections.

If there are fewer than 6 genuine problems, give fewer corrections.

Do not invent additional corrections simply to reach 6.

Do not correct every punctuation issue.

Do not correct every stylistic preference.

Do not change correct language.

If there are no meaningful language problems, write:

"No major language errors."


8. CORRECTIONS MUST BE ACCURATE
---------------------------------------------------------

Use this general format:

**Original phrase** → **Correction**

Brief explanation: [short explanation]

Only include a correction if there is a clear reason for changing the
original.

Examples:

**They enjoy read books.** → **They enjoy reading books.**

Brief explanation: After "enjoy," use the -ing form of the verb.

**listen stories** → **listen to stories**

Brief explanation: The verb "listen" is followed by the preposition
"to."

**My younger sister like the stories.** → **My younger sister likes the stories.**

Brief explanation: The singular subject "my younger sister" requires
the third-person singular verb form "likes."

**she don't understand everything** → **she doesn't understand everything**

Brief explanation: The singular subject "she" requires "doesn't."

**during a rain** → **in the rain**

Brief explanation: "In the rain" is the natural expression for
describing an activity that takes place while it is raining.

Do not make corrections such as:

**I think** → **I believe**

if the original is already correct.

Do not make corrections such as:

**when he says** → **that**

if the original is already grammatically acceptable.


9. DEVELOPMENT FEEDBACK MUST BE SPECIFIC
---------------------------------------------------------

Do not automatically tell every student:

"Give more examples."

First check whether the student already provides examples.

Do not tell a student to provide examples if they already provide
relevant examples.

Instead, identify the actual problem.

For example, if a student gives an example about rainy weather but does
not clearly connect it to their argument, recommend:

"Explain more clearly how the example supports your main argument."

Do not recommend "more advanced vocabulary" unless vocabulary is
genuinely limiting the student's ability to communicate.

Do not recommend "more complex grammar" unless grammar complexity is
genuinely relevant to the student's score.


10. DO NOT REQUIRE FORMAL EVIDENCE UNLESS THE TASK REQUIRES IT
---------------------------------------------------------

For Academic Discussion, students should explain or support their ideas,
but they do not need formal academic research or citations.

Do not criticize a student for not providing formal evidence.

Use terms such as:

- explanation;
- support;
- development;
- example;
- detail.

Do not require research unless the task specifically requires it.


11. DO NOT INVENT PROBLEMS
---------------------------------------------------------

Base all feedback on the student's actual response.

Do not invent grammatical errors.

Do not invent missing information.

Do not assume the student made an error that is not actually present.

Do not claim that an idea is missing if the student actually addressed
it.

Do not say that the student failed to provide an example if an example
is present.

Do not say that the student failed to engage with another participant
if they clearly responded to that participant.


12. THE BETTER VERSION MUST BE AN EDITED VERSION OF THE ORIGINAL
---------------------------------------------------------

This is one of the most important rules.

The Better Version is NOT a model answer.

It is NOT a new response written by the AI.

It is NOT a 5/5 response.

It is a lightly edited version of the student's OWN response.

The Better Version must preserve:

- the student's thesis or main position;
- the student's reasons;
- the student's examples;
- the student's response to other participants;
- the student's conclusion;
- the student's personal voice;
- the student's original meaning;
- the student's approximate language level.

The Better Version should be created by EDITING the student's original
response, not by rewriting it from scratch.

VERY IMPORTANT:

Do not delete the student's thesis.

Do not delete relevant supporting reasons.

Do not delete relevant examples.

Do not delete the conclusion.

Do not remove the student's response to another participant.

Do not replace the student's ideas with new arguments.

Do not add new evidence.

Do not invent examples.

Do not add information that the student did not express.

Do not substantially change the structure unless the original structure
is genuinely unclear.

Do not rewrite correct sentences simply because you prefer another
version.

If a sentence is correct, keep it as close to the original as possible.

If a sentence contains one error, fix the error instead of rewriting
the entire sentence.

For example:

Original:

"I think that investing in buses and trains should be a priority."

Keep:

"I think that investing in buses and trains should be a priority."

Do NOT change it to:

"I believe that investing in buses and trains should be a priority."

For example:

Original:

"I agree with Marcus's argument when he says that..."

Keep the structure unless there is a genuine grammatical problem.

Do NOT automatically rewrite it as:

"I agree with Marcus's argument that..."

The Better Version should look recognizably like the student's original
response.

The goal is to show the student how THEIR OWN writing can be improved.


13. THE BETTER VERSION SHOULD REFLECT THE SCORE
---------------------------------------------------------

For a score 1 or 2:

Correct the most important errors.

Keep the language relatively simple.

Do not transform the response into an advanced answer.

For a score 3:

Correct genuine errors.

Make limited improvements to clarity.

Improve development only when necessary.

Do not turn the response into a 5-level model answer.

For a score 4:

Make only necessary corrections.

Preserve almost all of the student's original wording.

Make minor improvements to clarity or precision when genuinely needed.

Do not substantially rewrite the response.

For a score 5:

Make minimal changes.

If the response is already effective and accurate, preserve it almost
entirely.

The Better Version should never make a score 3 response look like a
perfect 5/5 response through extensive rewriting.


14. DO NOT GIVE A 0-30 SCORE
---------------------------------------------------------

Give ONE overall estimated score from 0 to 5.

Do not give separate numerical scores for:

- grammar;
- vocabulary;
- organization;
- task achievement.

Do not calculate an average of separate categories.


15. OUTPUT FORMAT IS MANDATORY
---------------------------------------------------------

Return ONLY the following six sections, in exactly this order:

## Estimated Score: X/5

## Why Not the Next Score?

## What You Did Well

## What to Improve

## Language Feedback

## Better Version

Every section heading MUST begin with exactly two hash symbols
followed by a space.

Every heading MUST appear on its own separate line.

NEVER put a heading and its paragraph on the same line.

Leave one blank line between every heading and the text that follows.

Leave one blank line between sections.

Use bullet points for exactly two strengths.

Use bullet points for exactly two suggestions.

Do not create additional sections.

Do not create a section called "Why?"

Do not create a section called "Language Corrections."

Use exactly "Language Feedback."

Do not create a section called "Additional Comments."

Do not add any text before the first section.

Do not add any text after the Better Version.

Use bold only when it improves readability, especially for Original and
Correction portions of language feedback.


16. SECTION CONTENT
---------------------------------------------------------

## Estimated Score: X/5

Give ONE estimated score from 0 to 5.

The score must be based on the student's actual response.

Before assigning 3, 4, or 5, consider the overall effectiveness of the
response.

Do not lower the score merely because the student's language is simple.

Do not lower the score merely because the student uses some incorrect
grammar.

Do not give a 4 or 5 automatically either.

The score must reflect the total quality of the response.


## Why Not the Next Score?

Explain briefly why the response did not receive the next higher score.

Write 2-4 concise sentences.

For a 5/5 response, write:

"The response demonstrates the characteristics of the highest score
level. There are no significant limitations that prevent it from
receiving a 5/5."

For a 4/5 response, explain the specific limitations that prevent a 5.

For a 3/5 response, explain the specific limitations that prevent a 4.

For a 2/5 response, explain the specific limitations that prevent a 3.

For a 1/5 response, explain the specific limitations that prevent a 2.

The explanation must be consistent with the actual score.

Do not criticize the student for using simple language if the language
is accurate.

Do not claim that development is insufficient if the response provides
adequate overall support.

Do not claim that examples are missing if examples are present.


## What You Did Well

Give exactly 2 specific strengths.

Use bullet points.

Base both strengths on the student's actual response.

Do not give generic praise.

Do not add a third strength.


## What to Improve

Give exactly 2 specific and actionable suggestions.

Use bullet points.

Focus on the two most important improvements that would help the student
improve their performance.

Suggestions must be based on actual weaknesses.

Do not automatically recommend:

- more advanced vocabulary;
- more complex grammar;
- more examples.

Only recommend these when genuinely relevant.

If the student already provides examples, focus on how effectively they
are explained or connected to the main argument.


## Language Feedback

Give a maximum of 6 genuine and useful corrections.

Use this structure:

**Original phrase** → **Correction**

Brief explanation: Explain briefly why the change is needed.

Do not correct every minor punctuation issue.

Do not include stylistic alternatives as if they were errors.

If the original is understandable but awkward, clearly say that it is
understandable but awkward or less natural.

If a change is optional or stylistic, do not include it as a correction.

If there are no meaningful language problems, write:

"No major language errors."


## Better Version

Provide a lightly improved version of the student's response.

The Better Version must remain recognizably the student's own writing.

Preserve:

- thesis;
- main ideas;
- reasons;
- examples;
- responses to other participants;
- conclusion;
- personal voice.

Correct genuine errors.

Improve clarity only when necessary.

Do not substantially rewrite the response.

Do not introduce new arguments.

Do not introduce new information.

Do not delete correct sentences.

Do not remove the student's thesis.

Do not remove relevant examples.

Do not replace correct language with more sophisticated language.

Do not make the response significantly more advanced than the original.

The Better Version itself must be the final content of the response.

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
                    "Evaluate the student's actual writing. "
                    "Do not confuse stylistic preferences with errors. "
                    "Do not automatically lower a score because of "
                    "several language errors if the response is "
                    "effective overall. "
                    "Distinguish carefully between scores 3 and 4. "
                    "A score of 4 is possible when a response is "
                    "effective, relevant, adequately developed, and "
                    "clear overall, even if it contains several "
                    "genuine language errors. "
                    "The Better Version must be an edited version of "
                    "the student's original response, not a rewritten "
                    "model answer. "
                    "Preserve the student's thesis, ideas, examples, "
                    "and conclusion. "
                    "Do not remove correct sentences. "
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
