import streamlit as st

# Page configuration
st.set_page_config(
    page_title="TOEFL Writing AI Grader",
    page_icon="📝",
    layout="centered"
)

# Title
st.title("📝 TOEFL Writing AI Grader")

st.write(
    "Practice your TOEFL Writing skills and receive AI-powered "
    "feedback based on the official ETS scoring guides."
)

st.info(
    "This tool provides an AI-estimated practice score. "
    "It is not an official ETS score."
)

# Task selection
task_type = st.selectbox(
    "Choose your TOEFL Writing task:",
    [
        "Write an Email",
        "Write for an Academic Discussion"
    ]
)

# Task prompt
st.subheader("TOEFL Task")

task_prompt = st.text_area(
    "Paste the TOEFL task or prompt here:",
    height=200,
    placeholder="Paste the complete TOEFL task here..."
)

# Student response
st.subheader("Your Response")

student_response = st.text_area(
    "Paste your response here:",
    height=300,
    placeholder="Paste your TOEFL writing response here..."
)

# Evaluate button
if st.button("🔍 Evaluate My Writing", type="primary"):

    if not task_prompt.strip():
        st.warning("Please enter the TOEFL task or prompt.")

    elif not student_response.strip():
        st.warning("Please enter your writing response.")

    else:
        st.success(
            "Your response is ready to be evaluated!"
        )

        st.write("### Selected Task")
        st.write(task_type)

        st.write("### Your Response")
        st.write(student_response)

        st.info(
            "The AI evaluation system will be connected in the next step."
        )
