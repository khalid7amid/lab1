import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

st.set_page_config(page_title="Interactive QAM Lab", layout="centered")
st.title("📡 Wireless Communication Interactive Lab")
st.subheader("🔁 Back-to-Back 16–QAM | Lab 1")

st.markdown("Please enter your full name or student ID to begin.")
student_name = st.text_input("🧑‍🎓 Your Name or Student ID")

# المهام والأسئلة
tasks = [
    {"question": "What is the shape of the bit vector `srcBits` if it contains 20,000 bits as a column vector?", "answer": "(20000, 1)"},
    {"question": "What is the modulation order used for 16-QAM?", "answer": "16"},
    {"question": "How many modulated symbols are generated from 20,000 bits using 16–QAM (4 bits per symbol)?", "answer": "5000"},
    {"question": "How many distinct points are there in a 16–QAM constellation diagram?", "answer": "16"},
    {"question": "What MATLAB function is used to visualize the QAM constellation diagram?", "answer": "scatterplot"},
    {"question": "What is the name of the variable that holds the demodulated output bits?", "answer": "demodOut"},
    {"question": "Which MATLAB function can be used to check if `srcBits` and `demodOut` are identical?", "answer": "isequal"},
]

# تحميل أو إنشاء ملف CSV
csv_file = "responses.csv"
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Name", "Question", "Your Answer", "Correct Answer", "Correct", "Timestamp"])

if student_name:
    st.markdown("---")
    st.header("📝 Lab Questions")

    for i, task in enumerate(tasks):
        st.markdown(f"**Q{i+1}: {task['question']}**")
        user_input = st.text_input(f"Your Answer for Q{i+1}", key=f"answer_{i}")
        if user_input:
            correct = str(user_input).strip().lower() == str(task["answer"]).strip().lower()
            st.markdown("✅ Correct" if correct else "❌ Incorrect")

            row = {
                "Name": student_name,
                "Question": task["question"],
                "Your Answer": user_input,
                "Correct Answer": task["answer"],
                "Correct": "✅" if correct else "❌",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            hash_id = hashlib.sha256(f"{student_name}_{i}".encode()).hexdigest()
            if not ((df["Name"] == student_name) & (df["Question"] == task["question"])).any():
                df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                df.to_csv(csv_file, index=False)

    st.markdown("---")
    st.success("🎉 You've completed the lab. Stay tuned for Lab 2 in the next release.")
