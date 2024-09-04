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

        due_date = issue.get('fieldValueByName', {}).get('date')
        issue_title = issue['title']
     
        if not due_date:
            logger.info(f'No due date found for issue {issue_title}')
            continue
        
        expected_comment = f"The due date is updated to: {due_date}."
 
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_title, comment_text):
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_duedate_comment(
                    issue=issue,
                    assignees=assignees, 
                    due_date=due_date
                )
                
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment( issue_title, comment)    
                logger.info(f'Comment added to issue with title {issue_title}. Due date is {due_date}')


def main():
    logger.info('Process started...')
    if config.dry_run:
        logger.info('DRY RUN MODE ON!')

    notify_due_date_changes()

if __name__ == "__main__":
    main()

