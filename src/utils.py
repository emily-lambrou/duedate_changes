import graphql
import config
from logger import logger

def prepare_duedate_comment(issue: dict, assignees: dict, due_date):
    """
    Prepare the comment from the given arguments and return it
    """

    comment = ''
    if assignees:
        for assignee in assignees:
            comment += f'@{assignee["login"]} '
    else:
        logger.info(f'No assignees found for issue #{issue["number"]}')

    comment += f'The Due Date is updated to: {due_date}.'
    logger.info(f'Issue {issue["title"]} | {comment}')

    return comment


def check_comment_exists(issue_title, expected_comment):
    """Check if the comment already exists on the issue."""
    comments = graphql.get_issue_comments(issue_title)
    for comment in comments:
        if expected_comment in comment.get('body', ''):
            return True
    return False
