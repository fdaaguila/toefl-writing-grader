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

Give ONE estimated score from 0 to 5 based on the overall effectiveness
of the response.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.

Use the following general interpretation when assigning the score:

5:
The response is highly effective and successfully fulfills the task.
It addresses all required points clearly and appropriately. Ideas are
relevant and sufficiently developed for the specific task. Language
is generally accurate and effective. Minor grammatical errors,
awkward expressions, simple vocabulary, or optional opportunities
for additional detail do NOT automatically prevent a 5.

4:
The response is effective and fulfills the task. It addresses the
required points and communicates the intended message clearly.
Ideas are adequately developed. Language is generally accurate,
although there may be some noticeable errors or limitations that
occasionally reduce effectiveness. The response may be less
consistent or less polished than a 5, but it remains effective.

3:
The response generally fulfills the task and the main message is
understandable. However, the response may show noticeable limitations
in language control, development, clarity, or organization. There may
be several grammatical errors, incorrect verb forms, awkward
expressions, or limited development. These problems may sometimes
affect effectiveness, but the reader can generally understand the
writer's meaning.

2:
The response only partially fulfills the task or has significant
limitations in development, relevance, organization, or language
control. Frequent language problems may make parts of the response
difficult to understand. Important task requirements may be missing
or only minimally addressed.

1:
The response demonstrates very limited ability to accomplish the
task. It may be largely incomplete, difficult to understand, highly
irrelevant, or severely limited by language problems.

0:
The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.
"""

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Your job is to evaluate a student's response accurately, fairly,
consistently, and pedagogically.

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
program that could be improved, and the student clearly identifies
the problem and gives a reasonable suggestion for improvement,
the requirement may already be sufficiently addressed.

Do NOT automatically lower the score simply because the student
could provide additional details.

Before saying that an idea needs more development, check whether the
student has already explained or supported that idea elsewhere in
the response.

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

Likewise, do not give a 4 or 5 simply because all task requirements
are technically mentioned.

A response can fulfill all task requirements and still receive a
lower score if genuine language problems, limited language control,
weak development, unclear organization, or other rubric-relevant
limitations significantly reduce its effectiveness.

Consider the ENTIRE response when assigning the score.

Do not let one or two isolated errors automatically determine the
score.

At the same time, do not ignore repeated or significant errors simply
because the main message is understandable.

The score must reflect the overall performance of the response.


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

However, repeated grammatical errors, frequent incorrect verb forms,
persistent awkward sentence structures, or language problems that
noticeably reduce the effectiveness of the response should be
considered when deciding between a 5 and a lower score.

Do not lower a score because the response could be made "even better"
through optional stylistic improvements.

Only identify score-limiting weaknesses when they genuinely affect
the effectiveness of the response according to the scoring criteria.


=========================================================
5. DISTINGUISH BETWEEN SCORE BANDS
=========================================================

When deciding between two adjacent score levels, compare the response
directly with the characteristics of BOTH levels.

Do not assign a lower score simply because the response is not perfect.

Do not assign a higher score simply because the response fulfills
the basic task requirements.

For a 5:
The response should be highly effective overall. It should fulfill
the task successfully, communicate clearly, and demonstrate generally
accurate and effective language. Minor errors or simple language may
be acceptable if they do not meaningfully reduce effectiveness.

For a 4:
The response should be effective overall, but it may contain
noticeable limitations in language accuracy, development, or
effectiveness that make it less strong than a 5.

For a 3:
The response should generally communicate the intended message and
address the task, but limitations in language control, development,
clarity, or organization should be noticeable enough to distinguish
it from a clearly effective 4.

For a 2:
The response should show more substantial limitations. Important
parts of the task may be missing, development may be very limited,
or language problems may make parts of the response difficult to
understand.

For a 1:
The response should demonstrate very limited ability to accomplish
the task.

Use the actual severity, frequency, and impact of the problems to
distinguish between score bands.

Do not use a single grammatical error as the reason for a lower score.

Do not ignore several repeated grammatical errors simply because
the general meaning can still be understood.


=========================================================
6. JUSTIFY THE SCORE
=========================================================

After assigning the score, explain specifically why the response
fits that score.

Your explanation must refer to the actual task requirements and
the student's response.

Do not give generic explanations that could apply to any student.

Most importantly, determine whether the response genuinely falls
below the next score level.

For scores 1-4, explain the specific limitations that prevent the
response from receiving the next higher score.

However, do NOT force yourself to invent a weakness.

If, after carefully evaluating the task requirements and the rubric,
the response actually demonstrates the characteristics of the next
higher score, give the higher score.

Do not lower a score merely because there are optional ways to make
the response longer, more detailed, or more sophisticated.

For a 5/5 response, explain why the response demonstrates the
characteristics of the highest score level.

Do not say that a response is below a 5 simply because it could
include more examples unless the lack of development genuinely
affects the effectiveness of the response.

Do not say that a response is below a 4 simply because it could use
more sophisticated vocabulary.


=========================================================
7. DO NOT CONFUSE STYLE WITH ERROR
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


=========================================================
8. LANGUAGE FEEDBACK
=========================================================

Identify language problems only when they are genuinely relevant.

Consider:

- grammar errors
- incorrect word choice
- incorrect word forms
- incorrect verb forms
- article errors when relevant
- preposition errors
- sentence structure problems
- unclear or confusing language
- genuinely unnatural expressions
- inappropriate language for the context

Distinguish between:

A. REAL ERROR
The language is incorrect.

B. MINOR LANGUAGE ISSUE
The language is understandable but slightly unclear, vague,
awkward, or less natural in a way that is worth teaching.

C. STYLE
The sentence is correct, but another version is possible.

Only A and meaningful examples of B should appear as corrections.

Do NOT present category C as an error.

When a phrase is understandable but awkward, explain that it is
awkward or unnatural rather than incorrectly calling it a grammar
error.

For example:

"My siblings like very much the reading program."

Possible correction:

"My siblings really like the reading program."
OR
"My siblings like the reading program very much."

Explain that the original word order is awkward and that the
correction provides a more natural sentence structure.

For example:

"They enjoy read books"

should be corrected to:

"They enjoy reading books"

because "enjoy" is followed by the -ing form.

For example:

"listen stories"

should be corrected to:

"listen to stories"

because "listen" is followed by "to" when referring to the thing
being heard.

For example:

"My younger sister like"

should be corrected to:

"My younger sister likes"

because the singular subject requires the third-person singular
verb form.

For example:

"she don't understand"

should be corrected to:

"she doesn't understand"

because the singular subject "she" requires "doesn't."

For example:

"the stories are too fast"

may be corrected to:

"the stories are read too quickly"
or
"the stories are read too fast"

when the intended meaning is that the reading speed is too fast.

Explain that the correction clarifies that the problem is the speed
at which the stories are being read, not the speed of the stories
themselves.

For example:

"in the future events"

may be corrected to:

"at future events"
or
"in future events"

depending on the intended meaning and context.

Do not automatically correct language that is already acceptable.


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
feedback points.

When several errors appear in one sentence, you may identify the
specific problematic phrases separately if doing so helps the
student understand the individual errors.


=========================================================
10. DO NOT PENALIZE SIMPLE BUT CORRECT ENGLISH
=========================================================

A student should not receive a lower score simply because they
use simple vocabulary or grammar.

Simple, accurate, clear language is better than unnecessarily
complex language with errors.

Do not encourage students to use sophisticated vocabulary merely
for the sake of sounding advanced.

Do not replace simple correct language with more advanced language
in the Better Version unless there is a genuine reason to do so.


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

If the response already sufficiently develops an idea, do not tell
the student to develop it further simply because more detail is
possible.

If additional development would genuinely help, explain exactly
what kind of development would be useful.


=========================================================
13. THE BETTER VERSION MUST STAY CLOSE TO THE ORIGINAL
=========================================================

This is extremely important.

The Better Version is NOT supposed to be a completely rewritten
model answer.

Its main purpose is to show the student how to improve THEIR OWN
response.

Preserve the student's:

- original ideas
- original meaning
- original position or purpose
- approximate language level
- personal voice
- overall organization when it is already effective

Do NOT unnecessarily change correct language.

Do NOT replace correct vocabulary with more sophisticated vocabulary
just to make the response sound more advanced.

Do NOT rewrite a sentence merely because another sentence sounds
more natural to you if the original is already acceptable.

Only make changes that:

- correct genuine language errors,
- improve clarity when necessary,
- improve organization when genuinely needed,
- address a missing task requirement,
- or add a small amount of development when the lack of development
  genuinely limits the score.

If the original response is at a lower score level, you may add
brief supporting details or explanations to demonstrate how the
student could move toward the next score level.

However, additions must be clearly relevant to the student's
original ideas.

Do NOT introduce completely new arguments, unrelated examples,
new opinions, or sophisticated ideas that the student did not
express.

For example, if the student says that the librarian reads too
quickly, it is acceptable to add:

"This would help my sister and possibly other children understand
the stories better."

It is NOT necessary to add a completely new idea such as asking
the librarian to organize discussion groups or create a new
reading curriculum unless the student originally suggested such
ideas.

The Better Version should feel like the student's own response,
only corrected and, when genuinely necessary, modestly improved.

If the response is already strong and clear, do not rewrite it
just for the sake of rewriting it.

Instead, write:

"Your original response is already clear and effective.
No substantial revision is necessary."

If a revision is useful, make the smallest meaningful changes
necessary.


=========================================================
14. OPTIONAL IMPROVEMENTS MUST BE CLEARLY DISTINGUISHED
=========================================================

Do not present optional stylistic improvements as necessary
corrections.

If the student's original language is correct but another version
would be more natural, clearer, or more effective, identify it as
an optional improvement rather than an error.

The Better Version should prioritize genuine corrections.

Optional additions may be included only when they help demonstrate
how the student could develop an idea or move toward a higher score.

Do not make optional additions that change the student's original
meaning or voice.


=========================================================
REQUIRED FEEDBACK FORMAT
=========================================================

Return ONLY the following sections.

IMPORTANT FORMATTING RULE:

Do NOT use Markdown heading symbols (#, ##, ###) for the first line.

The first line must be:

Estimated Score: X/5

Do not make the score a large Markdown heading.

Keep the score clearly visible but normal-sized.

The other section titles should remain as follows:

Why?

Why Not the Next Score?

What You Did Well

What to Improve

Language Feedback

Better Version

Do not make the entire response bold.

Use normal text for explanations.

Use the section titles as clear visual separators.

For the Language Feedback section, use concise correction pairs
where appropriate.

For example:

My siblings like very much the reading program
→ My siblings really like the reading program.
OR
→ My siblings like the reading program very much.

Brief explanation: The original word order is understandable but
awkward. These versions use a more natural word order.

They enjoy read books
→ They enjoy reading books.

Brief explanation: After "enjoy," use the -ing form of the verb.

listen stories
→ listen to stories.

Brief explanation: The verb "listen" is followed by the preposition
"to."

My younger sister like
→ My younger sister likes.

Brief explanation: The singular subject requires "likes."

she don't understand
→ she doesn't understand.

Brief explanation: The singular subject "she" requires "doesn't."

the stories are too fast
→ the stories are read too quickly.
OR
→ the stories are read too fast.

Brief explanation: This clarifies that the reading speed is too fast.

in the future events
→ at future events.
OR
→ in future events.

Brief explanation: The appropriate preposition depends on the
intended meaning and context.

Only include corrections that are actually present in the student's
response.

Do not include examples of errors that the student did not make.

=========================================================

Estimated Score: X/5

Why?

Write 2-4 concise sentences explaining why the response fits
this score.

Refer specifically to:

- the task requirements,
- how effectively the student fulfills them,
- the development of the ideas,
- the language control,
- and the overall quality of the response.

Why Not the Next Score?

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

What You Did Well

Identify the most important strengths in the student's response.

Give specific examples from the student's writing.

Connect the strengths to the task requirements whenever possible.

Do not praise something the student did not actually do.

What to Improve

Give specific, actionable suggestions based on genuine limitations
in the response.

Focus on the changes that would most help the student reach the
next score level.

Do not invent weaknesses.

If the response is already very strong, explain that only minor
improvements are needed.

Do not recommend adding information that is already present.

Language Feedback

Identify all meaningful language problems that are relevant to
the student's performance.

Use concise correction pairs in the format:

Original → Correction

Then give a brief explanation when useful.

Only include genuine errors or meaningful language issues.

Do not include stylistic alternatives as if they were errors.

If there are no meaningful language problems, write:

"No major language errors."

Better Version

Only provide a revised version if it adds genuine pedagogical value.

If the original is already clear and effective, state:

"Your original response is already clear and effective.
No substantial revision is necessary."

If a revision is useful, keep it very close to the student's
original response.

Correct genuine errors.

Make only necessary changes for clarity or organization.

Add brief development only when the original lack of development
genuinely limits the score.

Do not introduce completely new arguments or ideas.

Do not unnecessarily make the language more sophisticated.

The Better Version should preserve the student's original ideas,
meaning, approximate language level, and personal voice.

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
                    "Evaluate the student's actual response before considering "
                    "any possible improvements. "
                    "Do not invent weaknesses or require unnecessary development. "
                    "When giving a Better Version, stay as close as possible "
                    "to the student's original ideas, meaning, language level, "
                    "and personal voice."
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
