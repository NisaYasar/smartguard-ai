import streamlit as st
import joblib
import re

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

urdu_words = ["bewaqoof", "pagal", "jahil", "bakwas", "ullu", "kutta"]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

def check_urdu(text):
    text = text.lower()
    return any(word in text for word in urdu_words)

def predict(text):
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])
    return model.predict(vec)[0]

st.set_page_config(page_title="SmartGuard AI", page_icon="🛡")

st.markdown(
    "<h1 style='text-align:center; color:#4CAF50;'>🛡 SmartGuard AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:gray;'>AI-Based Social Media Content Moderation System</p>",
    unsafe_allow_html=True
)

st.write("---")

user_input = st.text_area("✍ Enter your comment here:", height=120)

if st.button("🔍 Analyze"):

    if user_input.strip() == "":
        st.warning("Please enter a comment first.")
    else:

        category = predict(user_input)
        urdu_flag = check_urdu(user_input)

        if category == "Hate Speech" or urdu_flag:
            risk = "🔴 HIGH RISK"
            color = "red"
            recommendation = "🚨 Flag for Review"

        elif category == "Offensive Language":
            risk = "🟠 MEDIUM RISK"
            color = "orange"
            recommendation = "⚠ Review Suggested"

        else:
            risk = "🟢 LOW RISK"
            color = "green"
            recommendation = "✅ Safe Content"

        st.markdown("### 📊 Result")

        st.markdown(
            f"""
            <div style="
                padding:20px;
                border-radius:10px;
                background-color:#f5f5f5;
                border-left:8px solid {color};
            ">
                <h4>Category: {category}</h4>
                <h4>Risk Level: {risk}</h4>
                <h4>Recommendation: {recommendation}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )