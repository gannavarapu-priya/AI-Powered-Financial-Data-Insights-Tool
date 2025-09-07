import streamlit as st
from dotenv import load_dotenv
from rag_chain import answer_question
from pathlib import Path

load_dotenv()

# ---------------------- Global styles -------------------- #
st.markdown(
    """
    <style>
      .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1100px;
      }
      html, body, [class*="css"] {
        font-size: 16px;
        font-family: 'Montserrat', sans-serif !important;
      }
      h1, h2, h3 {
        letter-spacing: .2px;
        text-align: center !important;  /* Center title and subtitle */
      }
      .title-wrap h1 {
        font-size: 1.9rem !important;
        font-weight: 700 !important;
        margin-bottom: .25rem !important;
      }
      .subtitle {
        color: rgba(255,255,255,0.65);
        margin-top: .1rem;
        margin-bottom: 1.25rem;
      }
      .card {
        background: rgba(255,255,255,0.03);
        border-radius: 14px;
        padding: 18px;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 8px 22px rgba(0,0,0,.20);
      }
      .stButton>button {
        background: linear-gradient(180deg, #4f46e5 0%, #4338ca 100%) !important;
        color: #fff !important;
        border: 0 !important;
        border-radius: 10px !important;
        padding: .55rem 1.1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(79,70,229,.45);
      }
      .stButton>button:hover {
        filter: brightness(1.04);
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(79,70,229,.55);
      }
      .stTextInput>div>div>input {
        border-radius: 10px !important;
        height: 44px !important;
        font-size: 0.98rem !important;
      }
      .stSelectbox>div>div>div>div {
        font-size: 0.98rem !important;
      }
      .section-title {
        margin-top: 22px;
        margin-bottom: 10px;
        font-size: 1.15rem;
        font-weight: 700;
      }
      .examples ul {
        margin-top: .25rem;
      }
      .examples li {
        margin: .3rem 0 .35rem 0;
        line-height: 1.35rem;
      }
      .footer {
        margin-top: 28px;
        opacity: .65;
        font-size: .88rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Optional: Montserrat font via Google Fonts
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# ---------------------- Title & Subtitle -------------------- #
st.markdown("<h1>Explore Companies Financial Reports</h1>", unsafe_allow_html=True)
st.markdown("<h3>Ask about revenue, risks, or trends - powered by AI, from 10-Ks.</h3>", unsafe_allow_html=True)

# ---------------------- Inputs ----------------------- #
companies = ["", "Microsoft", "Amazon", "Apple", "Meta"]
company = st.selectbox("Company", companies, index=0, placeholder="Choose options")

with st.form(key="qa_form"):
    q = st.text_input("Ask a question", placeholder="", label_visibility="visible")
    submitted = st.form_submit_button("Run")


# ---------------------- Run Logic ---------------------- #
if submitted:
    if not q.strip():
        st.warning("Please enter a question.")
        st.stop()
    filt = [company] if company and company in companies else None
    result = answer_question(q, k=8, company_filter=filt)
    st.subheader("Answer")
    st.write(result.get("answer", "No answer returned."))

# ---------------------- Example questions -------------- #
st.markdown('<div class="section-title">Example Questions</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="examples">
      <ul>
        <li>Summarize the main revenue drivers in this report.</li>
        <li>What were the key year-over-year changes in cost of revenue?</li>
        <li>List the top risks mentioned and why they matter.</li>
        <li>How did AI or cloud offerings impact growth?</li>
        <li>Compare segment revenue growth and margins.</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)
