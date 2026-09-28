import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="EduGenie - AI Learning Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduGenie: AI-Powered Learning Assistant")
st.subheader("Summarize Study Notes & Generate Practice Quizzes")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get a free API key at: aistudio.google.com")

st.header("📚 Enter Your Study Content")
user_text = st.text_area(
    "Paste your study notes, textbook excerpt, or topic summary below:",
    height=200,
    placeholder="Paste your course notes or syllabus topic here..."
)

task_option = st.radio(
    "Select Action:",
    ("Generate Concise Summary", "Create 5 Multiple Choice Questions (Quiz)")
)

if st.button("🚀 Generate Response", type="primary"):
    if not api_key_input:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not user_text.strip():
        st.warning("Please enter some text or topic to analyze.")
    else:
        try:
            with st.spinner("Processing with Gemini AI..."):
                genai.configure(api_key=api_key_input)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                if task_option == "Generate Concise Summary":
                    prompt = f"Act as an expert tutor. Provide a structured, clear, and easy-to-read bullet-point summary of the following content:\n\n{user_text}"
                else:
                    prompt = f"Act as an exam coordinator. Create a 5-question multiple choice quiz with correct answers based on the following text:\n\n{user_text}"
                
                response = model.generate_content(prompt)
                
                st.success("✨ Analysis Complete!")
                st.markdown("### Output Result")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error communicating with Gemini API: {str(e)}")
