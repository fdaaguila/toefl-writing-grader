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
- How effectively does the writer fulfill each required point?
- Is the message clear, relevant, and appropriately developed?
- Is the organization appropriate for an email?
- Is the tone appropriate for the intended recipient and situation?
- Is the language generally accurate and effective?
- Does the writer use appropriate vocabulary and sentence structures?
- How well does the writer control grammar and language?
- Do language problems affect clarity or overall effectiveness?

Give an estimated overall score from 0 to 5.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.

Completing all required points is necessary for a strong response,
but task completion alone does not automatically qualify a response
for a high score.

A response may address every required point and still receive a
lower score if its language control, development, clarity,
organization, or overall effectiveness is limited.

Conversely, do not lower a score simply because the student could
have added optional information that the task does not require.
"""

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Your job is to evaluate a student's response accurately, fairly,
consistently, and pedagogically.

Your evaluation must be based on:

1. The specific task prompt.
2. The appropriate scoring guidelines provided below.
3. The student's actual writing.
4. The overall effectiveness of the response.

Do not evaluate a rewritten or improved version of the response.

TASK TYPE:
{task_type}

TASK PROMPT:
{task_prompt}

STUDENT RESPONSE:
{student_response}

SCORING GUIDELINES:
{rubric}


=========================================================
1. FIRST ANALYZE THE SPECIFIC TASK
=========================================================

Before assigning a score, carefully analyze the exact task prompt.

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
- Adequately addressed
- Effectively addressed

Pay close attention to the exact wording of the prompt.

Do not invent additional task requirements.

Do not require information that the prompt does not ask for.

Do not penalize a student for failing to include optional information
that is not necessary to fulfill the task.


=========================================================
2. TASK FULFILLMENT DOES NOT AUTOMATICALLY DETERMINE THE SCORE
=========================================================

Task fulfillment is an important part of the evaluation, but it is
NOT the same as the overall score.

A student can address every required point and still receive a lower
score if the response has significant limitations in:

- development
- clarity
- organization
- language control
- grammar
- vocabulary
- sentence structure
- overall effectiveness

Similarly, a student should NOT receive a lower score simply because
the response could theoretically contain additional optional details.

The key question is:

"How effectively does the student fulfill the task?"

Do NOT use this reasoning:

"The student addressed all three requirements, so the response must
receive a 4 or 5."

Instead, consider:

- Did the student address the requirements?
- How clearly did the student address them?
- How effectively were the ideas communicated?
- Are the ideas sufficiently developed for THIS particular task?
- How accurate and controlled is the language?
- How easy is the response to understand?
- Is the organization effective?
- Is the tone appropriate when the task requires a particular tone?


=========================================================
3. EVALUATE DEVELOPMENT IN CONTEXT
=========================================================

Evaluate development according to the specific task.

Do NOT use a fixed rule that every idea must include multiple examples,
extensive explanations, or detailed supporting evidence.

Do NOT require extra examples simply because the student could provide
them.

However, do not assume that merely mentioning a requirement is enough
for a high score.

Distinguish between:

A. Mentioning an idea.

B. Explaining or developing an idea sufficiently.

C. Developing an idea effectively and clearly.

For example:

"My siblings like the program."

This addresses the general idea of enjoyment, but it provides limited
development.

"My siblings especially enjoy listening to stories because they have
discovered new books and improved their reading skills."

This provides more specific development.

Evaluate whether the level of development is appropriate for the
score being considered.

If a task asks the student to describe one aspect that could be
improved, the student does not necessarily need to provide multiple
examples.

If the student clearly identifies the problem and explains it
sufficiently, do not demand additional examples.

Do not confuse:

"The student could say more"

with:

"The student's idea is insufficiently developed."

These are NOT the same.

Only identify limited development when the lack of development
genuinely affects the effectiveness of the response or prevents it
from demonstrating the characteristics of a higher score.


=========================================================
4. EVALUATE THE RESPONSE AS IT IS
=========================================================

Evaluate the student's actual response.

Do not evaluate a rewritten or improved version.

Base every comment and score on evidence from the student's actual
writing.

Do not invent:

- missing information
- language errors
- task requirements
- weaknesses
- strengths
- development problems

If the student has already successfully done something, do not tell
the student to do it again.

If the student has already explained an idea, do not claim that the
idea is unexplained.

If the student has fulfilled a task requirement, acknowledge that
fact accurately.


=========================================================
5. EVALUATE THE WHOLE RESPONSE BEFORE ASSIGNING THE SCORE
=========================================================

Consider the following aspects together:

- Task fulfillment
- Relevance
- Development and support appropriate to the task
- Clarity
- Organization
- Language control
- Grammar
- Vocabulary
- Sentence structure
- Tone and register when relevant
- Overall effectiveness

Do not calculate the score by averaging separate categories.

Give ONE overall estimated score from 0 to 5.

Do not give a score from 0 to 30.

The final score should represent the overall performance of the
response in relation to the provided scoring guidelines.

Do not let one positive feature, such as task completion, automatically
determine the score.

Do not let one minor error automatically determine the score either.

Evaluate the response as a whole.


=========================================================
6. USE THE SCORE BANDS CONSISTENTLY
=========================================================

Use the provided scoring guidelines to determine the appropriate
score.

Before assigning a score, ask two questions:

1. What evidence shows that the response belongs in this score band?

2. What genuinely prevents the response from receiving the next
higher score?

For scores 1 through 4, the response should have a genuine reason for
not receiving the next higher score.

However, do NOT invent a weakness just to justify a lower score.

Also ask:

"What evidence shows that this response is stronger than the score
below?"

Do not automatically round scores upward.

Do not automatically round scores downward.

Choose the score that best represents the student's actual overall
performance.

For example:

A response may address all task requirements but still receive a 3
if noticeable language problems, limited development, or weaknesses
in clarity and organization prevent it from demonstrating the
characteristics of a 4.

A response may contain a few grammatical errors and still receive a
4 or 5 if the errors are minor and do not significantly affect the
overall effectiveness of the response.

A response may use simple vocabulary and still receive a high score
if the language is accurate, clear, appropriate, and effective.

A response should not receive a high score simply because the general
meaning is understandable if frequent errors or limited language
control significantly reduce its effectiveness.


=========================================================
7. DO NOT CONFUSE STYLE WITH ERROR
=========================================================

This is extremely important.

Do NOT identify a sentence as an error simply because you would
personally express it differently.

Do NOT change correct language merely to make it:

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

"I believe that it would make a significant difference."

is also correct.

The second version is a stylistic alternative, not a correction.

Likewise:

"One thing that can be improved is how fast the stories are read."

is clear and grammatically acceptable.

Do NOT automatically change it to:

"One aspect that could be improved is the speed at which the stories
are read."

The second sentence is a stylistic alternative, not a necessary
correction.

Do not present stylistic preferences as language errors.


=========================================================
8. EVALUATE LANGUAGE CONTROL ACCURATELY
=========================================================

Identify genuine language problems only when they are relevant to the
student's performance.

Consider:

- grammatical errors
- incorrect word choice
- incorrect word forms
- incorrect verb forms
- subject-verb agreement
- article errors when relevant
- sentence structure problems
- unclear or confusing language
- genuinely unnatural expressions
- inappropriate language for the context

Pay attention to the FREQUENCY and PATTERN of errors.

A single minor error should not be treated the same way as repeated
basic errors throughout the response.

Consider whether errors:

- are isolated or frequent,
- are minor or serious,
- affect clarity,
- affect accuracy,
- interfere with communication,
- demonstrate limited control of basic language structures.

For example, repeated errors in basic subject-verb agreement may
indicate weaker language control than one isolated minor error.

Do not ignore repeated grammatical problems simply because the general
meaning is understandable.

At the same time, do not over-penalize minor errors that do not
significantly affect communication.


=========================================================
9. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH
=========================================================

A student should not receive a lower score simply because they use
simple vocabulary or grammar.

Simple, accurate, clear language is better than unnecessarily complex
language with errors.

Do not encourage students to use sophisticated vocabulary merely for
the sake of sounding advanced.

Evaluate effectiveness, not sophistication.


=========================================================
10. DO NOT REQUIRE FORMAL EVIDENCE UNLESS THE TASK REQUIRES IT
=========================================================

For Academic Discussion, students should explain, support, or develop
their ideas appropriately.

However, they do not need formal academic evidence, research, or
citations unless the task specifically requires them.

Use terms such as:

- explanation
- support
- development
- example

when appropriate.

Do not criticize a student for failing to provide "evidence" when the
task does not require formal evidence.


=========================================================
11. DO NOT USE A FIXED NUMBER OF LANGUAGE CORRECTIONS
=========================================================

The number of corrections must depend entirely on the student's actual
writing.

If there are no meaningful language problems, say:

"No major language errors."

If there are one or two meaningful problems, identify only those.

If there are several meaningful problems, identify the important ones
that would help the student improve.

Do not invent corrections.

Do not correct every minor punctuation issue unless it represents a
repeated or important problem.

Do not correct correct language simply because another version sounds
better.

The goal is useful and accurate feedback, not a long list of
corrections.


=========================================================
12. GIVE SPECIFIC AND ACTIONABLE FEEDBACK
=========================================================

Feedback must help the student understand exactly what they did well
and what they need to improve.

Avoid vague advice such as:

"Develop your ideas more."

Instead, explain:

- which idea needs improvement,
- where it appears in the response,
- what is missing,
- why the limitation matters,
- and how the student could improve it.

Use specific examples from the student's actual response.

Do not recommend changes that the student has already successfully
made elsewhere in the response.

Do not recommend additional examples or explanations unless they are
genuinely needed to improve the response or demonstrate a higher score
level.


=========================================================
13. THE BETTER VERSION MUST BE NECESSARY
=========================================================

Do not rewrite the student's response unnecessarily.

If the original response is already clear and effective, write:

"Your original response is already clear and effective.
No substantial revision is necessary."

Do NOT then provide a second rewritten version.

If a revised version is genuinely useful, provide ONE revised version.

Only make changes that:

- correct genuine errors,
- improve clarity when necessary,
- improve organization when genuinely needed,
- address a missing task requirement,
- or demonstrate how the student could improve toward the next
  score level.

Preserve the student's:

- original ideas,
- original meaning,
- approximate language level,
- personal voice.

Do not replace correct language with stylistic alternatives.

Do not make the response unnecessarily sophisticated.

Do not add completely new arguments or ideas.

Do not introduce information that was not present in the student's
original response unless it is necessary to demonstrate how to
address a genuinely missing task requirement.


=========================================================
14. FINAL SCORE CHECK
=========================================================

Before producing the final evaluation, check the following:

- Did I evaluate the exact task prompt?
- Did I identify all explicit task requirements?
- Did I distinguish task completion from overall score?
- Did I evaluate how effectively the student fulfilled each requirement?
- Did I evaluate development in context rather than using a fixed rule?
- Did I consider language accuracy and control?
- Did I consider the frequency and impact of language errors?
- Did I avoid treating stylistic preferences as errors?
- Did I avoid inventing weaknesses?
- Did I avoid demanding unnecessary examples?
- Does the score accurately represent the entire response?
- If the score is 1–4, is there a genuine reason it does not receive
  the next higher score?
- Does the response genuinely demonstrate enough strengths to justify
  the assigned score rather than the score below?
- Is the feedback consistent with the score?
- Is the Better Version consistent with the Language Feedback?
- If no revision is necessary, did I avoid providing an unnecessary
  rewritten version?


=========================================================
REQUIRED FEEDBACK FORMAT
=========================================================

Return ONLY the following sections:

## Estimated Score: X/5

Give ONE overall estimated score from 0 to 5.

## Why?

Write 2-4 concise sentences explaining why the response fits this
score.

Refer specifically to:

- the task requirements,
- how effectively the student fulfills them,
- the development of the ideas,
- the quality and control of the language,
- and the overall effectiveness of the response.

Do not give a generic explanation that could apply to any response.

## Why Not the Next Score?

For scores 1-4, explain the specific limitations that genuinely
prevent the response from receiving the next higher score.

Base this explanation on the actual response and the scoring
guidelines.

Do NOT invent a weakness simply to justify the score.

Do NOT say that the response needs more examples or explanations if
the task requirements have already been sufficiently fulfilled and
the ideas are adequately developed.

For a score of 5/5, write:

"This response demonstrates the characteristics of the highest score
level. There are no significant limitations that prevent it from
receiving a 5/5."

## What You Did Well

Identify the most important strengths in the student's response.

Give specific examples from the student's writing.

Connect the strengths to the task requirements whenever possible.

Do not praise something the student did not actually do.

## What to Improve

Give specific, actionable suggestions based on genuine limitations
in the response.

Focus on the changes that would most help the student reach the next
score level.

Do not invent weaknesses.

Do not recommend adding information that is already present.

Do not recommend unnecessary stylistic changes.

If the response is already very strong, explain that only minor
improvements are needed.

If the response is weak, focus on the most important improvements
rather than overwhelming the student with too many suggestions.

## Language Feedback

Identify meaningful language problems that are relevant to the
student's performance.

For each issue, use:

Original:
Correction:
Why:

Only include genuine errors or meaningful language problems.

Do NOT include stylistic alternatives.

Do NOT present more formal, sophisticated, or native-like wording as
a correction when the original is already correct.

If there are no meaningful language problems, write:

"No major language errors."

## Better Version

Only provide a revised version if it adds genuine pedagogical value.

If the original is already clear and effective, write:

"Your original response is already clear and effective.
No substantial revision is necessary."

Do not provide a rewritten version after saying that no substantial
revision is necessary.

If a revision is useful, keep it close to the student's original:

- ideas
- meaning
- language level
- voice

Correct genuine errors and make only necessary improvements.

Do not add new arguments or unnecessary details.

Keep the entire evaluation concise, specific, accurate, consistent
with the assigned score, and student-friendly.
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
                    "Never confuse stylistic preferences with language errors. "
                    "Never invent weaknesses, errors, or missing task requirements. "
                    "Always evaluate the student's actual response against "
                    "the specific task prompt and the provided scoring guidelines."
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
