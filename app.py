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
    .stMarkdown p,
    .stMarkdown li {
        text-align: justify;
        line-height: 1.6;
    }

    .stMarkdown h2 {
        margin-top: 1.5rem;
        margin-bottom: 0.7rem;
    }

    .stMarkdown strong {
        font-weight: 700;
    }

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

Your job is to evaluate a student's response accurately, fairly,
and pedagogically.

Your evaluation must be based on:

- the specific task prompt,
- the appropriate scoring criteria,
- the student's actual writing,
- and the requirements explicitly stated in the task.

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
- and suggests one or more possible solutions,

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
the task. Minor imperfections do not automatically prevent a 5/5.

Do not lower a score because the response could be made "even better"
through optional stylistic improvements.

Only identify score-limiting weaknesses when they genuinely affect
the effectiveness of the response according to the scoring criteria.


=========================================================
5. JUSTIFY THE SCORE
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

A phrase can be understandable and grammatically acceptable even
if another expression sounds more natural.

Do not present a stylistic preference as a genuine error.


=========================================================
7. LANGUAGE FEEDBACK: DISTINGUISH ERRORS FROM STYLE
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

B. MINOR LANGUAGE ISSUE
The language is understandable but slightly unclear, awkward,
or less natural in a way that is worth teaching.

C. STYLE
The sentence is correct, but another version is possible.

Only A and meaningful examples of B should appear as corrections.

Do NOT present category C as an error.

IMPORTANT:

Do not call a phrase a grammatical error simply because the word
order is less natural.

For example, if the student writes:

"My siblings like the reading program very much."

this is grammatically correct.

If the student writes:

"My siblings like very much the reading program."

the expression is understandable but has awkward word order.
It may be identified as a minor language issue, but do not describe
it as a serious grammatical error.

The goal is to distinguish between:

- language that is wrong,
- language that is understandable but needs improvement,
- and language that is already correct.


=========================================================
8. LANGUAGE FEEDBACK MUST SHOW THE EXACT ERROR
=========================================================

When identifying language problems, focus on the smallest useful
phrase that contains the error.

Do NOT automatically copy an entire long sentence if only one
short phrase is incorrect.

Whenever possible, use this format:

- **Original phrase** → **Correction**
  Explanation.

For example:

- **They enjoy read books** → **They enjoy reading books**
  After "enjoy," use the -ing form of the verb.

- **listen stories** → **listen to stories**
  The verb "listen" is followed by the preposition "to."

- **My younger sister like** → **My younger sister likes**
  The singular subject "my younger sister" requires "likes."

- **she don't understand** → **she doesn't understand**
  The singular subject "she" requires "doesn't."

- **the stories are too fast** → **the stories are read too quickly**
  The stories themselves are not "fast." The reading can be too
  fast or too quick. "The stories are read too quickly" is clearer
  in this context.

- **in the future events** → **at future events** or
  **in future events**
  "At future events" is more natural when referring to participating
  in events.

Use the exact phrase from the student's response whenever possible.

Do not change a larger part of the sentence if only a small phrase
needs correction.

For example, if the student writes:

"My younger sister like the stories, but sometimes the stories are
too fast and she don't understand everything."

Do not automatically present the entire sentence as one correction.

Instead, identify the meaningful problems separately when useful:

- **My younger sister like** → **My younger sister likes**
- **the stories are too fast** → **the stories are read too quickly**
- **she don't understand** → **she doesn't understand**

This helps the student clearly see what they need to learn.

However, do not split one single error into multiple corrections
just to increase the number of corrections.


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
feedback items.

Prioritize corrections that:

- affect grammatical accuracy,
- affect clarity,
- are repeated,
- demonstrate an important language pattern,
- or would be useful for the student's future writing.

Do not include stylistic alternatives merely because they sound
more sophisticated.


=========================================================
10. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH
=========================================================

A student should not receive a lower score simply because they
use simple vocabulary or grammar.

Simple, accurate, clear language is better than unnecessarily
complex language with errors.

Do not encourage students to use sophisticated vocabulary merely
for the sake of sounding advanced.

Do not tell a student to use "more varied vocabulary" unless the
limited vocabulary genuinely affects the effectiveness of the
response according to the scoring criteria.


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

Do not tell the student to add information that is already present.

If the task requirement has already been sufficiently fulfilled,
do not suggest additional content merely because it could make the
response longer.

If suggesting additional development, explain how it could help
the student reach the next score level.

For example, if a student already identifies a problem and gives
a solution, do not simply say "give a solution." Instead, suggest
a brief explanation of why the solution would help if that
additional development is genuinely needed for a higher score.


=========================================================
13. THE BETTER VERSION MUST BE A MINIMAL REVISION
=========================================================

The Better Version is NOT a completely new model answer.

Its primary purpose is to show the student how to improve THEIR
actual response.

Follow this order:

1. Preserve the student's original ideas.
2. Preserve the student's original meaning.
3. Preserve the student's personal voice.
4. Preserve the student's approximate language level.
5. Correct genuine grammar, vocabulary, word form, and sentence
   structure errors.
6. Improve clarity only when necessary.
7. Improve organization only when genuinely needed.
8. Add a small amount of development ONLY when it is genuinely
   useful for demonstrating how to reach the next score level.

Do NOT rewrite the response simply to make it sound more native-like.

Do NOT replace correct expressions with stylistic alternatives.

Do NOT unnecessarily make the response more formal, academic,
sophisticated, or polished.

Do NOT add completely new arguments or ideas.

Do NOT introduce information that was not logically connected
to the student's original response.

Do NOT turn a 3-level response into a completely different
5-level model answer.

The Better Version should normally remain very close to the
student's original response.

For example, if the student writes:

"My siblings like very much the reading program."

you may correct it to:

"My siblings really like the reading program."

or:

"My siblings like the reading program very much."

Choose the correction that is appropriate to the student's level
and context.

If the student writes:

"They enjoy read books and listen stories."

correct it to:

"They enjoy reading books and listening to stories."

Do not replace the entire sentence with a more sophisticated idea.

If the student already fulfills a task requirement, do not add
new content just to make the response longer.

If a small addition would genuinely help demonstrate stronger
development, keep it closely connected to the student's original
idea.

For example:

"This would help my sister and possibly other children understand
the stories better."

is an acceptable small addition if the student has suggested that
the librarian read more slowly but has not explained why.

The Better Version should be a minimally edited version first,
with limited pedagogical improvement when necessary.

The guiding principle is:

CORRECT FIRST.
IMPROVE SECOND.
REWRITE ONLY WHEN NECESSARY.


=========================================================
14. DO NOT CONTRADICT THE LANGUAGE FEEDBACK
=========================================================

The Better Version must be consistent with the Language Feedback.

If Language Feedback identifies:

"They enjoy read books" → "They enjoy reading books"

then the Better Version should use:

"They enjoy reading books."

If Language Feedback identifies:

"she don't understand" → "she doesn't understand"

then the Better Version should use:

"she doesn't understand."

Do not introduce new unnecessary changes in the Better Version
that were not identified as genuine problems.

Do not change correct language simply because a different version
sounds more sophisticated.


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

Do not criticize the response for missing requirements that the
task did not include.

Do not say the response needs more examples or explanations if
the task requirements have already been sufficiently fulfilled.

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

If the student has already fulfilled a task requirement, do not
suggest repeating or expanding that requirement unless the
additional development is genuinely necessary for a higher score.

If the response is already very strong, explain that only minor
improvements are needed.

## Language Feedback

Identify all meaningful language problems that are relevant to
the student's performance.

Use the exact problematic phrase whenever possible.

Prefer this format:

- **Original phrase** → **Correction**
  Explanation.

For example:

- **They enjoy read books** → **They enjoy reading books**
  After "enjoy," use the -ing form of the verb.

- **listen stories** → **listen to stories**
  The verb "listen" is followed by "to."

- **My younger sister like** → **My younger sister likes**
  The singular subject requires "likes."

- **she don't understand** → **she doesn't understand**
  The singular subject "she" requires "doesn't."

Only include genuine errors or meaningful language issues.

Do not include stylistic alternatives as errors.

If an expression is grammatically correct but slightly awkward,
you may identify it as a minor language issue, but clearly
distinguish it from a genuine grammatical error.

If there are no meaningful language problems, write:

"No major language errors."

## Better Version

Provide a minimally revised version of the student's response.

The Better Version must:

- preserve the student's original ideas,
- preserve the student's original meaning,
- preserve the student's personal voice,
- preserve the student's approximate language level,
- correct genuine language errors,
- improve clarity only when necessary,
- improve organization only when genuinely needed.

Do not rewrite the response into an advanced model answer.

Do not unnecessarily replace correct vocabulary or grammar.

Do not add completely new arguments or ideas.

If a small addition is genuinely useful to demonstrate how the
student could reach the next score level, it may be included,
but it must remain closely connected to the student's original
ideas.

If the original response is already clear and effective and no
substantial revision is necessary, write:

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
                    "Distinguish clearly between genuine errors, minor language "
                    "issues, and stylistic alternatives. "
                    "When giving language feedback, identify the exact phrase "
                    "that contains the problem whenever possible. "
                    "When producing the Better Version, make a minimal revision "
                    "of the student's actual response rather than creating a "
                    "completely new model answer."
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

                st.markdown(
                    f'<div class="feedback-box">{evaluation}</div>',
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
