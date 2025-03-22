# AirSprint Intern Assignment

## Overview

This Jupyter Notebook is a **data analysis project** for the **AirSprint Internship**.

I analyzed the provided datasets as well as data from API. Created a streamlit application that displayed my visuals (Invoice & March Flight breakdowns) and allows PDF generation, as well as email function.

## Requirements Checked
1. Data Processing & Transformation ✅ 
2. SQL & ETL Skills ✅ 
3. Dashboard & Visualization - Unsure whether to include barcharts & piecharts and such in an invoice assessment ❓
4. Automation & Process Efficiency ✅ 
5. Creativity & Problem Solving - Unsure on Roll-Over Hours from previous year ❓
6. Documentation ✅

This assessment was an incredible learning experience. I had the opportunity to explore PDF conversion and emailing, areas I wasn’t very familiar with before. My previous experience with Streamlit from my graduate projects helped me quickly adapt to building the web app. While working with aviation data is something I enjoy, handling invoices was a new challenge. Overall, it was a great experience that helped me grow my skills in data handling, visualization, and practical application development.

---

## 1. Data Cleaning and Preprocessing

### 1.1 Data Import
The first step is to import the necessary data files:
- CSV files from the email
- pulled API from fl3xx
    - ETA, ETD, Registration Number, airportFrom, airportTo and derived Flight Time from ETA & ETD  
    - No data found for Flight ID 79970
    - 79959 (CGBAS) does not have departure airport, arrival appears as KREG (Louisiana) but flightaware does not have any data on March 12th
    - https://www.flightaware.com/live/flight/CGBAS/history/20250318/1315Z/KPBI/KRSW

### 1.2 Data Inspection
- Missing values
- Unexpected data types
- General data quality issues
    - Found duplicates on asset & opportunity
    - Turned out to be Null duplicates & IsWon (Binary) duplicates
    - Re-inspected all other tables since there should be many duplicates (account numbers, invoice numbers, etc...)
    - Passes inspection ✅

### 1.3 Data Cleaning
- Renaming columns for consistency
- Handling missing data - decided to not handle any due to nature of the assessment

### 1.4 Data Transformation
- Date formatting: The dates in `Lease_Renewal_Date_2__c` and `Lease_Renewal_Date_3__c` columns are formatted into `YYYY-MM-DD` format.
- ID Conversion: The account number ID is converted into a string format to preserve leading zeros and prevent loss of data precision.

---

## 2. Data Exploration and Summary Generation

### 2.1 Aircraft Group Invoice Summary
- Account Name - pulled from Account where Name = "Jim Jets"
- Contact Name - Pulled from Contact matching Jim Jets' Contact ID from Account
- Account Number - Pulled from Account where Name = "Jim Jets", column = Account Number
- Date - Today's date with datetime() in pandas
- Anniversary Date - Pulled from Account where Name "Jim Jets", column = Lease Renewal CJ2+ & CJ3+ , ignored the first one because it does not belong in CJ group
- Aircraft - Combined the columns from Aircraft, combined table with asset after normalizing column name, matched accountID with Jim Jet's accountID then select
- Airgroup - implemented lambda function to add a column that puts CJ if the aircraft column contains 'CJ' in it, else 'Legacy' to separate out Airgroup
- Ownership Percentage - Used the previously combined table and aggregate on selected flights, multiply by 100 and adds '%' to reflect percentage.
- Total Contract Hours Brought Forward From Previous Year: Couldn't find any data that specifically mentions from previous year. However, due to some high hours from certain flight registrations, I assumed those hours cannot come from a single year. Same retrival method as ownership percentage.
- Total Hours Purchased in 2025: match AccountID in Opportunity -> came up with 3 'CJ' results, one is CJ2+ isn't in 2025, so only 2 results
- Total Flight Time Used: implemented SQL to inner join Flight Time and Aircraft. Then used the calculated flight time (from ETA & ETD)

### 2.2 Detailed Flight Breakdown
- Invoice Number - in Invoice - Match Flight ID
- Date of Invoice - in Invoice - Match Flight ID - change to Date time format
- Aircraft Registration/Tail - filtered out March, used SQL to combined filtered March table & flight time (extracted Registration from API) 
- Total Flight Time - from previous combined table
- Origin & Destination Airport - from previous combined table, 9959 (CGBAS) does not have departure airport, checked flightaware and yielded nothing
- Total Invoice Amount - from Invoice
- Comments - from Invoice

### 2.3 Data Organization
- Collected all the necessary information and put them in dataframe for automation
- Exported as CSV files
  
---

## 3. PDF Report Generation

### 3.1 Report Template
- Utilizes Jinja2 templates to generate a formatted HTML report, which can then be converted into a PDF using WeasyPrint. 
- Made an interactive application with streamlit, made a toggle button between CJ2+ and CJ3+ visual invoice summary while keeping invoice the same
- I honestly think I lack a bit knowledge on industry standard for invoices, I didn't email for clarification because I think the assessment is testing my problem-solving as well as technical skills, I just need to showcase my skills.

### 3.2 Export to PDF
- There is a button on streamlit App to export to PDF
  
---

## 4. Sending the Report via Email

### 4.1 Email Functionality
- After the PDF is generated, the notebook offers an option to send the report via email using Gmail
- I have already set Sender to my email with Application passwords - I embedded in the application so I don't have to enter it every time - but it also means anyone has access to my application can send unlimited spam emails
- Email has Recipient (Set to Stephany Welter), Sender (set to my gmail), Subject, and body, as well as the PDF reports as an attachment.

---

## 5. Future Enhancements

- Deploy PDF Export on Cloud: Fix issues related to WeasyPrint and deploy the PDF export functionality on a VM or external server.
  - My AWS is out of money and I couldn't deploy on Streamlit community due to Weasyprint requires installing libraries which I can't do.

---

## Conclusion

Overall, I really appreciate AirSprint for giving me such a wonderful opportunity to explore areas I hadn’t worked with before. I hope my work on this project impresses you, and I look forward to having a great interview.

---

