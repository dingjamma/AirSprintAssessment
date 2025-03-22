import streamlit as st
import pandas as pd
from datetime import date
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

# Load data
df_summary_cj2 = pd.read_csv("invoice_summary_cj2+.csv")
df_summary_cj3 = pd.read_csv("invoice_summary_cj3+.csv")
df_invoice = pd.read_csv("invoice.csv")

st.title("📄 JimJets Invoice Summary Dashboard")
st.write(f"**Report Date:** {date.today().strftime('%Y-%m-%d')}")

# CJ2+ / CJ3+ toggle
aircraft_group = st.radio("Select Aircraft Group:", ["CJ2+", "CJ3+"], horizontal=True)

# Display selected group with index hidden
if aircraft_group == "CJ2+":
    st.header("✈️ CJ2+ Aircraft Group - Invoice Summary")
    st.dataframe(df_summary_cj2.style.hide(axis="index"))
    selected_df = df_summary_cj2
else:
    st.header("✈️ CJ3+ Aircraft Group - Invoice Summary")
    st.dataframe(df_summary_cj3.style.hide(axis="index"))
    selected_df = df_summary_cj3

# Pre-convert summary table for PDF rendering
summary_html = selected_df.to_html(index=False)

# Show invoice table
st.header("🧾 Detailed Flight Breakdown - March 2025")
st.dataframe(df_invoice.style.hide(axis="index"))

# PDF Export
with st.expander("📥 Export to PDF"):
    if st.button(f"Generate PDF for {aircraft_group}"):
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("invoice_template_single.html")

        html_out = template.render(
            today=date.today().strftime('%Y-%m-%d'),
            aircraft_group=aircraft_group,
            summary_table=summary_html,
            invoice_table=df_invoice.to_html(index=False)
        )

        output_path = f"output/JimJets_Report_{aircraft_group.replace('+', 'Plus')}.pdf"
        HTML(string=html_out).write_pdf(output_path)

        st.session_state["last_pdf"] = output_path
        st.success(f"✅ PDF for {aircraft_group} Generated!")

# Email Form
with st.form("email_form"):
    st.markdown("📤 **Send this report via email**")

    recipient = st.text_input("Recipient Email", value="swelter@airsprint.com")
    sender = st.text_input("Your Gmail Address", value="youremail@gmail.com")
    subject = st.text_input("Email Subject", value=f"JimJets Report - {aircraft_group}")
    message = st.text_area("Message", value="Please find the attached invoice summary and breakdown.")

    app_password = "qznk hlgw ydaq ftyz"

    submit = st.form_submit_button("Send Email")

    if submit:
        if "last_pdf" not in st.session_state:
            st.warning("⚠️ Please generate a PDF before sending the email.")
        else:
            try:
                import yagmail
                yag = yagmail.SMTP(sender, app_password)
                yag.send(
                    to=recipient,
                    subject=subject,
                    contents=message,
                    attachments=st.session_state["last_pdf"]
                )
                st.success(f"✅ Email sent to {recipient}!")
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")
