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

1. The exact task prompt.
2. The appropriate scoring guidelines.
3. The student's actual response.

Do not evaluate a rewritten version of the student's response.

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

For example, if the task asks the student to:

- explain what their siblings enjoyed about the program,
- describe one aspect of the program that could be improved,
- and offer to help with future events,

evaluate whether the student actually does each of these things.

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
does not mean that longer responses automatically receive higher
scores.

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
the task.

Minor imperfections do not automatically prevent a 5/5.

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
the student's actual response.

Do not give generic explanations that could apply to any student.

Most importantly, determine whether the response genuinely falls
below the next score level.

For scores 1-4, explain what specific limitations prevent the
response from receiving the next higher score.

However, do NOT force yourself to invent a weakness.

If the response actually demonstrates the characteristics of the
next higher score, give the higher score.

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

is correct.

Do NOT automatically replace it with:

"I believe that it would make a significant difference."

The second version is only a stylistic alternative.

Likewise:

"One thing that can be improved is how fast the stories are read."

is clear and grammatically acceptable.

Do NOT automatically replace it with:

"One aspect that could be improved is the speed at which the stories
are read."

That is a stylistic alternative, not a necessary correction.

=========================================================
7. ONLY CORRECT REAL LANGUAGE PROBLEMS
=========================================================

Identify language problems only when they are genuinely relevant.

Consider:

- grammatical errors
- incorrect word choice
- incorrect word forms
- incorrect verb forms
- subject-verb agreement errors
- incorrect verb patterns
- missing or incorrect articles when they affect accuracy
- sentence structure problems
- unclear or confusing language
- genuinely unnatural expressions
- inappropriate language for the context

Distinguish between:

A. REAL ERROR

The language is incorrect.

Example:

"My younger sister like the stories."

Correction:

"My younger sister likes the stories."

B. MINOR LANGUAGE ISSUE

The language is understandable but slightly unclear, awkward,
or less natural in a way that is genuinely worth teaching.

C. STYLE

The sentence is correct, but another version is possible.

Only A and meaningful examples of B should appear as corrections.

Do NOT present category C as an error.

=========================================================
8. DO NOT OVER-CORRECT
=========================================================

Do NOT give a predetermined number of corrections.

The number of corrections must depend entirely on the student's
actual writing.

If there are no meaningful language problems, write:

"No major language errors."

If there are one or two meaningful problems, identify only those.

If there are several meaningful problems, identify the important
ones that would help the student improve.

Do not invent corrections simply to provide more feedback.

Do not correct every minor punctuation issue unless it represents
a repeated or important problem.

The goal is useful and accurate feedback, not a long list of
corrections.

=========================================================
9. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH
=========================================================

A student should not receive a lower score simply because they
use simple vocabulary or grammar.

Simple, accurate, clear language is better than unnecessarily
complex language with errors.

Do not encourage students to use sophisticated vocabulary merely
for the sake of sounding advanced.

Do not tell a student to use "more varied vocabulary" or "more
complex sentence structures" unless the lack of range genuinely
limits the response according to the scoring criteria.

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

Do not criticize a response for lacking "evidence" unless the
task specifically requires evidence.

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

Do not recommend adding examples or explanations merely because
they are possible.

Only recommend additional development when it is genuinely needed
to fulfill the task or reach the next score level.

=========================================================
12. THE BETTER VERSION MUST STAY VERY CLOSE TO THE ORIGINAL
=========================================================

This rule is extremely important.

The Better Version is NOT an opportunity to rewrite the student's
response as if a native speaker or advanced student had written it.

The purpose of the Better Version is to show the student how THEIR
OWN response could be improved.

Preserve the student's:

- original ideas
- original meaning
- personal voice
- approximate language level
- original organization whenever it is effective
- original details whenever they are relevant

Make the FEWEST changes necessary.

The Better Version should normally be a minimally edited version
of the student's original response.

PRIORITY ORDER FOR CHANGES:

1. Correct genuine grammatical errors.
2. Correct incorrect verb forms or word forms.
3. Correct incorrect word choice when it affects meaning or accuracy.
4. Fix unclear language when clarification is genuinely necessary.
5. Fix awkward expressions only when they are genuinely problematic,
   not merely because another expression sounds more natural.
6. Improve organization only when the original organization causes
   a real problem.
7. Add a small amount of development ONLY when a task requirement
   is genuinely incomplete or when the lack of development clearly
   limits the score.

DO NOT:

- rewrite the entire response unnecessarily,
- replace simple correct vocabulary with advanced vocabulary,
- change the student's voice,
- remove relevant details,
- change the student's ideas,
- add unrelated arguments,
- invent personal experiences,
- invent examples,
- add information that the student did not imply,
- make the response sound like a 5/5 response if the student's
  original level is lower,
- rewrite correct sentences just because another version sounds
  more natural,
- shorten the response unnecessarily.

For example, if the student writes:

"My siblings like very much the reading program."

A minimal correction could be:

"My siblings really like the reading program."

Do not unnecessarily rewrite the sentence as:

"My siblings have greatly benefited from participating in the
weekend reading program."

The second version adds meaning and vocabulary that the student
did not originally express.

If the student writes:

"They enjoy read books and listen stories."

A necessary correction is:

"They enjoy reading books and listening to stories."

Do not replace it with:

"They particularly enjoy engaging in reading activities and
listening to captivating stories."

That would be an unnecessary stylistic rewrite.

If the student writes:

"My younger sister like the stories, but sometimes the stories are
too fast and she don't understand everything."

A useful correction may be:

"My younger sister likes the stories, but sometimes the stories
are read too quickly, and she doesn't understand everything."

This is acceptable because it corrects genuine errors and clarifies
the meaning.

DO NOT automatically add new explanations such as:

"This helps children improve their reading skills."

unless the student originally expressed that idea.

=========================================================
13. BETTER VERSION MUST REFLECT THE SCORE LEVEL
=========================================================

The Better Version should demonstrate realistic improvement from
the student's original response.

For a score of 1 or 2:

- Correct the most important language problems.
- Improve clarity where necessary.
- Add only minimal development if the task is not sufficiently
  fulfilled.
- Do not transform the response into an advanced response.
- Preserve as much of the student's original content as possible.

For a score of 3:

- Correct genuine language errors.
- Improve unclear or genuinely awkward expressions.
- Preserve the student's original organization and ideas.
- Add only limited development if a genuine weakness in task
  fulfillment or development prevents a higher score.
- Do not rewrite the response into a 4/5 or 5/5 response.

For a score of 4:

- Make only necessary corrections.
- Preserve the student's original wording whenever it is correct.
- Make small improvements only where they genuinely improve
  accuracy, clarity, or task effectiveness.
- Do not add unnecessary sophistication.

For a score of 5:

- Do not rewrite the response simply to make it sound better.
- If there are no meaningful errors, state:

"Your original response is already clear and effective.
No substantial revision is necessary."

If there are minor genuine errors, correct only those errors.

=========================================================
14. DO NOT CONTRADICT YOUR OWN FEEDBACK
=========================================================

The evaluation must be internally consistent.

If you identify genuine language errors in the Language Feedback,
the Better Version should correct those same errors.

If you say that no substantial revision is necessary, do not then
provide a heavily rewritten version.

If you say that the student's ideas are sufficiently developed,
do not rewrite the response by adding extensive new development.

If you say that a student's response fully fulfills the task,
do not criticize the student for failing to include information
that the task did not require.

If the response receives a 5/5, do not suggest optional changes
as though they are necessary for a higher score.

If the response receives a 3/5 because of language problems,
the Better Version should primarily correct those language problems
rather than substantially changing the content.

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
- and the overall quality of the response.

Base the explanation on the student's actual response.

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

Do not recommend more examples or more detail unless they are
genuinely needed according to the task and scoring criteria.

If the response is already very strong, explain that only minor
improvements are needed.

## Language Feedback

Identify all meaningful language problems that are relevant to
the student's performance.

For each issue, use exactly this format:

Original:
Correction:
Why:

Only include genuine errors or meaningful language issues.

Do not include stylistic alternatives.

If there are no meaningful language problems, write:

"No major language errors."

## Better Version

The Better Version must be a minimally edited version of the
student's original response.

Before rewriting, compare the student's original response with
the Language Feedback.

Correct the genuine language problems identified in the feedback.

Preserve the student's original ideas, details, meaning, voice,
organization, and approximate language level whenever possible.

Do not rewrite the response merely to make it sound more natural,
more sophisticated, more academic, or more native-like.

Do not add new arguments or invented information.

Do not remove relevant information.

Do not substantially restructure the response unless the original
organization genuinely prevents the student from communicating
effectively.

If the student has fully addressed the task, do not add new content
just to make the response longer.

If the student has not fully addressed a required task point,
make only the minimum addition necessary to address that requirement.

If the response is already clear and effective and contains no
meaningful language problems, state:

"Your original response is already clear and effective.
No substantial revision is necessary."

The Better Version should show the student how to improve THEIR
response, not replace it with a completely different response.

Keep the entire evaluation concise, specific, accurate,
internally consistent, and student-friendly.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and fair TOEFL Writing evaluator. "
                    "Your priority is accurate evaluation and useful teaching "
                    "feedback, not rewriting. "
                    "Evaluate the student's actual response. "
                    "Never invent weaknesses, errors, or missing task requirements. "
                    "Never confuse stylistic preferences with genuine language errors. "
                    "When providing a Better Version, make the fewest changes "
                    "necessary and preserve the student's original ideas, "
                    "meaning, voice, organization, and approximate language level. "
                    "Do not rewrite correct language unnecessarily."
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
