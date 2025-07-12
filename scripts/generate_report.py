from fpdf import FPDF
import pandas as pd
import os

def generate_pdf_report(csv_path, output_path):
    df = pd.read_csv(csv_path)

    total_students = len(df)
    passed = len(df[df['Result'] == "Pass"])
    failed = total_students - passed
    pass_percentage = round((passed / total_students) * 100, 2)

    subjects = [col for col in df.columns if col.endswith("_Total")]
    subject_averages = df[subjects].mean().sort_values(ascending=False)

    toppers = df.sort_values(by="Grand_Total", ascending=False).head(5)[["RegNo", "Name", "Grand_Total"]]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Result Analysis Report", ln=True, align='C')

    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Total Students: {total_students}", ln=True)
    pdf.cell(200, 10, f"Passed: {passed}", ln=True)
    pdf.cell(200, 10, f"Failed: {failed}", ln=True)
    pdf.cell(200, 10, f"Pass Percentage: {pass_percentage}%", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Subject-wise Averages:", ln=True)
    pdf.set_font("Arial", '', 12)
    for subject, avg in subject_averages.items():
        pdf.cell(200, 10, f"{subject}: {round(avg, 2)}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Top 5 Students:", ln=True)
    pdf.set_font("Arial", '', 12)
    for index, row in toppers.iterrows():
        pdf.cell(200, 10, f"{row['RegNo']} - {row['Name']} : {row['Grand_Total']} marks", ln=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"PDF report saved to: {output_path}")

# Run as script
if __name__ == "__main__":
    generate_pdf_report("../data/marklist_with_marks.csv", "../pdf_report/result_summary.pdf")
