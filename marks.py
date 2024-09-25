import streamlit as st
import os
import json
import plotly.express as px
import pandas as pd

# Function to save credentials as JSON file
def save_credentials(name, email, password, phone, dob):
    folder_name = email.split('@')[0]  # Use email's local part as folder name
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, "credentials.json")

    user_data = {
        'name': name,
        'email': email,
        'password': password,
        'phone': phone,
        'dob': str(dob)
    }
    with open(file_path, 'w') as json_file:
        json.dump(user_data, json_file, indent=4)

# Function to load credentials from JSON file
def load_credentials(folder_name):
    file_path = os.path.join(folder_name, "credentials.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    return None

# Sidebar navigation function
def sidebar_navigation():
    if 'username' in st.session_state:
        st.sidebar.title(f"Welcome, {st.session_state['username']}")
        if st.sidebar.button("Sign Out"):
            del st.session_state['username']
            st.session_state['page'] = 'login'
            st.experimental_rerun()
    else:
        action = st.sidebar.radio("Navigation", ["Log In", "Sign Up"])
        if action == "Log In":
            st.session_state['page'] = 'login'
        elif action == "Sign Up":
            st.session_state['page'] = 'signup'

def sign_up_page():
    st.title("Welcome to the Sign Up Page")
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    dob = st.date_input("Date of Birth")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if name and phone and dob and email and password:
            folder_exists = os.path.exists(email.split('@')[0])
            if folder_exists:
                st.error("A user with this email already exists. Please log in.")
            else:
                save_credentials(name, email, password, phone, dob)
                st.success("Sign up successful! Redirecting to login...")
                st.session_state['page'] = 'login'
        else:
            st.error("Please fill in all the fields.")

def login_page():
    st.title("Welcome to the Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        folder_name = email.split('@')[0]
        credentials = load_credentials(folder_name)

        if credentials and credentials['password'] == password:
            st.session_state['username'] = credentials['name']
            st.session_state['page'] = 'marks'
            st.success("Login successful! Redirecting to marks page...")
        else:
            st.error("Invalid email or password.")

def marks_page():
    st.title(f"Welcome, {st.session_state['username']}")  # Updated title

    subjects = ['English', 'Math', 'Science']
    marks = {}
    for subject in subjects:
        marks[subject] = st.slider(f"Choose your marks for {subject}", 0, 100)

    if st.button("Submit"):
        folder_name = st.session_state['username']  # Folder based on username
        # Create folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_path = os.path.join(folder_name, "marks.csv")
        marks_df = pd.DataFrame(list(marks.items()), columns=['Subject', 'Marks'])
        marks_df.to_csv(file_path, index=False)

        st.success("Marks saved successfully! Redirecting to report page...")
        st.session_state['page'] = 'report'


def report_page():
    st.title("Your Reports are Ready")
    folder_name = st.session_state['username']
    file_path = os.path.join(folder_name, "marks.csv")
    if not os.path.exists(file_path):
        st.error("Marks not found. Please submit your marks.")
        return

    marks_df = pd.read_csv(file_path)

    # Average Marks Bar Chart
    avg_marks = marks_df['Marks'].mean()
    st.subheader("Average Marks Bar Chart")
    fig1 = px.bar(x=['Average Marks'], y=[avg_marks], labels={'x': 'Category', 'y': 'Marks'})
    st.plotly_chart(fig1)

    # Marks per subject Line Graph
    st.subheader("Marks per Subject - Line Graph")
    fig2 = px.line(marks_df, x='Subject', y='Marks', title='Marks per Subject')
    st.plotly_chart(fig2)

    # Marks per subject Pie Chart
    st.subheader("Marks per Subject - Pie Chart")
    fig3 = px.pie(marks_df, names='Subject', values='Marks', title='Marks Distribution per Subject')
    st.plotly_chart(fig3)

# Main function to render pages based on session state
def main():
    # Initialize the session state if it doesn't exist
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'  # Default to login page

    sidebar_navigation()  # Show the sidebar navigation based on the session state

    # Render the appropriate page based on the session state
    if st.session_state['page'] == 'signup':
        sign_up_page()
    elif st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'marks':
        marks_page()
    elif st.session_state['page'] == 'report':
        report_page()

if __name__ == "__main__":
    main()
