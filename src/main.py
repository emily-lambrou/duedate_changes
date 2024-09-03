from logger import logger
import requests
import config
import utils
import graphql

def notify_due_date_changes():
    due_date_history = graphql.load_due_date_history()
    issues = graphql.get_project_issues(
        owner=config.repository_owner,
        owner_type=config.repository_owner_type,
        project_number=config.project_number,
        duedate_field_name=config.duedate_field_name
    )

    if not issues:
        logger.info('No issues found')
        return

    issues_with_due_dates = graphql.filter_issues_with_due_dates(issues, config.duedate_field_name)
    changes = graphql.get_due_date_changes(issues_with_due_dates, due_date_history)

    for issue_id, new_due_date in changes:
        comment = f"The due date has been updated to {new_due_date}."
        if not config.dry_run:
            graphql.add_issue_comment(issue_id, comment)

        logger.info(f'Comment added to issue with ID {issue_id}. Due date updated to {new_due_date}')


def main():
    logger.info('Process started...')
    if config.dry_run:
        logger.info('DRY RUN MODE ON!')

    notify_due_date_changes()
   

if __name__ == "__main__":
    main()
