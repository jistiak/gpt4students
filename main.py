import requests

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