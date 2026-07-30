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

IMPORTANT:

Do not require formal academic research or citations.

Students do not need statistical evidence or research unless the
task explicitly asks for it.

Evaluate the quality of the student's explanation and support based
on what is appropriate for the task.

Do not invent additional requirements that are not present in the
task.

Do not automatically require:

- counterarguments
- long-term consequences
- alternative solutions
- multiple examples
- sophisticated analysis
- formal evidence
- complex grammar
- advanced vocabulary

unless these are explicitly required by the task or genuinely
necessary for adequate development.

A student can receive a 4 or 5 using relatively simple language if
the language is accurate, clear, effective, and appropriate.

Do not penalize a student merely because their argument is simple.

Do not penalize a student merely because they did not discuss every
possible perspective.

Do not invent weaknesses in order to justify a lower score.
"""

# ---------------------------------------------------------
# EMAIL RUBRIC
# ---------------------------------------------------------

EMAIL_RUBRIC = """

Evaluate the response as a TOEFL iBT Writing "Write an Email" task.

Consider:

- Does the writer successfully accomplish the purpose of the email?
- Does the writer address the required points in the task?
- Is the message clear and relevant?
- Are ideas sufficiently developed for the task?
- Is the organization appropriate for an email?
- Is the tone appropriate for the intended recipient?
- Is the language generally accurate and effective?
- Does the writer use appropriate vocabulary and sentence structures?

Give ONE overall estimated score from 0 to 5.

Do not give separate numerical scores for grammar, vocabulary,
organization, or task achievement.

Score 5:
The response is highly effective and successfully accomplishes the
purpose of the email. It addresses the required points clearly and
appropriately. Ideas are relevant and sufficiently developed for the
task. The organization and tone are appropriate. Language use is
generally accurate and effective. Minor errors may occur but do not
significantly affect communication.

Score 4:
The response is effective and accomplishes the main purpose of the
email. It addresses the required points and is generally clear and
appropriate. Ideas may be somewhat basic or less fully developed.
The organization and tone are generally appropriate. There may be
some noticeable language errors or limitations, but the message
remains clear and effective overall.

Score 3:
The response generally accomplishes the task and addresses most or
all of the required points, but development may be limited. Ideas may
be basic, repetitive, or insufficiently explained. Language control
is inconsistent, with noticeable grammatical errors, incorrect word
forms, awkward expressions, or sentence structure problems. The main
message is generally understandable.

Score 2:
The response shows limited ability to accomplish the task. One or
more required points may be missing, unclear, or insufficiently
developed. Ideas may be difficult to follow or only partially
relevant. Frequent language errors may significantly affect clarity.

Score 1:
The response demonstrates very limited ability to accomplish the task.
Important parts of the task may be missing or largely irrelevant.
Ideas are severely limited or unclear, and frequent language problems
significantly interfere with communication.

Score 0:
The response is blank, copied from the prompt, completely irrelevant,
not written in English, or does not provide a meaningful response.

IMPORTANT:

Do not give a 4 or 5 simply because the student addresses all task
requirements.

However, do not lower a score simply because the student uses simple
but correct language.

Do not require sophisticated vocabulary or complex grammar for a high
score.

Do not invent weaknesses in order to justify a lower score.
"""

# ---------------------------------------------------------
# STEP 1: EVALUATE WRITING
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

    evaluation_prompt = f"""
You are an experienced TOEFL Writing teacher and evaluator.

Evaluate the student's response accurately, fairly, conservatively,
and consistently.

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
SCORING GUIDELINES
=========================================================

{rubric}

=========================================================
CORE EVALUATION PRINCIPLES
=========================================================

1. SCORE THE ACTUAL STUDENT RESPONSE

Evaluate exactly what the student wrote.

Do not score a hypothetical improved version.

Do not assume what the student intended if the actual writing does
not communicate it.

Do not mentally correct the student's writing before assigning the
score.

=========================================================
2. DO NOT INVENT TASK REQUIREMENTS
=========================================================

Evaluate the actual task prompt.

Do not penalize the student for failing to discuss ideas that the
prompt does not require.

Do not automatically require:

- counterarguments
- long-term consequences
- alternative solutions
- statistical evidence
- formal research
- multiple examples
- sophisticated analysis
- nuanced arguments

unless these are explicitly required by the task or genuinely
necessary to adequately develop the student's response.

For Academic Discussion, students should express and support an
opinion and contribute to the discussion.

They do not need to address every possible argument.

They do not need formal academic evidence.

Do not invent a new standard for a score of 5.

=========================================================
3. DISTINGUISH TASK DEVELOPMENT FROM LANGUAGE ACCURACY
=========================================================

Do not confuse a simple idea with a language error.

A student may have a simple argument and still use accurate English.

Do not lower the score simply because the student does not use
sophisticated vocabulary.

Do not lower the score simply because the student uses simple
grammar if that grammar is accurate and effective.

=========================================================
4. LANGUAGE FEEDBACK MUST IDENTIFY ONLY REAL ERRORS
=========================================================

This is the most important instruction.

A language correction is allowed ONLY if the original contains a
genuine language problem.

A genuine problem includes:

- incorrect grammar
- incorrect subject-verb agreement
- incorrect verb form
- incorrect word form
- incorrect preposition
- incorrect article when it affects accuracy
- incorrect sentence structure
- incorrect word order
- genuinely incorrect vocabulary
- wording that is genuinely unclear or unintelligible

Do NOT correct something merely because:

- another expression sounds more natural
- another expression is more academic
- another expression is more formal
- another expression is more sophisticated
- another expression is more precise
- you personally prefer another expression
- the claim is broad
- the claim is debatable
- the claim is subjective
- the claim may not be universally true

=========================================================
5. DO NOT CHANGE MEANING
=========================================================

NEVER change the student's meaning in Language Feedback.

For example:

"bikes can't be used in winter"

may be a broad claim, but it is grammatically understandable.

This is NOT a language error.

DO NOT change it to:

"bikes can be difficult or dangerous to use in winter."

That changes the meaning and strength of the student's claim.

The student may intentionally be making a strong claim.

Do not weaken or qualify the student's opinion.

Similarly, do not change:

"bikes"

to:

"bicycles"

unless "bikes" is genuinely incorrect.

Do not change:

"think"

to:

"believe"

unless "think" is genuinely incorrect.

Do not change:

"says"

to:

"argues"

unless "says" is genuinely incorrect.

Do not change:

"help"

to:

"assist"

unless "help" is genuinely incorrect.

Simple and common language is acceptable.

=========================================================
6. THREE-WAY LANGUAGE CLASSIFICATION
=========================================================

For every possible language issue you consider, classify it internally
as exactly one of the following:

REAL_ERROR

The original contains a genuine language error that should be
corrected.

NO_ERROR

The original is correct and should remain unchanged.

STYLE_ONLY

The original may be less natural, less formal, less sophisticated,
or stylistically improvable, but it is not a genuine error.

ONLY REAL_ERROR ITEMS MAY APPEAR IN LANGUAGE FEEDBACK.

Do NOT include NO_ERROR items.

Do NOT include STYLE_ONLY items.

Do NOT write:

"Phrase → No correction needed."

Do not include correct phrases in Language Feedback.

=========================================================
7. EXAMPLES OF WHAT NOT TO CORRECT
=========================================================

Do NOT correct:

"I think that investing in buses and trains should be a priority."

Do NOT change it to:

"I believe that investing in buses and trains should be a priority."

Reason:
"I think" is correct.

Do NOT correct:

"I agree with Marcus's argument when he says..."

Do NOT change it to:

"I agree with Marcus's argument that..."

Reason:
The original structure is grammatically acceptable.

Do NOT correct:

"bikes can't be used in winter"

to:

"bikes can be difficult or dangerous to use in winter."

Reason:
This changes meaning.

Do NOT correct:

"bikes"

to:

"bicycles"

Reason:
"Bikes" is correct.

Do NOT correct:

"help"

to:

"assist"

Reason:
"Help" is correct.

=========================================================
8. MAXIMUM LANGUAGE CORRECTIONS
=========================================================

Give a maximum of 6 REAL_ERROR corrections.

Prioritize the most important errors.

If there are only 2 genuine errors, give only 2 corrections.

If there are no genuine errors, write exactly:

No major language errors.

Never invent errors to reach 6.

=========================================================
9. CORRECTION FORMAT
=========================================================

For every REAL_ERROR, use exactly:

**Original phrase** → **Correction**

Brief explanation: [short explanation]

The correction must preserve the student's original meaning.

Do not change the strength of the student's claim.

Do not add information.

Do not remove information.

=========================================================
10. BETTER VERSION
=========================================================

Do NOT create a Better Version in this step.

The Better Version will be created separately using ONLY the approved
REAL_ERROR corrections.

=========================================================
11. SCORE CONSISTENCY
=========================================================

Consider:

- task fulfillment
- relevance
- development
- organization
- language control
- clarity
- appropriateness of tone

Do not automatically give a 4 or 5 because all task requirements
are addressed.

Do not automatically give a 3 because ideas are simple.

Do not invent weaknesses.

Do not require advanced vocabulary or complex grammar for a high score.

=========================================================
12. REQUIRED OUTPUT
=========================================================

Return ONLY these five sections:

## Estimated Score: X/5

## Why Not the Next Score?

## What You Did Well

## What to Improve

## Language Feedback

Do not include:

- Better Version
- additional comments
- model answers
- alternative rewrites
- corrections that are not REAL_ERROR items

=========================================================
SECTION REQUIREMENTS
=========================================================

## Estimated Score: X/5

Give ONE estimated score from 0 to 5.

=========================================================

## Why Not the Next Score?

Explain briefly why the response did not receive the next higher score.

Write 2-4 concise sentences.

The explanation must be consistent with the actual score.

Do not invent weaknesses.

Do not automatically mention:

- sophisticated vocabulary
- complex grammar
- nuanced arguments
- counterarguments
- long-term consequences

unless they are genuinely relevant to the actual response and task.

=========================================================

## What You Did Well

Give exactly 2 specific strengths.

Use bullet points.

Base both strengths on the student's actual response.

Do not give generic praise.

=========================================================

## What to Improve

Give exactly 2 specific and actionable suggestions.

Use bullet points.

Focus on the two most important improvements.

Do not automatically recommend advanced vocabulary.

Do not automatically recommend complex grammar.

Do not invent missing weaknesses.

=========================================================

## Language Feedback

Include ONLY genuine REAL_ERROR corrections.

Maximum 6.

Use:

**Original phrase** → **Correction**

Brief explanation: [short explanation]

If there are no genuine language errors, write exactly:

No major language errors.

Do not include:

- correct phrases
- stylistic alternatives
- optional improvements
- meaning changes
- factual corrections
- broad claims that are grammatically correct
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful, fair, conservative TOEFL "
                    "Writing evaluator. "
                    "Evaluate the student's actual writing. "
                    "Never change the student's meaning. "
                    "Never weaken or qualify the student's claims. "
                    "Distinguish REAL_ERROR from STYLE_ONLY and NO_ERROR. "
                    "Only genuine language errors may appear in Language "
                    "Feedback. "
                    "Do not include correct phrases as corrections. "
                    "Do not invent task requirements. "
                    "Do not require sophisticated vocabulary or complex "
                    "grammar for high scores. "
                    "Do not create a Better Version."
                )
            },
            {
                "role": "user",
                "content": evaluation_prompt
            }
        ],
        temperature=0.0,
        max_tokens=1800
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# STEP 2: EXTRACT ONLY APPROVED CORRECTIONS
# ---------------------------------------------------------

def extract_corrections(language_feedback):

    if not language_feedback:
        return []

    if "No major language errors." in language_feedback:
        return []

    corrections = []

    lines = language_feedback.splitlines()

    for i, line in enumerate(lines):

        if "→" not in line:
            continue

        clean_line = re.sub(
            r"\*\*",
            "",
            line
        ).strip()

        parts = clean_line.split("→", 1)

        if len(parts) != 2:
            continue

        original = parts[0].strip()
        correction = parts[1].strip()

        if not original or not correction:
            continue

        # Remove accidental labels
        original = re.sub(
            r"^(Original phrase:|Original:)\s*",
            "",
            original,
            flags=re.IGNORECASE
        ).strip()

        correction = re.sub(
            r"^(Correction:)\s*",
            "",
            correction,
            flags=re.IGNORECASE
        ).strip()

        # Ignore explicit "no correction" entries
        if correction.lower() in [
            "no correction needed",
            "no change needed",
            "no correction",
            "keep as is"
        ]:
            continue

        corrections.append(
            {
                "original": original,
                "correction": correction
            }
        )

    return corrections[:6]


# ---------------------------------------------------------
# STEP 3: STRICT MINIMAL-DIFF EDITOR
# ---------------------------------------------------------

def create_better_version(
    student_response,
    corrections
):

    if not corrections:
        return student_response

    correction_list = ""

    for index, item in enumerate(corrections, start=1):

        correction_list += (
            f"\nCORRECTION {index}:\n"
            f'Original exact phrase: "{item["original"]}"\n'
            f'Approved replacement: "{item["correction"]}"\n'
        )

    editing_prompt = f"""
You are a STRICT MINIMAL-DIFF editor.

Your ONLY task is to apply the explicitly approved language
corrections to the student's original response.

You are NOT evaluating the writing.

You are NOT improving the writing.

You are NOT rewriting the writing.

You are NOT making the student sound more academic.

You are NOT making the student sound more sophisticated.

You are NOT adding information.

You are ONLY applying the approved corrections.

=========================================================
STUDENT ORIGINAL RESPONSE
=========================================================

{student_response}

=========================================================
APPROVED CORRECTIONS
=========================================================

{correction_list}

=========================================================
ABSOLUTE RULES
=========================================================

RULE 1:

The student's original response is the source of truth.

Start with the original response.

RULE 2:

Apply ONLY the approved corrections listed above.

No other changes are allowed.

RULE 3:

Every change in your output must correspond directly to one of the
approved corrections.

RULE 4:

Do NOT add:

- ideas
- arguments
- examples
- explanations
- evidence
- supporting details
- conclusions
- transitions
- sentences

RULE 5:

Do NOT remove any information.

RULE 6:

Do NOT change the student's meaning.

RULE 7:

Do NOT weaken or strengthen the student's claims.

For example, do NOT change:

"bikes can't be used in winter"

to:

"bikes can be difficult or dangerous to use in winter."

That is forbidden because it changes meaning.

RULE 8:

Do NOT replace correct words with synonyms.

Do NOT change:

"think" to "believe"

"bikes" to "bicycles"

"says" to "argues"

"help" to "assist"

unless that exact change appears in the approved corrections.

RULE 9:

Do NOT change correct grammar.

RULE 10:

Do NOT add transitions such as:

"however"

"therefore"

"in addition"

"as a result"

"for this reason"

unless they already appear in the student's original response or are
explicitly included in an approved correction.

RULE 11:

Do NOT restructure sentences.

Only replace the exact approved phrase with its approved replacement.

RULE 12:

Do NOT make punctuation changes unless punctuation is included in an
approved correction.

RULE 13:

If an approved correction cannot be found exactly in the original,
do NOT invent a replacement.

Leave that part unchanged.

RULE 14:

If there are no approved corrections, return the student's original
response exactly as written.

=========================================================
FINAL CHECK
=========================================================

Before returning the response, compare it with the original.

Every difference must be explained by one of the approved corrections.

If you made any other change, undo it.

=========================================================
OUTPUT
=========================================================

Return ONLY the corrected student response.

Do not include:

- headings
- explanations
- comments
- quotation marks
- bullet points
- "Better Version"
- introductory text
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict minimal-diff editor. "
                    "Apply only the explicitly approved corrections. "
                    "Do not rewrite. "
                    "Do not add information. "
                    "Do not add arguments. "
                    "Do not add examples. "
                    "Do not add transitions. "
                    "Do not change meaning. "
                    "Do not replace correct words with synonyms. "
                    "Every change must correspond to an approved "
                    "correction. "
                    "Return only the corrected response."
                )
            },
            {
                "role": "user",
                "content": editing_prompt
            }
        ],
        temperature=0.0,
        max_tokens=1800
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# STEP 4: SAFETY CHECK
# ---------------------------------------------------------

def verify_minimal_edit(
    original,
    edited,
    corrections
):

    if not corrections:
        return original

    # If the AI accidentally returns formatting or commentary,
    # remove common unwanted elements.
    edited = edited.strip()

    edited = re.sub(
        r"^Better Version:\s*",
        "",
        edited,
        flags=re.IGNORECASE
    )

    edited = re.sub(
        r"^##\s*Better Version\s*",
        "",
        edited,
        flags=re.IGNORECASE
    )

    # If the edited version is empty, use original.
    if not edited:
        return original

    return edited.strip()


# ---------------------------------------------------------
# FORMAT EVALUATION FOR DISPLAY
# ---------------------------------------------------------

def format_evaluation(
    evaluation,
    better_version
):

    # Remove accidental Better Version section
    evaluation = re.split(
        r"##\s*Better Version",
        evaluation,
        flags=re.IGNORECASE
    )[0].strip()

    lines = evaluation.split("\n")

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

        else:

            processed_lines.append(
                line
            )

    formatted_evaluation = "\n".join(
        processed_lines
    )

    # -----------------------------------------------------
    # BOLD TEXT
    # -----------------------------------------------------

    formatted_evaluation = re.sub(
        r"\*\*(.*?)\*\*",
        r"<strong>\1</strong>",
        formatted_evaluation
    )

    # -----------------------------------------------------
    # BULLET POINTS
    # -----------------------------------------------------

    formatted_evaluation = re.sub(
        r"(?m)^\s*-\s+(.*)$",
        r"<li>\1</li>",
        formatted_evaluation
    )

    formatted_evaluation = re.sub(
        r"((?:<li>.*?</li>\s*)+)",
        r"<ul>\1</ul>",
        formatted_evaluation
    )

    # -----------------------------------------------------
    # SPACING
    # -----------------------------------------------------

    formatted_evaluation = formatted_evaluation.replace(
        "\n\n",
        "<br>"
    )

    formatted_evaluation = formatted_evaluation.replace(
        "\n",
        "<br>"
    )

    # Remove breaks around headings

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

    # Remove breaks around lists

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

    # -----------------------------------------------------
    # BETTER VERSION
    # -----------------------------------------------------

    better_version_html = (
        "<h2>Better Version</h2>"
        "<div class='better-version'>"
        + better_version.replace("\n", "<br>")
        + "</div>"
    )

    formatted_evaluation = (
        formatted_evaluation
        + better_version_html
    )

    return formatted_evaluation


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

                # -------------------------------------------------
                # STEP 1
                # EVALUATE RESPONSE
                # -------------------------------------------------

                evaluation = evaluate_writing(
                    task_type,
                    task_prompt,
                    student_response
                )

                # -------------------------------------------------
                # STEP 2
                # EXTRACT LANGUAGE FEEDBACK
                # -------------------------------------------------

                language_feedback_match = re.search(
                    r"##\s*Language Feedback\s*(.*)",
                    evaluation,
                    flags=re.IGNORECASE | re.DOTALL
                )

                if language_feedback_match:

                    language_feedback = (
                        language_feedback_match
                        .group(1)
                        .strip()
                    )

                else:

                    language_feedback = (
                        "No major language errors."
                    )

                # -------------------------------------------------
                # STEP 3
                # EXTRACT ONLY APPROVED CORRECTIONS
                # -------------------------------------------------

                approved_corrections = (
                    extract_corrections(
                        language_feedback
                    )
                )

                # -------------------------------------------------
                # STEP 4
                # CREATE MINIMAL-DIFF VERSION
                # -------------------------------------------------

                better_version = (
                    create_better_version(
                        student_response,
                        approved_corrections
                    )
                )

                # -------------------------------------------------
                # STEP 5
                # FINAL SAFETY CHECK
                # -------------------------------------------------

                better_version = (
                    verify_minimal_edit(
                        student_response,
                        better_version,
                        approved_corrections
                    )
                )

                # -------------------------------------------------
                # STEP 6
                # FORMAT EVERYTHING
                # -------------------------------------------------

                formatted_evaluation = (
                    format_evaluation(
                        evaluation,
                        better_version
                    )
                )

                # -------------------------------------------------
                # DISPLAY
                # -------------------------------------------------

                st.success(
                    "Evaluation complete!"
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
