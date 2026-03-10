import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="AI Resume Ranking",
    page_icon="🤖",
    layout="wide"
)


st.markdown("""
<style>

.main-title {
    font-size:48px;
    font-weight:800;
    text-align:center;
    background: linear-gradient(90deg,#ff4b4b,#6c63ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align:center;
    color:gray;
    margin-bottom:30px;
}

.card {
    padding:20px;
    border-radius:15px;
    background-color:#f8f9ff;
    box-shadow:0 4px 15px rgba(0,0,0,0.1);
}

.rank-card {
    padding:15px;
    border-radius:12px;
    background:linear-gradient(90deg,#6c63ff,#5a54d6);
    color:white;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">🤖 AI Resume Screening</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload resumes and automatically rank candidates</div>', unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "📄 Upload Candidate Resumes",
        type=["pdf"],
        accept_multiple_files=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    jd = st.text_area(
        "🧾 Paste Job Description",
        height=220,
        placeholder="Paste the job description here..."
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")

rank_button = st.button("🚀 Rank Candidates", use_container_width=True)

if rank_button:

    if not uploaded_files:
        st.warning("Please upload resumes first.")

    elif not jd.strip():
        st.warning("Please paste the job description.")

    else:

        with st.spinner("🔍 Analyzing resumes..."):

            files = []

            for file in uploaded_files:
                files.append(("files", (file.name, file.getvalue())))

            response = requests.post(
                "http://127.0.0.1:8000/rank",
                files=files,
                data={"jd": jd}
            )

            results = response.json()

            st.success("✅ Ranking completed!")

            df = pd.DataFrame(results)

            if "score" in df.columns:
                df = df.sort_values(by="score", ascending=False)

            st.divider()

            st.subheader("🏆 Candidate Rankings")

            if len(df) > 0:
                top = df.iloc[0]

                st.markdown(f"""
                <div class="rank-card">
                🥇 <b>Top Candidate:</b> {top['name']} <br>
                Score: {top['score']}%
                </div>
                """, unsafe_allow_html=True)

            for i, row in df.iterrows():

                st.markdown(f"""
                <div class="card">
                <b>{row['name']}</b> <br>
                Score: {row['score']}%
                </div>
                """, unsafe_allow_html=True)

                st.progress(float(row["score"]) / 100)

            st.divider()

            st.subheader("📊 Detailed Results")

            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇ Download Ranking",
                csv,
                "ranking_results.csv",
                "text/csv"
            )