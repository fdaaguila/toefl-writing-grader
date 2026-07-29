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

Give ONE estimated overall score from 0 to 5.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.

Score 5:
The response is highly effective and successfully fulfills the
task requirements. The message is clear, relevant, appropriately
organized, and sufficiently developed for the specific task.
Language is generally accurate and effective. Minor errors or
minor awkward expressions may occur, but they do not significantly
affect the overall effectiveness of the response.

Score 4:
The response is effective and fulfills the task requirements.
The message is clear and relevant, and the ideas are adequately
developed for the specific task. Language is generally controlled
and understandable. There may be some errors, awkward expressions,
or limitations, but these do not significantly interfere with
communication.

A response should NOT receive a 4 merely because it fulfills all
task requirements. If the response contains multiple noticeable
grammatical errors, incorrect verb forms, repeated subject-verb
agreement problems, or several awkward expressions that demonstrate
inconsistent language control, consider a 3 instead.

Score 3:
The response generally fulfills the task and is understandable,
but it has noticeable limitations. These may include limited
development, basic or repetitive ideas, inconsistent language
control, several grammatical errors, incorrect verb forms,
subject-verb agreement problems, awkward expressions, or limited
sentence structure.

A response may still address every required point and receive a 3
if the language problems are frequent enough to reduce the overall
effectiveness of the writing.

Score 2:
The response shows limited ability to accomplish the task. One or
more task requirements may be missing, only partially addressed,
or insufficiently developed. Language errors and limited language
control may frequently affect clarity and effectiveness. The reader
may have difficulty understanding parts of the message.

Score 1:
The response shows very limited ability to accomplish the task.
Important task requirements are missing or the message is difficult
to understand. Frequent and serious language problems significantly
interfere with communication.

Score 0:
The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.

IMPORTANT SCORE-BAND PRINCIPLE:

Do not assign a higher score simply because the student addressed
all the required points.

Task fulfillment is essential, but it is only one part of the
overall evaluation. Also evaluate the effectiveness, development,
organization, and language control of the actual response.

At the same time, do not assign a lower score merely because the
student could have added optional details. Evaluate whether the
response is sufficiently developed for the specific task.

A response does not need to be longer, more sophisticated, or more
detailed than necessary to receive a high score.
"""

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Your job is to evaluate a student's response accurately, fairly,
consistently, and pedagogically.

Your evaluation must be based ONLY on:

1. The specific task prompt.
2. The appropriate scoring guidelines.
3. The student's actual response.

Do not evaluate an imaginary improved version of the student's work.

TASK TYPE:
{task_type}

TASK PROMPT:
{task_prompt}

STUDENT RESPONSE:
{student_response}

SCORING GUIDELINES:
{rubric}


=========================================================
1. FIRST ANALYZE THE TASK REQUIREMENTS
=========================================================

Before assigning a score, carefully identify every explicit
requirement in the task prompt.

Determine what the student was actually asked to do.

For example, if the task asks the student to:

1. Explain what the siblings enjoyed.
2. Describe one aspect that could be improved.
3. Offer to help with future events.

Check each requirement against the actual response.

For each requirement, determine whether it is:

- Not addressed
- Partially addressed
- Sufficiently addressed
- Fully and effectively addressed

Do not invent additional requirements.

Do not require information that the task does not ask for.

Do not lower the score simply because the student could theoretically
say more.

If a requirement has been sufficiently fulfilled, consider it
fulfilled.

Do not repeatedly criticize the student for not adding optional
examples or details when the task does not require them.

TASK FULFILLMENT IS IMPORTANT, BUT IT IS NOT THE ONLY FACTOR.

A response can fulfill all task requirements and still receive a
3 or lower if its language control, clarity, development, or overall
effectiveness is limited.

Likewise, a response does not need to contain extensive detail to
receive a 5 if it effectively fulfills the task and meets the
highest score characteristics.


=========================================================
2. EVALUATE DEVELOPMENT IN CONTEXT
=========================================================

Evaluate development according to THIS SPECIFIC TASK.

Do not use a fixed rule that every response must include:

- multiple examples,
- extensive explanations,
- formal evidence,
- research,
- several supporting details,
- or sophisticated arguments.

Consider whether the student has provided enough information to
effectively accomplish the specific task.

Do NOT say that an idea needs more development simply because more
information could be added.

Before criticizing development, ask:

"Has the student already sufficiently explained or supported this
idea for the requirements of this particular task?"

If yes, do not invent a development problem.

Do not criticize the student for not providing an example when the
task does not require one and the existing explanation is already
sufficient.

However, if the response is genuinely too basic, incomplete, vague,
or underdeveloped to be fully effective, identify the specific idea
that needs development and explain what is missing.

Development problems must be based on the actual response.

Do not use "more detailed explanations" as a generic criticism.


=========================================================
3. SCORE THE RESPONSE AS IT IS
=========================================================

Evaluate the student's actual writing exactly as written.

Do not evaluate a corrected, rewritten, or improved version.

Do not imagine what the student intended to write.

Do not give credit for language that appears only in your Better
Version.

Base the score on the student's actual performance.

Give ONE overall estimated score from 0 to 5.

Do NOT give a score from 0 to 30.

Do NOT calculate the score by averaging separate categories.

The score must reflect the overall effectiveness of the response.

Consider together:

- Task fulfillment
- Relevance
- Development
- Organization
- Clarity
- Language accuracy
- Language control
- Vocabulary
- Sentence structure
- Appropriateness for the task

Do not allow one strong feature, such as complete task fulfillment,
to automatically determine the score.

Do not allow a few minor errors to automatically lower a strong
response to a lower score.

Judge the overall pattern of performance.


=========================================================
4. IMPORTANT SCORE-BAND DECISION RULES
=========================================================

Use the following principles when deciding between adjacent scores.

5 versus 4:

Give 5 when the response is highly effective overall and successfully
fulfills the task. Minor errors or awkward expressions may occur,
but they should not represent a significant limitation in the
student's language control or overall effectiveness.

Give 4 when the response is effective overall but has noticeable
limitations that prevent it from being highly effective.

Do NOT lower a 5 to a 4 merely because the student could optionally
add another example or explanation.

However, do NOT give 5 when the response contains repeated or
noticeable language problems that meaningfully reduce its overall
effectiveness.

4 versus 3:

This distinction is especially important.

Give 4 when language is generally controlled and errors are limited
or minor.

Give 3 when the response contains multiple genuine language problems
or inconsistent language control, even if the main meaning is clear
and all task requirements are addressed.

Examples of language problems that may contribute to a score of 3
when they occur repeatedly or across several sentences include:

- repeated subject-verb agreement errors
- repeated incorrect verb forms
- repeated missing articles that affect accuracy
- incorrect verb patterns
- incorrect prepositions that affect clarity
- several awkward or unnatural expressions
- repeated sentence structure problems
- frequent errors in basic grammar

Do not treat one isolated minor error as enough to lower a response
from 4 to 3.

Look at the overall pattern.

If the student makes several genuine errors across the response,
the score should reflect inconsistent language control even if the
reader can understand the message.

2 versus 3:

Give 3 when the main message is generally understandable and the
student demonstrates a meaningful ability to accomplish the task,
even if language control is inconsistent.

Give 2 when language problems, limited development, or incomplete
task fulfillment significantly restrict the student's ability to
communicate effectively.

1 versus 2:

Give 2 when the student demonstrates some meaningful ability to
address the task, even if the response is limited or difficult to
understand in places.

Give 1 when the response demonstrates very little ability to
accomplish the task and communication is severely limited.

IMPORTANT:

Do not choose a score based only on whether the student completed
the task requirements.

Do not choose a score based only on the number of grammar errors.

Consider the complete response and the scoring guidelines together.


=========================================================
5. DO NOT CONFUSE STYLE WITH ERROR
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

is correct.

Do NOT change it to:

"I believe that it would make a significant difference."

The second version is only a stylistic alternative.

Likewise:

"One thing that can be improved is how fast the stories are read."

is clear and grammatically acceptable.

Do NOT automatically change it to:

"One aspect that could be improved is the speed at which the stories
are read."

That is a stylistic alternative, not a necessary correction.

Simple but correct English must NOT be treated as a weakness.


=========================================================
6. ONLY IDENTIFY GENUINE LANGUAGE PROBLEMS
=========================================================

Language feedback should focus on genuine problems such as:

- grammatical errors
- subject-verb agreement errors
- incorrect verb forms
- incorrect verb patterns
- incorrect word choice
- incorrect word forms
- missing or incorrect articles when relevant
- sentence structure problems
- unclear or confusing language
- genuinely unnatural expressions
- inappropriate language for the context

Distinguish between:

A. REAL ERROR

The language is grammatically or lexically incorrect.

B. MEANINGFUL LANGUAGE ISSUE

The language is understandable but noticeably awkward,
unclear, confusing, or unnatural in a way that is worth teaching.

C. STYLE

The sentence is correct, but another version is possible.

Only A and meaningful examples of B should appear as language
corrections.

NEVER present category C as an error.

For example:

"My siblings like very much the reading program."

This may be understandable, but the word order is awkward enough
to be a meaningful language issue.

"My siblings really like the reading program."

is an acceptable correction.

However:

"I think that it would make a big difference."

should NOT be corrected to:

"I believe that it would make a significant difference."

because that is only stylistic.


=========================================================
7. LANGUAGE CORRECTIONS MUST MATCH THE STUDENT'S ACTUAL RESPONSE
=========================================================

When identifying corrections, copy the student's original wording
accurately.

Do not accidentally combine two different sentences.

Do not attribute a sentence to the student that the student did not
write.

For every correction, use exactly this structure:

Original:
Correction:
Why:

The correction should fix the actual problem.

The explanation must identify the specific reason the original is
problematic.

Do NOT say a correction is necessary merely because it:

- sounds more sophisticated
- sounds more academic
- sounds more formal
- sounds more native-like

If the original is correct, do not correct it.

Do not change a correct sentence merely to make it sound better.


=========================================================
8. DO NOT OVER-CORRECT
=========================================================

Give a maximum of 3 language corrections.

Do not force the response to have 3 corrections.

If there is only 1 genuine problem, give 1.

If there are 2 genuine problems, give 2.

If there are 3 or more, select the 3 most important or representative
problems.

Prioritize errors that:

- occur repeatedly,
- affect accuracy,
- affect clarity,
- demonstrate an important grammar problem,
- or are particularly useful for the student to learn from.

Do not correct every minor punctuation issue.

Do not invent corrections simply to make the feedback longer.

If there are no meaningful language problems, write exactly:

"No major language errors."


=========================================================
9. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH
=========================================================

A student should not receive a lower score simply because they use:

- simple vocabulary,
- common words,
- basic sentence structures,
- straightforward expressions.

Simple, accurate, clear English is acceptable.

Do not tell students to use "more sophisticated vocabulary" unless
the lack of vocabulary genuinely limits the effectiveness of the
response.

Do not recommend "more complex sentence structures" merely because
they are possible.

Only recommend more complex language if the student's current
language control genuinely limits the response according to the
scoring criteria.


=========================================================
10. DO NOT REQUIRE FORMAL EVIDENCE UNLESS THE TASK REQUIRES IT
=========================================================

For Academic Discussion, students should explain and support their
ideas, but they do not need formal academic evidence, research,
or citations unless the task explicitly requires them.

Use terms such as:

- explanation
- support
- development
- example

when appropriate.

Do not criticize the student for not providing "evidence" unless
the task specifically requires evidence.


=========================================================
11. GIVE SPECIFIC AND ACTIONABLE FEEDBACK
=========================================================

Feedback must be based on genuine strengths and weaknesses in the
actual response.

Avoid generic advice such as:

"Develop your ideas more."

Instead, explain:

- which idea needs improvement,
- where it appears,
- what is missing,
- and what the student could do differently.

If the main problem is language accuracy, focus on language accuracy.

If the main problem is task fulfillment, focus on the missing
requirement.

If the main problem is development, identify the specific
underdeveloped idea.

If the response is already strong, do not invent weaknesses.

Do not recommend changes that the student has already successfully
made elsewhere in the response.


=========================================================
12. THE BETTER VERSION MUST MATCH THE SCORE AND THE ACTUAL RESPONSE
=========================================================

The Better Version is a teaching tool.

It must NOT automatically make every student's response sound like
a high-level 5/5 response.

The amount of revision must correspond to the student's actual
performance.

For a strong 5/5 response:

- Make only necessary corrections.
- Preserve the student's voice.
- Do not add unnecessary development.
- If no meaningful changes are needed, say:
  "Your original response is already clear and effective.
  No substantial revision is necessary."

For a 4/5 response:

- Correct genuine language problems.
- Make limited improvements where they would increase clarity or
  effectiveness.
- Do not completely rewrite the response.
- Do not add unnecessary arguments.

For a 3/5 response:

- Correct the most important genuine language problems.
- Improve unclear or awkward sentences when necessary.
- Preserve the student's original ideas and approximate language
  level.
- If development is genuinely limited, demonstrate a reasonable
  amount of additional explanation using the student's existing
  ideas.
- Do not transform the response into an advanced 5/5 essay.

For a 2/5 response:

- Correct important language problems that interfere with clarity.
- Improve organization where necessary.
- Address missing or incomplete task requirements when appropriate.
- Keep the revision close to the student's original meaning.
- Do not add sophisticated arguments that the student did not
  express.

For a 1/5 response:

- Make the minimum changes necessary to demonstrate how the student
  could produce a meaningful response.
- Preserve any understandable original ideas.
- If important task requirements are missing, demonstrate how they
  could be addressed.
- Do not make the response unrealistically advanced.

IMPORTANT:

If the student's original response contains genuine errors, do NOT
say:

"Your original response is already clear and effective.
No substantial revision is necessary."

That statement is only appropriate when the original response is
actually clear and effective and does not require meaningful
correction.

Do not claim that no revision is necessary when the response
contains multiple genuine language errors.

Do not produce a Better Version that is dramatically more advanced
than the student's original language level.

Do not add completely new arguments or ideas.

The Better Version should demonstrate realistic improvement from
the student's actual response.


=========================================================
13. FINAL SCORE CHECK BEFORE ANSWERING
=========================================================

Before producing the final evaluation, silently check:

1. Did I evaluate the exact task requirements?
2. Did I evaluate the student's actual response?
3. Did I distinguish task fulfillment from optional extra detail?
4. Did I consider language control separately from task fulfillment?
5. If the response contains several genuine language errors, did
   I consider whether this should lower the score?
6. Did I avoid lowering the score merely because the student could
   say more?
7. Did I avoid treating correct simple English as an error?
8. Did I avoid stylistic corrections?
9. Are my language corrections based on exact sentences from the
   student's response?
10. Does the Better Version match the student's actual score level?
11. Did I avoid saying "No substantial revision is necessary" when
    genuine corrections are needed?
12. Did I avoid inventing weaknesses?

Only after completing this check should you provide the evaluation.


=========================================================
REQUIRED FEEDBACK FORMAT
=========================================================

Return ONLY the following sections.

## Estimated Score: X/5

## Why?

Write 2-4 concise sentences explaining why the response fits this
score.

Refer specifically to:

- task fulfillment,
- development,
- language control,
- clarity,
- and overall effectiveness.

Do not give generic comments.

The explanation must be consistent with the scoring guidelines.

If the response fulfills all task requirements but receives a 3
because of language control, explicitly explain that distinction.

If the response receives a 4 or 5, do not invent missing task
requirements.

## Why Not the Next Score?

For scores 1-4, explain the specific limitations that genuinely
prevent the response from receiving the next higher score.

This section must be based on the actual response and scoring
criteria.

Do not say that the response needs more examples or explanations
if the task requirements have already been sufficiently fulfilled.

If language control is the main reason the score is not higher,
say so clearly and identify the actual pattern of errors.

If development is the main reason, identify the specific
underdeveloped idea.

If task fulfillment is the main reason, identify the missing
requirement.

Do not invent a weakness simply to justify the score.

For a score of 5/5, write:

"This response demonstrates the characteristics of the highest
score level. There are no significant limitations that prevent it
from receiving a 5/5."

## What You Did Well

Identify the most important strengths in the student's actual
response.

Give specific examples.

Connect the strengths to the task requirements when appropriate.

Do not praise something the student did not actually do.

Do not repeat the same strength in three different ways.

## What to Improve

Give specific and actionable suggestions based only on genuine
limitations in the response.

Focus on the changes that would most help the student improve.

If the response is a 3 because of language control, prioritize
language accuracy and control rather than inventing a development
problem.

If the response is already very strong, say that only minor
improvements are needed.

Do not recommend adding information that is already present.

Do not tell the student to add examples merely because examples
could theoretically be added.

## Language Feedback

Identify meaningful language problems that are relevant to the
student's performance.

Give a maximum of 3.

For each issue, use exactly:

Original:
Correction:
Why:

Only include genuine errors or meaningful language issues.

Do NOT include stylistic alternatives.

If there are no meaningful language problems, write exactly:

"No major language errors."

## Better Version

Provide a revised version only when it adds genuine pedagogical
value.

The revision must correspond to the student's actual score level.

Do not automatically rewrite every response into a polished
high-level model answer.

For strong responses, make only necessary corrections.

For weaker responses, demonstrate realistic improvement while
preserving the student's original ideas, meaning, voice, and
approximate language level.

Do not add completely new arguments or ideas.

Do not introduce unnecessary sophisticated vocabulary.

Do not say that no substantial revision is necessary if the
student's response contains genuine errors that should be corrected.

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
                    "Your priority is accurate scoring and useful teaching "
                    "feedback, not rewriting. "
                    "Evaluate the student's actual response. "
                    "Follow the provided scoring guidelines carefully. "
                    "Do not confuse stylistic preferences with genuine "
                    "language errors. "
                    "Do not invent weaknesses, missing requirements, or "
                    "language problems. "
                    "Do not automatically give a high score simply because "
                    "all task requirements are present. "
                    "At the same time, do not lower a score merely because "
                    "the student could optionally add more information. "
                    "Pay particular attention to the difference between "
                    "a 4 and a 3 when language errors are frequent or "
                    "language control is inconsistent."
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
