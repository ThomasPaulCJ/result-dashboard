import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

st.set_page_config(page_title="Result Dashboard", layout="wide")

st.title("📊 Result Analysis Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload Marklist CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Show raw data
    st.subheader("Full Marklist")
    st.dataframe(df, use_container_width=True)

    # Result summary
    total_students = len(df)
    passed = len(df[df['Result'] == "Pass"])
    failed = total_students - passed
    pass_percentage = round((passed / total_students) * 100, 2)

    st.subheader("📌 Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", total_students)
    col2.metric("Passed", passed, delta=f"{pass_percentage}%")
    col3.metric("Failed", failed)

    # Pie chart - Pass vs Fail
    st.subheader("📉 Pass vs Fail Distribution")
    fig1, ax1 = plt.subplots()
    ax1.pie([passed, failed], labels=["Pass", "Fail"], autopct='%1.1f%%', colors=["#90ee90", "#ffcccb"])
    ax1.axis('equal')
    st.pyplot(fig1)

    # Subject-wise average marks
    st.subheader("📚 Subject-wise Averages")
    subjects = [col for col in df.columns if col.endswith("_Total")]
    subject_averages = df[subjects].mean().sort_values(ascending=False)

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.barplot(x=subject_averages.index, y=subject_averages.values, ax=ax2, palette="Blues_d")
    ax2.set_ylabel("Average Marks")
    ax2.set_xlabel("Subjects")
    ax2.set_title("Subject-wise Average Marks")
    st.pyplot(fig2)

    # Toppers
    st.subheader("🏆 Top 5 Students")
    toppers = df.sort_values(by="Grand_Total", ascending=False).head(5)[["RegNo", "Name", "Grand_Total", "Average"]]
    st.table(toppers.reset_index(drop=True))

    # Search filter
    st.subheader("🔎 Search Student")
    search = st.text_input("Enter Name or RegNo")
    if search:
        filtered = df[df['Name'].str.contains(search, case=False) | df['RegNo'].str.contains(search, case=False)]
        st.dataframe(filtered)

    # Filter: Pass/Fail
    st.subheader("📌 Filter by Result")
    result_filter = st.selectbox("Select Result Type", ["All", "Pass", "Fail"])
    if result_filter != "All":
        st.dataframe(df[df['Result'] == result_filter])

    # Generate PDF report
    st.subheader("📥 Generate PDF Report")
    if st.button("Generate Summary Report PDF"):
        subprocess.run(["python", "scripts/generate_report.py"])
        st.success("PDF generated in 'pdf_report/' folder!")

else:
    st.info("👈 Upload a CSV file to get started.")
