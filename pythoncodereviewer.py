import streamlit as st
import google.generativeai as genai
import os

API_KEY = os.getenv("API_KEY")  #For securing API key so that it is not publicly available

if not API_KEY:
    st.error("API Key not fond. Please set it in your environment variables.")
else:
    genai.configure(api_key=API_KEY)

sys_prompt = """
You are Python code reviewer. Your task is to analyze the given Python code, identify potential bugs, logical errors, and areas of improvement, and suggest fixes.

Your response should be structured as follows:
1. **Issues Detected**: List the errors, inefficiencies, or improvements needed.
2. **Fixed Code**: Provide the corrected version of the code.
3. **Explanation**: Explain why the changes were made in a concise manner.

If the code is already optimal, acknowledge it and suggest best practices.
"""

def code_review(code):
    """Send the user's Python code to the Gemini API for review"""
    model = genai.GenerativeModel("gemini-1.5-pro",system_instruction=sys_prompt)
    user_prompt = f"Review the following Python code and provide feedback on potential bugs, improvements, and fixes:\n\n{code}"

    response = model.generate_content(user_prompt)

    return response.text

# Streamlit UI
st.title("Python Code Reviewer 🔍")

st.write("Submit your Python code for AI-powered review and feedback")

# User input for Python code
code_input = st.text_area("Enter your Python code:", height=200)

if st.button("Review Code"):
    if code_input.strip():
        with st.spinner("Analyzing your code with Google AI..."):
            feedback = code_review(code_input)
        st.subheader("Code Review Report 📋")
        #st.text_area("Review Output", feedback, height=300)
        st.markdown(feedback)
    else:
        st.warning("Please enter some Python code before submitting.")
