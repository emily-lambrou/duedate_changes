from pprint import pprint
import requests
import logging
import config
import utils

def get_repo_issues(owner, repository, duedate_field_name, after=None, issues=None):
    query = """
    query GetRepoIssues($owner: String!, $repo: String!, $duedate: String!, $after: String) {
          repository(owner: $owner, name: $repo) {
            issues(first: 100, after: $after, states: [OPEN]) {
              nodes {
                id
                title
                number
                url
                assignees(first:100) {
                  nodes {
                    name
                    email
                    login
                  }
                }
                projectItems(first: 10) {
                  nodes {
                    project {
                      number
                      title
                    }
                    fieldValueByName(name: $duedate) {
                      ... on ProjectV2ItemFieldDateValue {
                        id
                        date
                      }
                    }
                  }
                }
              }
              pageInfo {
                endCursor
                hasNextPage
                hasPreviousPage
              }
              totalCount
            }
          }
        }
    """

    variables = {
        'owner': owner,
        'repo': repository,
        'duedate': duedate_field_name,
        'after': after
    }

    response = requests.post(
        config.api_endpoint,
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {config.gh_token}"}
    )

    if response.json().get('errors'):
        print(response.json().get('errors'))

    pageinfo = response.json().get('data').get('repository').get('issues').get('pageInfo')
    if issues is None:
        issues = []
    issues = issues + response.json().get('data').get('repository').get('issues').get('nodes')
    if pageinfo.get('hasNextPage'):
        return get_repo_issues(
            owner=owner,
            repository=repository,
            after=pageinfo.get('endCursor'),
            issues=issues,
            duedate_field_name=duedate_field_name
        )

    return issues

def get_project_issues(owner, owner_type, project_number, duedate_field_name, filters=None, after=None, issues=None):
    query = f"""
    query GetProjectIssues($owner: String!, $projectNumber: Int!, $duedate: String!, $after: String)  {{
          {owner_type}(login: $owner) {{
            projectV2(number: $projectNumber) {{
              id
              title
              number
              items(first: 100,after: $after) {{
                nodes {{
                  id
                  fieldValueByName(name: $duedate) {{
                    ... on ProjectV2ItemFieldDateValue {{
                      id
                      date
                    }}
                  }}
                  content {{
                    ... on Issue {{
                      id
                      title
                      number
                      state
                      url
                      assignees(first:20) {{
                        nodes {{
                          name
                          email
                          login
                        }}
                      }}
                    }}
                  }}
                }}
                pageInfo {{
                endCursor
                hasNextPage
                hasPreviousPage
              }}
              totalCount
              }}
            }}
          }}
        }}
    """

    variables = {
        'owner': owner,
        'projectNumber': project_number,
        'duedate': duedate_field_name,
        'after': after
    }

    response = requests.post(
        config.api_endpoint,
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {config.gh_token}"}
    )

    if response.json().get('errors'):
        print(response.json().get('errors'))

    pageinfo = response.json().get('data').get(owner_type).get('projectV2').get('items').get('pageInfo')
    if issues is None:
        issues = []

    nodes = response.json().get('data').get(owner_type).get('projectV2').get('items').get('nodes')

    if filters:
        filtered_issues = []
        for node in nodes:
            if filters.get('open_only') and node['content'].get('state') != 'OPEN':
                continue
           
            filtered_issues.append(node)

        nodes = filtered_issues

    issues = issues + nodes

    if pageinfo.get('hasNextPage'):
        return get_project_issues(
            owner=owner,
            owner_type=owner_type,
            project_number=project_number,
            after=pageinfo.get('endCursor'),
            filters=filters,
            issues=issues,
            duedate_field_name=duedate_field_name
        )

    return issues

def load_due_date_history(filename='due_date_history.json'):
    """
    Load the due date history from a JSON file.

    Args:
        filename (str): The name of the file to load the history from.

    Returns:
        dict: A dictionary with issue IDs as keys and due dates as values.
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return an empty dictionary if the file does not exist
        return {}

def save_due_date_history(due_date_history, filename='due_date_history.json'):
    """
    Save the due date history to a JSON file.

    Args:
        due_date_history (dict): A dictionary with issue IDs as keys and due dates as values.
        filename (str): The name of the file to save the history to.
    """
    with open(filename, 'w') as f:
        json.dump(due_date_history, f, indent=4)


def filter_issues_with_due_dates(issues, duedate_field_name):
    filtered_issues = []
    for issue in issues:
        field_value = issue.get('fieldValueByName')
        if field_value:  # Ensure field_value is not None
            due_date = field_value.get('date')
            if due_date:  # Only include issues with a due date
                filtered_issues.append(issue)
    return filtered_issues




def get_due_date_changes(issues, due_date_history):
    """
    Compare the current due dates of issues with previously recorded due dates and identify changes.

    Args:
        issues (list): List of issues where each issue is a dictionary with due date information.
        due_date_history (dict): Dictionary where keys are issue IDs and values are previously recorded due dates.

    Returns:
        list: List of tuples where each tuple contains an issue ID and its new due date if the due date has changed.
    """
    changes = []

    for issue in issues:
        issue_id = issue.get('id')
        new_due_date = issue.get('fieldValueByName', {}).get('date')
        old_due_date = due_date_history.get(issue_id)

        # Check if there is a change in due date
        if new_due_date != old_due_date:
            changes.append((issue_id, new_due_date))

    # Update the due date history with the current due dates
    updated_due_date_history = {issue_id: new_due_date for issue_id, new_due_date in changes}
    save_due_date_history({**due_date_history, **updated_due_date_history})

    return changes



def add_issue_comment(issueId, comment):
    mutation = """
    mutation AddIssueComment($issueId: ID!, $comment: String!) {
        addComment(input: {subjectId: $issueId, body: $comment}) {
            clientMutationId
        }
    }
    """

    variables = {
        'issueId': issueId,
        'comment': comment
    }

    try:
        response = requests.post(
            config.api_endpoint,
            json={"query": mutation, "variables": variables},
            headers={"Authorization": f"Bearer {config.gh_token}"}
        )
        data = response.json()

        if 'errors' in data:
            logging.error(f"GraphQL mutation errors: {data['errors']}")

        return data.get('data')

    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return {}
