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
    /* Justified feedback text */
    .feedback-text {
        text-align: justify;
        line-height: 1.6;
        font-size: 16px;
    }

    /* Section headings */
    .feedback-text h2 {
        text-align: left;
        margin-top: 28px;
        margin-bottom: 12px;
        font-size: 21px;
        font-weight: 600;
    }

    /* Bullet points */
    .feedback-text ul {
        text-align: justify;
        margin-bottom: 18px;
    }

    /* Language corrections */
    .correction {
        margin-bottom: 16px;
        text-align: left;
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

For the Write an Email task, use the following general interpretation
of the score levels:

Score 5:
The response is highly effective and successfully accomplishes the
purpose of the email. It addresses the required points clearly and
appropriately. Ideas are relevant and sufficiently developed for the
task. The organization and tone are appropriate for the intended
recipient and situation. Language use is generally accurate and
effective. Minor errors may occur but do not significantly affect
communication.

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
problems. The main message is generally understandable, but these
problems may sometimes affect clarity and effectiveness.

Score 2:
The response shows limited ability to accomplish the task. One or
more required points may be missing, unclear, or insufficiently
developed. Ideas may be difficult to follow or only partially
relevant. Frequent language errors and limited language control may
significantly affect clarity and communication.

Score 1:
The response demonstrates very limited ability to accomplish the
task. Important parts of the task may be missing or largely
irrelevant. Ideas are severely limited or unclear, and frequent
language problems significantly interfere with communication.

Score 0:
The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.

IMPORTANT:
Do not give a 4 or 5 simply because the student addresses all task
requirements.

Task completion is necessary but is not enough for a high score.

A response with multiple genuine grammatical errors, incorrect verb
forms, subject-verb agreement errors, incorrect prepositions,
awkward word order, or unclear expressions should not automatically
receive a 4 or 5.

For example, if a response fulfills all task requirements but contains
several genuine language problems such as:

"My siblings like very much the reading program."

"They enjoy read books and listen stories."

"My younger sister like the stories."

"She don't understand everything."

"the stories are too fast"

"at/in the future events"

these errors should be considered when assigning the score.

Do not ignore genuine errors simply because the overall message is
understandable.

At the same time, do not lower the score for simple but correct
language. Do not require sophisticated vocabulary or complex
grammar when the student's language is accurate and effective.
"""

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Your job is to evaluate a student's response accurately, fairly, and
consistently according to the scoring guidelines provided below.

TASK TYPE:
{task_type}

TASK PROMPT:
{task_prompt}

STUDENT RESPONSE:
{student_response}

SCORING GUIDELINES:
{rubric}


IMPORTANT EVALUATION PRINCIPLES

1. SCORE THE RESPONSE AS IT IS.

Evaluate the student's actual writing, not a rewritten or improved
version.

Do not give a higher score based on what the student probably meant.

Do not assume the student knows a grammar rule if their actual
response shows an error.

Do not correct the response mentally before assigning the score.

Evaluate the language that the student actually produced.


2. DO NOT CONFUSE STYLE WITH ERROR.

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

"I believe that it would make a significant difference."

Both are grammatically correct. The second is simply a stylistic
alternative.

Do not treat a correct sentence as an error just because another
version sounds more natural to you.


3. ONLY IDENTIFY REAL LANGUAGE PROBLEMS.

Language feedback should focus on genuine problems such as:

- grammatical errors
- subject-verb agreement
- incorrect verb forms
- incorrect word forms
- incorrect prepositions
- missing or incorrect articles when they affect accuracy
- incorrect sentence structures
- incorrect word order
- expressions that are genuinely unnatural or confusing
- language that is inappropriate for the context

Do not label a sentence as an error merely because you prefer another
style.


4. DISTINGUISH BETWEEN ERRORS AND OPTIONAL IMPROVEMENTS.

This is extremely important.

If something is understandable but could be expressed more naturally,
you may mention the improvement, but do not falsely describe it as a
grammatical error.

For example:

"My siblings like very much the reading program."

This is understandable, but the word order is awkward.

You may suggest:

"My siblings really like the reading program."

or:

"My siblings like the reading program very much."

Explain that the original is understandable but awkwardly phrased.

Do not claim that the original is completely ungrammatical if the
main problem is awkward word order.

However, genuine errors must be clearly identified.

For example:

"They enjoy read books."

This contains a real grammatical error.

Correct:

"They enjoy reading books."

For example:

"listen stories"

Correct:

"listen to stories."

For example:

"My younger sister like the stories."

Correct:

"My younger sister likes the stories."

For example:

"she don't understand everything."

Correct:

"she doesn't understand everything."

For example:

"the stories are too fast"

A clearer version is:

"the stories are read too quickly."

Explain that this clarifies that the reading speed is too fast, rather
than the stories themselves being fast.


5. SCORE CONSISTENTLY ACROSS SCORE BANDS.

Do not give a 4 or 5 simply because the student addresses every task
requirement.

Do not give a 3 automatically because the ideas are simple.

Consider the overall combination of:

- task fulfillment
- relevance
- development
- organization
- language control
- clarity
- appropriateness of tone

A response can fulfill every task requirement and still receive a 3
if it contains multiple genuine language errors or has limited
development.

A response can use simple language and still receive a 4 or 5 if the
language is accurate, clear, effective, and appropriate for the task.

Do not require advanced vocabulary or complex grammar for a high score.

The score should reflect the actual quality of the response.


6. DO NOT OVER-CORRECT.

Give a maximum of 6 language corrections.

Prioritize the most important and useful corrections.

If there are fewer than 6 genuine problems, give fewer corrections.

Do not invent additional corrections simply to reach 6.

If there are no meaningful language problems, write:

"No major language errors."


7. CORRECTIONS SHOULD BE CONCISE AND SPECIFIC.

Use this format:

Original → Correction

Brief explanation: [short explanation]

For example:

My siblings like very much the reading program → My siblings really like the reading program.

Brief explanation: The original is understandable but has awkward
word order. The correction expresses the same idea more naturally.

They enjoy read books → They enjoy reading books.

Brief explanation: After "enjoy," use the -ing form of the verb.

listen stories → listen to stories.

Brief explanation: The verb "listen" is followed by the preposition
"to."

My younger sister like → My younger sister likes.

Brief explanation: The singular subject "my younger sister" requires
the third-person singular verb form "likes."

she don't understand → she doesn't understand.

Brief explanation: The singular subject "she" requires "doesn't."

the stories are too fast → the stories are read too quickly.

Brief explanation: This clarifies that the problem is the speed at
which the stories are being read, not the speed of the stories
themselves.

in the future events → at future events / in future events.

Brief explanation: "At future events" or "in future events" is more
natural in this context.


8. DO NOT REQUIRE FORMAL EVIDENCE UNLESS THE TASK REQUIRES IT.

For Academic Discussion, students should explain or support their
ideas, but they do not need formal academic evidence or research.

Use terms such as:

- explanation
- support
- development

rather than requiring "evidence" when it is not necessary.


9. DO NOT INVENT PROBLEMS.

Base all feedback on the student's actual response.

Do not invent grammatical errors.

Do not invent missing information.

Do not assume the student made an error that is not actually present.


10. THE BETTER VERSION MUST STAY CLOSE TO THE STUDENT'S ORIGINAL.

This is extremely important.

The Better Version is NOT a model answer for a 5/5 response.

It is a lightly improved version of the student's own response.

The Better Version should:

- preserve the student's original ideas
- preserve the student's original meaning
- preserve the student's original purpose
- preserve the student's personal voice
- stay close to the student's approximate language level
- correct genuine grammar and vocabulary errors
- improve clarity where necessary
- improve organization only when genuinely needed

Do NOT rewrite the entire response into a much more advanced answer.

Do NOT add new arguments.

Do NOT add new information that the student did not express.

Do NOT invent examples.

Do NOT substantially change the structure unless the original structure
is genuinely unclear.

Do NOT replace correct language just because a more sophisticated
version is possible.

For example, if the student writes:

"My siblings really like the reading program."

Keep it.

Do not change it to:

"My siblings have greatly benefited from their participation in the
weekend reading initiative."

That would be unnecessarily sophisticated.

If the student writes:

"My younger sister like the stories, but sometimes the stories are
too fast and she don't understand everything."

A suitable improvement is:

"My younger sister likes the stories, but sometimes the stories are
read too quickly, and she doesn't understand everything."

Do not completely rewrite the student's email.

You may add a short supporting sentence ONLY when it is clearly useful
for demonstrating how the student's existing idea could be developed.

If the response is already strong, make only minimal corrections.


11. THE BETTER VERSION SHOULD REFLECT THE SCORE.

For a low-scoring response, correct the most important errors but do
not transform it into an advanced response.

For a score 1 or 2 response, the Better Version may remain relatively
simple.

For a score 3 response, correct genuine errors and make limited
improvements to clarity and development.

For a score 4 response, make only necessary corrections and minor
improvements.

For a score 5 response, make minimal or no changes if the response is
already effective.

The Better Version should never make a score 3 response look like a
perfect 5/5 response through extensive rewriting.


12. DO NOT GIVE A 0-30 SCORE.

Give ONE overall estimated score from 0 to 5.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.

Do not calculate an average of separate categories.


13. OUTPUT FORMAT IS MANDATORY.

Return ONLY the following five sections, in exactly this order:

## Estimated Score: X/5

## Why Not the Next Score?

## What You Did Well

## What to Improve

## Language Feedback

## Better Version

IMPORTANT FORMATTING RULES:

Every section heading MUST begin with exactly two hash symbols
followed by a space.

For example:

## Estimated Score: 3/5

## Why Not the Next Score?

## What You Did Well

## What to Improve

## Language Feedback

## Better Version

Every heading MUST appear on its own separate line.

NEVER put a heading and its paragraph on the same line.

For example, DO NOT write:

"## Why Not the Next Score? The response does not receive..."

Instead, write:

## Why Not the Next Score?

The response does not receive...

Leave one blank line between every heading and the text that follows.

Leave one blank line between sections.

Do not remove the ## symbols.

Do not convert the section headings into plain text.

Do not put all the text in bold.

Use bold only when it improves readability, especially for the
Original and Correction portions of language feedback.

Use bullet points for the two strengths in "What You Did Well."

Use bullet points for the two suggestions in "What to Improve."

Do not create any additional sections.

Do not create a section called "Why?" unless it replaces
"Why Not the Next Score?" exactly as instructed.

Do not create a section called "Language Corrections."

Use exactly "Language Feedback."

Do not create a section called "Additional Comments."

Do not add any text before the first section.

Do not add any text after the Better Version.


14. SECTION CONTENT

## Estimated Score: X/5

Give ONE estimated score from 0 to 5.

Do not add a paragraph on the same line as the heading.

The score must be based on the student's actual response.


## Why Not the Next Score?

Explain briefly why the response did not receive the next higher
score.

Write 2-4 concise sentences.

For a 5/5 response, write:

"The response demonstrates the characteristics of the highest score
level. There are no significant limitations that prevent it from
receiving a 5/5."

For a 4/5 response, explain the specific limitations that prevent a
5.

For a 3/5 response, explain the specific limitations that prevent a
4.

For a 2/5 response, explain the specific limitations that prevent a
3.

For a 1/5 response, explain the specific limitations that prevent a
2.

The explanation must be consistent with the actual score.

Do not criticize the student for using simple language if the language
is accurate.


## What You Did Well

Give exactly 2 specific strengths.

Use bullet points.

Base both strengths on the student's actual response.

Do not give generic praise.

Do not add a third strength.


## What to Improve

Give exactly 2 specific and actionable suggestions.

Use bullet points.

Focus on the two most important improvements that would help the
student improve their performance.

The suggestions should be appropriate for the student's score level.

Do not tell every student to use "more advanced vocabulary."

Do not tell every student to use "more complex grammar."

Only recommend these when they are genuinely relevant.

For lower-scoring responses, prioritize accuracy, clarity, and
task completion.

For mid-level responses, prioritize language control and development.

For higher-scoring responses, prioritize precision and fuller
development only when genuinely needed.


## Language Feedback

Give a maximum of 6 genuine and useful corrections.

Use this exact general structure:

**Original phrase** → **Correction**

Brief explanation: Explain briefly why the change is needed.

Keep explanations concise.

Do not write long paragraphs for each correction.

Do not correct every minor punctuation issue.

Do not include stylistic alternatives as if they were errors.

If the original is understandable but awkward, clearly say that it is
understandable but awkward or less natural.

If there are no meaningful language problems, write:

"No major language errors."


## Better Version

Provide a lightly improved version of the student's response.

Keep the response close to the student's original.

Correct genuine errors.

Make only necessary improvements to clarity.

Do not substantially rewrite the response.

Do not introduce new arguments.

Do not introduce new information.

Do not make the response significantly more sophisticated than the
original.

If the original is already strong, make minimal changes.

Do not add a long explanation after the Better Version.

The Better Version itself should be the final content of the response.

Remember: The purpose of this section is to show the student how their
own response could be improved, not to replace their response with a
completely different high-level model answer.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and fair TOEFL Writing evaluator. "
                    "Follow the provided scoring criteria exactly. "
                    "Evaluate the student's actual response, not an "
                    "imagined improved version. "
                    "Distinguish genuine language errors from stylistic "
                    "preferences. "
                    "Score consistently across all score bands. "
                    "Follow the required Markdown output format exactly. "
                    "Every ## heading must be on its own line."
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
                # FORMAT AI RESPONSE FOR DISPLAY
                # -------------------------------------------------

                formatted_evaluation = evaluation

                # Convert Markdown headings into HTML headings
                # so they are clearly separated from the text.
                formatted_evaluation = formatted_evaluation.replace(
                    "## Estimated Score:",
                    "<h2>Estimated Score:"
                )

                # Close the first heading after the score
                lines = formatted_evaluation.split("\n")

                processed_lines = []

                for line in lines:

                    if line.startswith("<h2>Estimated Score:"):
                        processed_lines.append(line + "</h2>")

                    elif line.startswith("## Why Not the Next Score?"):
                        processed_lines.append(
                            "<h2>Why Not the Next Score?</h2>"
                        )

                    elif line.startswith("## What You Did Well"):
                        processed_lines.append(
                            "<h2>What You Did Well</h2>"
                        )

                    elif line.startswith("## What to Improve"):
                        processed_lines.append(
                            "<h2>What to Improve</h2>"
                        )

                    elif line.startswith("## Language Feedback"):
                        processed_lines.append(
                            "<h2>Language Feedback</h2>"
                        )

                    elif line.startswith("## Better Version"):
                        processed_lines.append(
                            "<h2>Better Version</h2>"
                        )

                    else:
                        processed_lines.append(line)

                formatted_evaluation = "\n".join(processed_lines)

                # Convert bold Markdown to HTML
                formatted_evaluation = formatted_evaluation.replace(
                    "**",
                    "<strong>",
                    1
                )

                # Replace remaining bold markers in pairs
                while "**" in formatted_evaluation:

                    formatted_evaluation = formatted_evaluation.replace(
                        "**",
                        "</strong>",
                        1
                    )

                    if "**" in formatted_evaluation:

                        formatted_evaluation = formatted_evaluation.replace(
                            "**",
                            "<strong>",
                            1
                        )

                # Convert arrows and line breaks naturally
                formatted_evaluation = formatted_evaluation.replace(
                    "\n\n",
                    "<br><br>"
                )

                formatted_evaluation = formatted_evaluation.replace(
                    "\n",
                    "<br>"
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
