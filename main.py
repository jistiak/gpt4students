import requests
import openai
import streamlit as st
from io import BytesIO
import base64
from fpdf import FPDF

# Create form for syllabus input
syllabus_input = st.radio("Choose syllabus input method:", ("Text input", "Upload file"))

if syllabus_input == "Text input":
    syllabus = st.text_area("Enter your syllabus here:")
elif syllabus_input == "Upload file":
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        syllabus = uploaded_file.getvalue().decode("utf-8")
    else:
        st.write("Please upload a file or enter your syllabus in the text area.")
        st.stop()

term_length = st.slider("Select your term length (in weeks)", 1, 20, 10)

# Create form for exam preparation input
exam_syllabus_input = st.radio("Choose exam syllabus input method:", ("Text input", "Upload file"))

if exam_syllabus_input == "Text input":
    exam_syllabus = st.text_area("Enter your exam syllabus here:")
elif exam_syllabus_input == "Upload file":
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        exam_syllabus = uploaded_file.getvalue().decode("utf-8")
    else:
        st.write("Please upload a file or enter your exam syllabus in the text area.")
        st.stop()

days_left = st.slider("Select the number of days left until your exam", 1, 100, 30)

# Create form for generating study plan
generate_plan = st.button("Generate study plan")

if generate_plan:
    if "syllabus" not in locals() or syllabus.strip() == "":
        st.write("Please enter your syllabus.")
    else:
        # Generate study plan
        prompt = f"Generate a study plan for a {term_length}-week term based on the following syllabus:\n\n{syllabus}"
        response = openai.Completion.create(
          engine="davinci",
          prompt=prompt,
          max_tokens=1024,
          n=1,
          stop=None,
          temperature=0.5,
        )

        study_plan = response.choices[0].text

        # Display study plan to user
        st.write("Here's your study plan:")
        st.write(study_plan)

# Create form for generating exam preparation plan
generate_exam_plan = st.button("Generate exam preparation plan")

if generate_exam_plan:
    if "exam_syllabus" not in locals() or exam_syllabus.strip() == "":
        st.write("Please enter your exam syllabus.")
    else:
        # Generate exam preparation plan
        prompt = f"Generate an exam preparation plan based on the following syllabus:\n\n{exam_syllabus}\n\nYou have {days_left} days until your exam."
        response = openai.Completion.create(
          engine="davinci",
          prompt=prompt,
          max_tokens=1024,
          n=1,
          stop=None,
          temperature=0.5,
        )

        exam_plan = response.choices[0].text

        # Display exam preparation plan to user
        st.write("Here's your exam preparation plan:")
        st.write(exam_plan)


# Define the GitHub API endpoint for issues
issues_url = 'https://api.github.com/repos/jistiak/gpt4students/issues'

# Set the headers for the API request, with your personal access token
headers = {
    'Authorization': f'Token <your-access-token>',
    'Accept': 'application/vnd.github.v3+json'
}

# Define a function to create a new issue on GitHub
def create_github_issue(title, body):
    # Define the JSON payload for the API request
    payload = {
        'title': title,
        'body': body
    }
    # Send the API request to create the new issue
    response = requests.post(issues_url, headers=headers, json=payload)
    if response.status_code == 201:
        print('Feature request posted successfully!')
    else:
        print('Error:', response.text)

# Call the create_github_issue function with the user's input
create_github_issue('New feature request', 'Please add a feature that allows me to do XYZ')

# create a function to generate resource recommendations
def generate_resources(topic):
    prompt = "Find three books, three research papers, and three blog or video links on " + topic
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n = 9,
        stop=None,
        )
    resources = response.choices[0].text.split("\n")
    return resources

# create a function to generate a PDF file
def generate_pdf(topic, resources):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=f"Recommended Resources for {topic}", ln=1, align="C")
    pdf.cell(200, 10, txt=" ", ln=1)
    for i, resource in enumerate(resources):
        pdf.cell(200, 10, txt=f"{i+1}. {resource}", ln=1, link=resource)
        pdf.cell(200, 5, txt=" ", ln=1)
    pdf.cell(200, 10, txt=" ", ln=1)
    pdf.output("resources.pdf", "F")
    with open("resources.pdf", "rb") as pdf_file:
        b64 = base64.b64encode(pdf_file.read()).decode()
    return b64


# create the Streamlit app interface
st.title("Resource Recommendation Generator")
topic_input = st.text_input("Enter a topic")
if topic_input:
    resources = generate_resources(topic_input)
    st.markdown("# Recommended Resources")
    for i, resource in enumerate(resources):
        st.markdown(f"{i+1}. [{resource}]({resource})")

    pdf_button = st.download_button(
        label="Download PDF",
        data=generate_pdf(topic_input, resources),
        file_name="resources.pdf"
    )