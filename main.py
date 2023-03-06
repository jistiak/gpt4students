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