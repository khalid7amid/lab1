
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Interactive QAM Lab", layout="centered")
st.title("📡 Wireless Communication Interactive Lab")
st.subheader("🔁 Back-to-Back 16–QAM | Lab 1")

# إدخال اسم الطالب
student_name = st.text_input("🧑‍🎓 Enter your Name or Student ID")

# حقل سري للمدرس فقط
admin_password = st.text_input("🔐 Admin Access (optional)", type="password")
is_admin = (admin_password == "adminpass")  # ← يمكنك تغييرها لاحقًا لكلمة سر خاصة

if not student_name:
    st.warning("Please enter your name to begin.")
    st.stop()

# المهام والتعليمات من Task 1 إلى Further Practice
tasks = [
    {
        "title": "Task 1",
        "description": """### Background
The first step in any digital communications simulation is to create a source signal.
Here, the source signal is a sequence of bits—or, in MATLAB terms, a vector of 0s and 1s.

You can use the `randi` function to create a column vector of randomly-generated 0s and 1s in MATLAB:

```matlab
x = randi([0,1],numBits,1)
```

The output `x` is a column vector containing `numBits` bits.
""",
        "question": "Create a column vector named srcBits containing 20,000 randomly-generated bits. What is its shape?"
    },
    {
        "title": "Task 2",
        "description": """### Background
QAM is a modulation scheme that maps 4 input bits to one of 16 complex numbers (symbols)—16-QAM.
The “16” refers to the modulation order.
""",
        "question": "What is the modulation order used for 16-QAM?"
    },
    {
        "title": "Task 3",
        "description": """### Background
Use the `qammod` function to modulate the bits:

```matlab
modOut = qammod(srcBits, modOrder, 'InputType','bit')
```

If there are 20,000 bits and you use 4 bits per symbol, how many modulated symbols will you get?
""",
        "question": "How many symbols are generated from 20,000 bits using 16-QAM?"
    },
    {
        "title": "Task 4",
        "description": """### Background
You can visualize the signal using:

```matlab
scatterplot(modOut)
```

This shows a constellation diagram with each point representing a QAM symbol.
""",
        "question": "How many distinct points are there in a 16-QAM constellation diagram?"
    },
    {
        "title": "Task 5",
        "description": """### Background
Assume the channel doesn’t affect the signal:

```matlab
chanOut = modOut
```

This helps isolate the demodulation step only.
""",
        "question": "What MATLAB function is used to visualize the QAM constellation?"
    },
    {
        "title": "Task 6",
        "description": """### Background
Demodulate the received signal back into bits using:

```matlab
z = qamdemod(y, modOrder, 'OutputType','bit')
```

The output `z` is a column vector of 1s and 0s—the received bits.
""",
        "question": "What is the name of the variable that holds the demodulated output bits?"
    },
    {
        "title": "Task 7",
        "description": """### Background
Compare the source and received bits using:

```matlab
check = isequal(x1,x2)
```

The output `check` is 1 if the vectors are identical, and 0 otherwise.
""",
        "question": "Which MATLAB function can be used to check if `srcBits` and `demodOut` are identical?"
    },
    {
        "title": "Further Practice",
        "description": """Because 16-QAM maps input bits in sets of 4, the number of source bits must be a multiple of 4.  
Try changing the number of bits in the source signal. What happens if it's not a multiple of 4?
""",
        "question": "What do you observe when the number of bits is not a multiple of 4?"
    }
]

# عرض المهام
answers = []
for task in tasks:
    with st.expander(task["title"]):
        st.markdown(task["description"])
        ans = st.text_input(f"✏️ {task['question']}", key=task["title"])
        answers.append(ans)

# زر الإرسال
if st.button("✅ Submit Lab"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {"timestamp": timestamp, "name": student_name}
    for i, task in enumerate(tasks):
        row[f"task_{i+1}"] = answers[i]
    try:
        df = pd.read_csv("responses.csv")
    except:
        df = pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv("responses.csv", index=False)
    st.success("✅ Your answers have been saved! Thank you!")

# زر تحميل للمدرس فقط
if is_admin:
    try:
        with open("responses.csv", "rb") as file:
            st.download_button("📥 Download Responses (Admin Only)", file, file_name="responses.csv")
    except FileNotFoundError:
        st.warning("⚠️ No responses yet to download.")
