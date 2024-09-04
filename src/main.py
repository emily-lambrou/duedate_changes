from logger import logger
import requests
import config
import utils
import graphql

def notify_due_date_changes():
    if config.is_enterprise:
        issues = graphql.get_project_issues(
            owner=config.repository_owner,
            owner_type=config.repository_owner_type,
            project_number=config.project_number,
            duedate_field_name=config.duedate_field_name,
            filters={'open_only': True}
        )
    else:
        # Get the issues
        issues = graphql.get_repo_issues(
            owner=config.repository_owner,
            repository=config.repository_name,
            duedate_field_name=config.duedate_field_name
        )

    # Check if there are issues available
    if not issues:
        logger.info('No issues have been found')
        return

    for projectItem in issues:
        issue = projectItem['content']

        # Get the list of assignees
        assignees = issue.get('assignees', {}).get('nodes', [])

        issue_id = issue['id']
        due_date = issue.get('fieldValueByName', {}).get('date')

        if not due_date:
            logger.info(f'No due date found for issue {issue_id}')
            continue
        
        # Get all comments on the issue
        comments = graphql.get_all_issue_comments(issue_id)

        # Prepare the expected comment text
        expected_comment = f"The due date is updated to: {due_date}."

        # Check if the due date is already mentioned in any comment
        if any(expected_comment in comment for comment in comments):
            logger.info(f"Due date {due_date} already mentioned in issue {issue_id}. Skipping...")
        else:
            # Prepare comment using the utils function
            comment_text = utils.prepare_duedate_comment(issue, assignees, due_date)

            # Directly notify about the due date
            if not config.dry_run:
                graphql.add_issue_comment(issue_id, comment_text)
            logger.info(f'Comment added to issue with ID {issue_id}. Due date is {due_date}')


def main():
    logger.info('Process started...')
    if config.dry_run:
        logger.info('DRY RUN MODE ON!')

    notify_due_date_changes()

if __name__ == "__main__":
    main()

