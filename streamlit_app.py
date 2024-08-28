import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import streamlit as st
import pandas as pd
import snowflake.connector
from transformers import pipeline
from PIL import Image
import pdf2image



# Establish Snowflake connection using credentials from the .env file
@st.cache_resource
def create_connection():
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT')
    )

conn = create_connection()

# Database, schema, table, and column retrieval functions
def get_databases(conn):
    with conn.cursor() as cur:
        cur.execute("SHOW DATABASES")
        return [db[1] for db in cur.fetchall()]  # db[1] is the database name

def get_schemas(conn, database):
    with conn.cursor() as cur:
        cur.execute(f"SHOW SCHEMAS IN DATABASE {database}")
        return [schema[1] for schema in cur.fetchall()]  # schema[1] is the schema name

def get_tables(conn, database, schema):
    with conn.cursor() as cur:
        cur.execute(f"SHOW TABLES IN {database}.{schema}")
        return [table[1] for table in cur.fetchall()]  # table[1] is the table name

def get_columns(conn, database, schema, table):
    with conn.cursor() as cur:
        cur.execute(f"DESCRIBE TABLE {database}.{schema}.{table}")
        return [column[0] for column in cur.fetchall()]  # column[0] is the column name

# Function to reset the app state
def reset_app():
    st.session_state['question_count'] = 1
    st.session_state['questions'] = [""]
    st.session_state['selected_columns'] = [""]
    st.session_state['uploaded_files'] = None
    st.session_state['database_dropdown'] = 'Invoices'
    st.session_state['schema_dropdown'] = 'public'
    st.session_state['table_dropdown'] = 'table1'
    st.session_state['temp_df'] = None

# Function to clear all fields
def clear_all_fields():
    reset_app()
    st.rerun()

# Function to export data to Snowflake
def export_to_snowflake(df, conn, database, schema, table):
    with conn.cursor() as cur:
        cur.execute(f"USE DATABASE {database}")
        cur.execute(f"USE SCHEMA {schema}")

        columns_str = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))

        for row in df.itertuples(index=False, name=None):
            insert_query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
            cur.execute(insert_query, row)

        st.success("Data exported successfully!")

# Function to extract answers using a document question-answering pipeline
def extract_answers(file, questions):
    dqa = pipeline("document-question-answering")
    answers = []

    if file.type in ["image/jpeg", "image/png"]:
        image = Image.open(file)
        for question in questions:
            answer = dqa(image, question=question)
            answers.append(answer[0]['answer'])

    elif file.type == "application/pdf":
        images = pdf2image.convert_from_bytes(file.read())
        for question in questions:
            aggregated_answer = " ".join(
                dqa(image, question=question)[0]['answer'] for image in images
            )
            answers.append(aggregated_answer)

    if len(answers) != len(questions):
        raise ValueError(f"Expected {len(questions)} answers, got {len(answers)}")

    return answers

# Initialize session state if not already done
if 'question_count' not in st.session_state:
    reset_app()

# Streamlit App
st.title("Extraction Phase")

st.markdown("## Data upload and Model Configuration")
uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True, type=['pdf', 'jpg', 'jpeg', 'png'])

# Dropdowns for Database, Schema, and Table
database_dropdown = st.selectbox(label='Database', options=get_databases(conn))

if database_dropdown:
    schemas = get_schemas(conn, database_dropdown)
    schema_dropdown = st.selectbox(label='Schema', options=schemas)
else:
    schema_dropdown = st.selectbox(label='Schema', options=[])

if schema_dropdown:
    tables = get_tables(conn, database_dropdown, schema_dropdown)
    table_dropdown = st.selectbox(label='Table', options=tables)
else:
    table_dropdown = st.selectbox(label='Table', options=[])

# Button to add questions
if st.button("Add Question"):
    st.session_state.question_count += 1
    st.session_state.questions.append("")
    st.session_state.selected_columns.append("")

if table_dropdown:
    columns = get_columns(conn, database_dropdown, schema_dropdown, table_dropdown)
else:
    columns = []

# Render questions and column options
for i in range(st.session_state.question_count):
    col1, col2, col3 = st.columns([3, 8, 2])
    with col1:
        selected_col = st.selectbox(
            label='Column', options=columns, key=f"column_{i}", index=0
        )
        st.session_state.selected_columns[i] = selected_col
    with col2:
        st.session_state.questions[i] = st.text_input(f"Question {i+1}", key=f"question_{i}")
    with col3:
        if st.button("Delete", key=f"delete_question_{i}"):
            st.session_state.questions.pop(i)
            st.session_state.selected_columns.pop(i)
            st.session_state.question_count -= 1
            st.rerun()
# Used model
st.markdown("# Model")
st.markdown("Impira Document QA 🦉")

if uploaded_files:
    num_columns = len(st.session_state.selected_columns)
    num_questions = len(st.session_state.questions)

    if num_columns > num_questions:
        st.session_state.questions.extend([''] * (num_columns - num_questions))
    elif num_questions > num_columns:
        st.session_state.questions = st.session_state.questions[:num_columns]

    all_answers = []
    for file in uploaded_files:
        answers = extract_answers(file, st.session_state.questions)
        all_answers.append(answers)

    st.session_state['temp_df'] = pd.DataFrame(
        all_answers,
        columns=st.session_state.selected_columns
    )

    st.session_state['temp_df'].index = range(1, len(st.session_state['temp_df']) + 1)

st.markdown("# Result")
if st.session_state.get('temp_df') is not None:
    edited_df = st.data_editor(st.session_state['temp_df'], num_rows="dynamic", key="data_editor_key", hide_index=False)

    # Save edits to session state
    st.session_state['temp_df'] = edited_df.copy()
    st.session_state['temp_df'].index = range(1, len(st.session_state['temp_df']) + 1)
    print(st.session_state['temp_df'])

if st.button("Export to Snowflake"):
    if st.session_state.get('temp_df') is not None:
        export_to_snowflake(st.session_state['temp_df'], conn, database_dropdown, schema_dropdown, table_dropdown)
    else:
        st.write("No data to export!")

if st.button("Clear"):
    clear_all_fields()
