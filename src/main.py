from logger import logger
import requests
import config
import utils
import graphql

def notify_due_date_changes():
    issues = graphql.get_project_issues(
        owner=config.repository_owner,
        owner_type=config.repository_owner_type,
        project_number=config.project_number,
        duedate_field_name=config.duedate_field_name
    )

    if not issues:
        logger.info('No issues found')
        return

    # Filter issues with due dates
    issues_with_due_dates = graphql.filter_issues_with_due_dates(issues, config.duedate_field_name)

    # Iterate over the filtered issues and handle them
    for issue in issues_with_due_dates:
        issue_id = issue.get('id')
        due_date = issue.get('fieldValueByName', {}).get('date')

        # Directly notify about the due date
        comment = f"The current due date is {due_date}."
        if not config.dry_run:
            graphql.add_issue_comment(issue_id, comment)

        logger.info(f'Comment added to issue with ID {issue_id}. Due date is {due_date}')



def main():
    logger.info('Process started...')
    if config.dry_run:
        logger.info('DRY RUN MODE ON!')

    notify_due_date_changes()
   

if __name__ == "__main__":
    main()
