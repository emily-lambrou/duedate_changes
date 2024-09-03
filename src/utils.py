import graphql
import config
from logger import logger

def prepare_missing_fields_comment(issue: dict, assignees: dict):
    """
    Prepare the comment from the given arguments and return it
    """

    comment = ''
    if assignees:
        for assignee in assignees:
            comment += f'@{assignee["login"]} '
    else:
        logger.info(f'No assignees found for issue #{issue["number"]}')

    comment += f'Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week.'
    logger.info(f'Issue {issue["title"]} | {comment}')

    return comment

