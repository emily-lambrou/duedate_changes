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

    comment += f'Due Date updated.'
    logger.info(f'Issue {issue["title"]} | {comment}')

    return comment

