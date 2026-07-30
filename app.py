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
    /* Justified feedback text */
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

    /* Language corrections */
    .correction {
        margin-bottom: 10px;
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

    # ---------------------------------------------------------
    # ACADEMIC DISCUSSION RUBRIC
    # ---------------------------------------------------------

    if task_type == "Write for an Academic Discussion":

        rubric = """
Evaluate the response using the TOEFL iBT Writing for an Academic
Discussion scoring scale from 0 to 5.

The score must reflect the overall effectiveness of the student's
actual response.

Evaluate these four broad dimensions together:

1. TASK FULFILLMENT
- Does the student answer the professor's question?
- Is the student's position clear?
- Does the student make a meaningful contribution in their own words?
- Does the student engage with the ideas presented by other participants
  when appropriate?

2. DEVELOPMENT AND SUPPORT
- Does the student explain their reasons?
- Does the student provide relevant examples or details when useful?
- Does the student explain why or how their ideas support their position?
- Does the student develop ideas rather than simply repeat the same claim?

3. ORGANIZATION AND COHERENCE
- Are the ideas logically connected?
- Is there a clear progression of ideas?
- Are transitions used effectively when needed?
- Is the response easy to follow?

4. LANGUAGE CONTROL
- Is the grammar generally accurate?
- Are vocabulary and word choices appropriate?
- Are sentence structures clear?
- Do errors interfere with meaning or clarity?
- Is the language natural enough for effective communication?

Do NOT assign separate numerical scores for these categories.
Give ONE overall score from 0 to 5.

SCORE 5:
The response is highly effective. It clearly and fully contributes to
the discussion, presents a clear position, and develops relevant ideas
with effective explanations and/or examples. The response is well
organized and coherent. Language use is accurate and effective, with
few or no errors that affect clarity. Minor imperfections are possible
but do not significantly limit the effectiveness of the response.

SCORE 4:
The response is effective and clearly contributes to the discussion.
The student's position is clear, and the response provides relevant
support and development. The student may engage effectively with other
participants' ideas. The response is generally organized and coherent.
There may be some genuine language errors, awkward expressions, or
minor limitations in development or precision, but the overall message
is clear and effective.

SCORE 3:
The response is generally relevant and understandable but has noticeable
limitations in development, explanation, support, organization, or
language control. The student may express a clear position but develop
it only partially. Ideas may be somewhat basic, repetitive, or
insufficiently explained. Language errors or awkward expressions may
sometimes affect clarity, although the main meaning is generally
understandable.

SCORE 2:
The response shows limited ability to contribute meaningfully to the
discussion. Ideas may be unclear, repetitive, insufficiently developed,
or only partially relevant. The response may have significant problems
with organization or language control. Errors may frequently interfere
with clarity or communication.

SCORE 1:
The response provides very little relevant content or does not
meaningfully contribute to the discussion. Ideas are severely limited,
unclear, or largely irrelevant. Frequent language problems significantly
interfere with communication.

SCORE 0:
The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.

IMPORTANT SCORE PRINCIPLES:

- A response does NOT need sophisticated vocabulary or complex grammar
  to receive a 4 or 5.
- Simple language can receive a high score if it is accurate, clear,
  effective, and appropriate.
- Addressing every task requirement does NOT automatically justify a
  4 or 5.
- At the same time, do NOT lower a score simply because the student's
  ideas are simple if they are clearly explained and effectively
  supported.
- Do not count grammar errors mechanically. Consider their frequency,
  seriousness, and effect on clarity.
- A few minor errors should not automatically prevent a 5.
- Several genuine errors that affect clarity or language control should
  be considered when assigning the score.
- Development is about explaining and supporting ideas, not about using
  formal academic research or citations.
"""

    # ---------------------------------------------------------
    # EMAIL RUBRIC
    # ---------------------------------------------------------

    else:

        rubric = """
Evaluate the response as a TOEFL iBT Writing "Write an Email" task.

Evaluate these broad dimensions together:

1. TASK FULFILLMENT
- Does the writer accomplish the purpose of the email?
- Does the writer address the required points?
- Does the writer respond appropriately to the situation?

2. DEVELOPMENT AND CLARITY
- Are the relevant ideas sufficiently explained?
- Is the message clear and complete for the purpose?
- Are important details included when required?

3. ORGANIZATION AND COHERENCE
- Is the message logically organized?
- Are ideas connected clearly?
- Is the organization appropriate for an email?

4. TONE AND APPROPRIATENESS
- Is the tone appropriate for the intended recipient?
- Is the level of formality suitable for the situation?

5. LANGUAGE CONTROL
- Is the grammar generally accurate?
- Are vocabulary and word choices appropriate?
- Are sentence structures clear?
- Do errors affect communication?

Give ONE overall estimated score from 0 to 5.

SCORE 5:
The response is highly effective and successfully accomplishes the
purpose of the email. It addresses the required points clearly and
appropriately. Ideas are relevant and sufficiently developed. The
organization and tone are appropriate. Language use is accurate and
effective. Minor imperfections may occur but do not significantly
affect communication.

SCORE 4:
The response is effective and accomplishes the main purpose of the
email. It addresses the required points and is generally clear and
appropriate. Ideas may be somewhat basic or less fully developed.
The organization and tone are generally appropriate. There may be some
noticeable genuine language errors or limitations, but the message
remains clear and effective overall.

SCORE 3:
The response generally accomplishes the task but may have limitations
in development, clarity, organization, tone, or language control.
Ideas may be basic, repetitive, or insufficiently explained. Noticeable
grammar errors, incorrect word forms, awkward expressions, or sentence
structure problems may sometimes affect clarity.

SCORE 2:
The response shows limited ability to accomplish the task. One or more
required points may be missing, unclear, or insufficiently developed.
Ideas may be difficult to follow. Frequent language errors or limited
language control may significantly affect clarity and communication.

SCORE 1:
The response demonstrates very limited ability to accomplish the task.
Important parts may be missing or largely irrelevant. Ideas are severely
limited or unclear, and frequent language problems significantly
interfere with communication.

SCORE 0:
The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.

IMPORTANT SCORE PRINCIPLES:

- Completing all task requirements does NOT automatically justify a
  4 or 5.
- However, simple but accurate English should not be penalized.
- Do not require sophisticated vocabulary or complex grammar for a high
  score.
- Consider the frequency, seriousness, and effect of genuine language
  errors on communication.
- Do not lower the score simply because the student's writing could be
  expressed in a more formal or sophisticated way.
"""

    # ---------------------------------------------------------
    # MAIN EVALUATION PROMPT
    # ---------------------------------------------------------

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher, evaluator, and language
feedback specialist.

Your job is to evaluate a student's response accurately, fairly,
consistently, and pedagogically.

You must evaluate the student's ACTUAL WRITING.

Do not evaluate what the student might have meant if the actual wording
does not communicate that meaning clearly.

At the same time, when providing language corrections, use the context
of the entire response to determine the student's likely intended
meaning.

TASK TYPE:
{task_type}

TASK PROMPT:
{task_prompt}

STUDENT RESPONSE:
{student_response}

SCORING GUIDELINES:
{rubric}


=========================================================
PART 1: EVALUATE THE STUDENT'S ACTUAL RESPONSE
=========================================================

First, internally evaluate the response based on:

- task fulfillment
- relevance
- development and support
- organization and coherence
- language control
- clarity
- appropriateness of tone when relevant

Do not show this internal analysis.

Then assign ONE overall score from 0 to 5.

The score must reflect the student's actual writing as submitted.

Do not mentally rewrite the student's response before scoring it.

Do not give credit for ideas that are not actually expressed.

Do not assume the student knows a grammar rule if the actual response
shows a genuine error.

However, do not penalize the student simply for using simple, accurate
language.


=========================================================
PART 2: DEVELOPMENT MUST BE EVALUATED SPECIFICALLY
=========================================================

When evaluating development, ask:

- Does the student give reasons for their position?
- Does the student explain those reasons?
- Does the student provide relevant examples or details?
- Does the student explain why or how the examples support the argument?
- Does the student repeat the same point without adding new information?

Do NOT say only:

"The response needs more detail."

Instead, identify exactly what is missing.

For example:

WEAK FEEDBACK:
"The ideas could be more developed."

BETTER FEEDBACK:
"The response gives two reasons for investing in public transportation,
but the second reason is only briefly mentioned. The writer could explain
why the limitation of bicycles makes buses and trains a more effective
option."

Development does NOT require formal research, citations, statistics,
or academic evidence unless the task specifically asks for them.

For Academic Discussion, relevant explanations, examples, personal
observations, or logical reasoning can effectively support an idea.


=========================================================
PART 3: DO NOT CONFUSE STYLE WITH ERROR
=========================================================

This is one of the most important rules.

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
enough for the context, and appropriate for the task, LEAVE IT ALONE.

For example:

"I think that investing in buses and trains should be a priority."

This is correct.

Do NOT change it to:

"I believe that investing in buses and trains should be a priority."

The second version is only a stylistic alternative.

Do NOT present "think → believe" as a correction.

Similarly:

"can't" → "cannot"

This is generally a register preference, not a genuine error.

Do NOT list it as a language error unless the task specifically requires
a particular level of formality and the original form is genuinely
inappropriate.

Simple language is NOT automatically weak language.


=========================================================
PART 4: IDENTIFY REAL LANGUAGE PROBLEMS
=========================================================

Language feedback should focus on genuine and useful problems such as:

- grammatical errors
- subject-verb agreement
- incorrect verb forms
- incorrect word forms
- incorrect prepositions
- incorrect articles when they affect accuracy
- incorrect sentence structures
- incorrect word order
- unclear pronoun reference
- incorrect or misleading word choice
- incorrect collocations
- expressions that are genuinely unnatural or confusing
- spelling errors
- punctuation problems that affect readability
- wording that makes the intended meaning unclear

Do NOT include a language correction simply because a different version
sounds more polished.


=========================================================
PART 5: DISTINGUISH ERRORS FROM AWKWARD LANGUAGE
=========================================================

Not every imperfect sentence is completely wrong.

Use these distinctions:

A. GENUINE ERROR

Example:

"They enjoy read books."

Correction:

"They enjoy reading books."

Explanation:

"Enjoy" is followed by a gerund (-ing form), not the base form.

B. AWKWARD BUT UNDERSTANDABLE

Example:

"My siblings like very much the reading program."

Correction:

"My siblings really like the reading program."

Explanation:

The meaning is clear, but the word order is awkward. The correction
expresses the same idea more naturally.

C. CORRECT BUT STYLISTICALLY DIFFERENT

Example:

"I think that investing in buses and trains should be a priority."

Do NOT correct this.

Do NOT replace "think" with "believe" and call it an error.

D. INCORRECT OR UNNATURAL COLLOCATION

Example:

"constructing more transports"

Possible correction:

"expanding public transportation"

Explanation:

"Transportation" is not normally something that is "constructed."
The intended meaning is to expand or improve public transportation
systems or infrastructure.

E. UNCLEAR MEANING

If the student's wording is unclear, use the surrounding context to
infer the most likely intended meaning.

Do NOT make a grammatically correct correction that changes the
student's intended meaning.


=========================================================
PART 6: MEANING PRESERVATION
=========================================================

ALWAYS preserve the student's intended meaning when correcting language.

Before correcting a sentence:

1. Read the entire sentence.
2. Read the surrounding paragraph.
3. Determine what the student is most likely trying to communicate.
4. Correct the language while preserving that meaning.

Do NOT simply replace individual words without considering context.

Example:

Student:
"environment change could be beneficial for the earth."

Do NOT automatically change this to:

"environmental change could be beneficial for the earth."

That changes or potentially distorts the student's intended meaning.

If the surrounding context shows that the student means that people's
actions can positively affect the environment, a better correction is:

"people's actions can have a positive impact on the environment."

The goal is to communicate the student's intended idea accurately,
not merely to produce a grammatically improved sentence.


=========================================================
PART 7: CONTEXTUAL CORRECTION
=========================================================

Do not correct sentences word-by-word in isolation.

Consider the complete meaning.

Example:

"This option is also cheaper than constructing more transports."

Do NOT simply change:

"transports" → "transportation"

The resulting sentence:

"This option is also cheaper than constructing more transportation."

is still unnatural and does not solve the problem.

A contextually appropriate correction may be:

"This option is also cheaper than expanding public transportation."

The correction must address the actual language problem in context.


=========================================================
PART 8: DO NOT INVENT PROBLEMS
=========================================================

Base all feedback on the student's actual response.

Do not invent:

- grammatical errors
- vocabulary errors
- missing information
- organizational problems
- development problems

Do not criticize a sentence that is correct.

Do not assume that a sentence is wrong simply because you would write
it differently.

If there are only two genuine language problems, give two corrections.

Do not invent additional corrections to fill space.


=========================================================
PART 9: LANGUAGE FEEDBACK LIMIT
=========================================================

Give a MAXIMUM of 6 language corrections.

Give fewer if appropriate.

Prioritize:

1. Errors that affect meaning.
2. Errors that significantly affect clarity.
3. Repeated grammar problems.
4. Important vocabulary or collocation problems.
5. Sentence structure problems.
6. Errors that are especially useful for the student to learn from.

Do NOT prioritize minor stylistic preferences.

Do NOT correct every minor punctuation issue.

Do NOT list "think → believe" as a correction.

Do NOT list "can't → cannot" as a correction unless the original is
inappropriate for the specific task.

If there are no meaningful language problems, write:

"No major language errors."


=========================================================
PART 10: CORRECTION FORMAT
=========================================================

Use this format:

**Original phrase** → **Correction**

Brief explanation: [short explanation]

Examples:

**They enjoy read books.** → **They enjoy reading books.**

Brief explanation: After "enjoy," use the -ing form of the verb.

---

**listen stories** → **listen to stories**

Brief explanation: The verb "listen" is followed by the preposition
"to."

---

**My younger sister like the stories.** → **My younger sister likes
the stories.**

Brief explanation: The singular subject "my younger sister" requires
the third-person singular form "likes."

---

**during a rain** → **in the rain**

Brief explanation: "In the rain" is the natural expression for
describing an activity that takes place while it is raining.

---

**constructing more transports** → **expanding public transportation**

Brief explanation: "Constructing more transportation" is not a natural
collocation. "Expanding public transportation" more accurately expresses
the intended meaning.

If the original is understandable but awkward, explicitly say:

"The original is understandable but awkward..."

Do not call something a grammatical error if the main issue is
naturalness or word choice.


=========================================================
PART 11: BETTER VERSION
=========================================================

The Better Version is a lightly improved version of the student's own
response.

It is NOT a new model answer.

It must:

- preserve the student's position
- preserve the student's main ideas
- preserve the student's intended meaning
- preserve the student's personal voice
- stay reasonably close to the student's language level
- correct genuine grammar errors
- correct inaccurate or confusing word choices
- improve clarity where necessary
- improve organization only when genuinely necessary

DO NOT:

- invent new arguments
- invent new evidence
- invent statistics
- invent examples
- add completely new reasons
- introduce information not present in the student's response
- substantially change the student's argument
- transform a B1/B2 response into artificial C1/C2 English
- replace simple correct language with unnecessarily sophisticated
  vocabulary

The Better Version should show the student how THEIR OWN response
could be improved.

For example, if the student writes:

"I think that investing in buses and trains should be a priority."

KEEP THIS SENTENCE.

Do NOT automatically change it to:

"I firmly believe that prioritizing investment in integrated public
transportation infrastructure represents a strategically advantageous
approach."

That would not be an appropriate correction.

If the student writes:

"My younger sister like the stories, but sometimes the stories are
too fast and she don't understand everything."

A suitable improvement is:

"My younger sister likes the stories, but sometimes the stories are
read too quickly, and she doesn't understand everything."

This preserves the student's meaning and voice.

If the student's response lacks development, do NOT automatically add
a completely new argument.

Instead, improve the explanation of an existing idea when possible.

For example, if the student already says that bikes are difficult to
use in the rain, the Better Version may clarify that idea:

"it can be dangerous to ride a bike in the rain because the pavement
is wet and slippery."

Do NOT add a completely new argument such as:

"Public transportation is also more accessible to people who live far
from the city center."

unless the student already expressed that idea.

The Better Version must remain recognizably the student's response.


=========================================================
PART 12: BETTER VERSION MUST REFLECT THE SCORE
=========================================================

For a score 1 or 2:

- Correct the most important problems.
- Keep the language relatively simple.
- Do not transform the response into an advanced model answer.

For a score 3:

- Correct genuine errors.
- Improve clarity.
- Make limited improvements to development only when they can be made
  using the student's existing ideas.

For a score 4:

- Make necessary language corrections.
- Make only minor improvements to clarity, precision, and development.
- Do not substantially rewrite the response.

For a score 5:

- Make minimal corrections.
- If the response is already effective, preserve it almost entirely.

The Better Version should never make a score 3 response look like a
perfect 5/5 response through extensive rewriting.


=========================================================
PART 13: "WHY NOT THE NEXT SCORE?" RULES
=========================================================

The "Why Not the Next Score?" section must explain the MAIN reasons the
response did not receive the next higher score.

Do NOT use vague or generic statements.

WEAK:

"The response could provide more detail."

BETTER:

"The response gives relevant reasons for investing in public
transportation, but one of the main arguments is only briefly explained.
The writer could further explain why the limitations of bicycles make
buses and trains a more effective investment."

For a 4/5 response, explain what prevents a 5.

For a 3/5 response, explain what prevents a 4.

For a 2/5 response, explain what prevents a 3.

For a 1/5 response, explain what prevents a 2.

For a 5/5 response, write:

"The response demonstrates the characteristics of the highest score
level. There are no significant limitations that prevent it from
receiving a 5/5."

The explanation should normally be 2-4 concise sentences.

Mention language problems only when they are genuinely relevant to the
score.

Do not say that a response is not a 5 simply because it uses simple
language.


=========================================================
PART 14: QUALITY CONTROL BEFORE FINAL RESPONSE
=========================================================

Before producing the final answer, silently check your evaluation.

Ask yourself:

1. Did I identify any correct sentence as an error?
2. Did I change a word only because I prefer a more formal synonym?
3. Did I incorrectly treat a stylistic preference as a grammar error?
4. Did I preserve the student's intended meaning?
5. Did I consider the context before correcting language?
6. Did I identify the student's most important actual language problems?
7. Did I distinguish language problems from development problems?
8. Did I explain specifically why the response received this score?
9. Did I give the correct score based on the whole response rather than
   simply counting errors?
10. Did I add new arguments or evidence to the Better Version?
11. Does the Better Version remain close to the student's original
    voice and language level?
12. Did I avoid inventing problems?
13. Did I avoid overcorrecting?
14. Did I avoid requiring sophisticated vocabulary or complex grammar
    when the student's language is already accurate?
15. Does the feedback provide useful information the student can apply
    to future TOEFL writing?

If any answer indicates a problem, revise the feedback internally before
producing the final response.


=========================================================
PART 15: MANDATORY OUTPUT FORMAT
=========================================================

Return ONLY the following six sections, in exactly this order:

## Estimated Score: X/5

## Why Not the Next Score?

## What You Did Well

## What to Improve

## Language Feedback

## Better Version

FORMATTING RULES:

Every section heading MUST begin with exactly two hash symbols
followed by a space.

Every heading MUST appear on its own separate line.

Leave one blank line between the heading and its content.

Leave one blank line between sections.

Do not remove the ## symbols.

Do not put all text in bold.

Use bold only where useful, especially for Original and Correction
portions of Language Feedback.

Use bullet points for the two strengths.

Use bullet points for the two improvement suggestions.

Do not create additional sections.

Do not create a section called "Why?"

Do not create a section called "Language Corrections."

Use exactly "Language Feedback."

Do not create an "Additional Comments" section.

Do not add any text before the first section.

Do not add any text after the Better Version.


=========================================================
PART 16: SECTION CONTENT
=========================================================

## Estimated Score: X/5

Give ONE overall estimated score from 0 to 5.

Do not add explanatory text on the same line as the score.


## Why Not the Next Score?

Give 2-4 concise sentences.

Explain the specific limitations preventing the next score.

Do not give generic feedback.


## What You Did Well

Give EXACTLY 2 specific strengths.

Use bullet points.

Base both strengths on the student's actual response.

Do not give generic praise.

Do not add a third strength.


## What to Improve

Give EXACTLY 2 specific and actionable suggestions.

Use bullet points.

Focus on the two most important improvements for the student's
performance.

For lower scores, prioritize:

- task completion
- clarity
- accuracy
- basic development

For mid-level scores, prioritize:

- language control
- development
- organization

For higher scores, prioritize:

- precision
- fuller development
- nuanced support

ONLY recommend more advanced vocabulary or complex grammar when this is
genuinely necessary.


## Language Feedback

Give a maximum of 6 genuine and useful corrections.

Do not invent corrections.

Do not include stylistic alternatives as errors.

If the original is understandable but awkward, explicitly say so.

If there are no meaningful problems, write:

"No major language errors."


## Better Version

Provide a lightly improved version of the student's response.

Keep it close to the original.

Correct genuine errors.

Improve clarity where necessary.

Do not introduce new arguments.

Do not introduce new information.

Do not substantially rewrite the response.

Do not make the response significantly more sophisticated than the
original.

The Better Version must be the final content.

Do not add an explanation after it.
"""

    # ---------------------------------------------------------
    # API CALL
    # ---------------------------------------------------------

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful, fair, and highly precise TOEFL "
                    "Writing evaluator and language teacher. "
                    "Evaluate the student's actual writing. "
                    "Distinguish genuine language errors from stylistic "
                    "preferences. "
                    "Preserve the student's intended meaning when "
                    "correcting language. "
                    "Consider context before making corrections. "
                    "Do not overcorrect. "
                    "Do not invent errors or information. "
                    "Do not add new arguments to the Better Version. "
                    "Score consistently across score bands. "
                    "Follow every instruction in the evaluation prompt. "
                    "Return only the six required sections in the exact "
                    "Markdown format requested. "
                    "Every ## heading must appear on its own line."
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

                # -------------------------------------------------
                # FORMAT AI RESPONSE FOR DISPLAY
                # -------------------------------------------------

                formatted_evaluation = evaluation

                lines = formatted_evaluation.split("\n")

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

                # Wrap consecutive list items
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

                # Remove unnecessary breaks directly around headings
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

                # Remove unnecessary breaks around lists
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
