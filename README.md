# Automated Data Extractor for Unstructured Data

## 🎯 Overview

This project aims to develop an automated application for extracting and processing unstructured data from documents such as PDFs and images. The application integrates with Snowflake to automatically store the extracted data in a structured format.
<hr style="border: 2px solid darkgray;">

## 👁️ Application preview
![Main Page](assets/img/img.png)


<hr style="border: 2px solid darkgray;">

## ⚛️ Technologies Used

- **Streamlit**: For building the web interface.
- **Snowflake**: For data storage and management.
- **Transformers**: For leveraging AI models for document question-answering.
- **Pillow (PIL)**: For image processing.
- **pdf2image**: For converting PDF pages to images.
- **PyCharm**: IDE for integrated development and debugging.
- **GitHub**: For version control and collaboration.

<div style="text-align: center">
    <img src="assets/icons/streamlit.jpg" style="width:60px; height:60px; display: inline-block; margin-right: 10px; border-radius: 10px;">
    <img src="assets/icons/snowflake.png" style="width:105px; height:60px; display: inline-block; margin-right: 10px;">
    <img src="assets/icons/transformers.png" style="width:60px; height:60px; display: inline-block; margin-right: 25px;">
    <img src="assets/icons/pillow.png" style="width:60px; height:60px; display: inline-block; margin-right: 25px;">
    <img src="assets/icons/pycharm.png" style="width:60px; height:60px; display: inline-block; margin-right: 25px;">
    <img src="assets/icons/github.png" style="width:60px; height:60px; display: inline-block; margin-right: 100px;">
</div>

<hr style="border: 2px solid darkgray;">

## 🔧 Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Yessine-BenHamroun/BI4YOU_Project.git
   cd <repository-directory>

2. **Install Required Libraries**

   ```bash
   pip install -r requirements.txt

3. **Setup Environment Variables**\
   Create a .env file in the root directory and add your Snowflake credentials:

   ```bash
   SNOWFLAKE_USER=your_username
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_ACCOUNT=your_account
<hr style="border: 2px solid darkgray;">

## 🤖 Running the application

1. **Start the Streamlit Application**
   ```bash
   streamlit run streamlit_app.py

2. **Access the Application**\
   Open a web browser and navigate to http://localhost:8501.
<hr style="border: 2px solid darkgray;">

## 👨🏻‍💻 Usage

1. **Upload Data: Import your documents (PDFs or images) to be processed by pressing on "Browse files".**
---
   ![Upload Phase](assets/img/upload.png)

2. **Select Database: Choose the Snowflake database you want to use.**
---
![DB dropdown](assets/img/db_dd.png)

3. **Select Schema: Choose the schema within the selected database.**
---
![schema dropdown](assets/img/schema_dd.png)

4. **Select Table: Choose the table where the extracted data will be stored.**
---
![tables dropdown](assets/img/tables_dd.png)

5. **Specify Columns: Indicate which columns will store the answers to your question.**
---
![columns dropdown](assets/img/columns_dd.png)

6. **Ask Questions: Enter the questions you want to ask about the documents.You can add more questions by pressing on "Add Question"**
---
![add questions](assets/img/add_qst.png)

7. **Review Results: Modify or delete the extracted data if necessary.**
---
![result preview](assets/img/preview.png)

You can preview results in full screen as well to help you manage multiple data.

![result in fullscreen](assets/img/preview_fs.png)

8. **Export to Snowflake: Confirm and export the data to the selected Snowflake table**
---
![export to snowflake](assets/img/export.png)

Uploaded data to Snowflake:

![snowflake table](assets/img/snowflakedata.png)
<hr style="border: 2px solid darkgray;">

## 🚀 Features
1. **Dynamic Question Management: Add, edit, and delete questions for data extraction.**
2. **Data Editing: Modify and review extracted data before exporting.**
3. **Multi-File Support: Process multiple files simultaneously.**
4. **Automated Data Storage: Automatically load extracted data into Snowflake.**


