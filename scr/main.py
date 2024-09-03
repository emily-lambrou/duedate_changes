from logger import logger
import requests
import config
import utils
import graphql

def notify_missing_status():
    if config.is_enterprise:
        issues = graphql.get_project_issues_status(
            owner=config.repository_owner,
            owner_type=config.repository_owner_type,
            project_number=config.project_number,
            status_field_name=config.status_field_name,
            filters={'empty_status': True, 'closed_only': True}
        )
    else:
        # Get the issues
        issues = graphql.get_repo_closed_issues(
            owner=config.repository_owner,
            repository=config.repository_name
        )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    for projectItem in issues:
        issue = projectItem['content']

        # Get the list of assignees
        assignees = issue['assignees']['nodes']

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        issue_id = issue['id']
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue['id'], comment_text):
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue,
                    assignees=assignees, 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue_id, comment)    
                logger.info(f'Comment added to issue {issue_id}')
                
def notify_missing_duedate():
    if config.is_enterprise:
        issues = graphql.get_project_issues_duedate(
            owner=config.repository_owner,
            owner_type=config.repository_owner_type,
            project_number=config.project_number,
            duedate_field_name=config.duedate_field_name,
            filters={'empty_duedate': True, 'closed_only': True}
        )
    else:
        # Get the issues
        issues = graphql.get_repo_closed_issues(
            owner=config.repository_owner,
            repository=config.repository_name
        )
        
    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    for projectItem in issues:
        issue = projectItem['content']

        # Get the list of assignees
        assignees = issue['assignees']['nodes']

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        issue_id = issue['id']
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue,
                    assignees=assignees, 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue_id, comment)    
                logger.info(f'Comment added to issue {issue_id}')

def notify_missing_timespent():
    if config.is_enterprise:
        issues = graphql.get_project_issues_timespent(
            owner=config.repository_owner,
            owner_type=config.repository_owner_type,
            project_number=config.project_number,
            timespent_field_name=config.timespent_field_name,
            filters={'empty_timespent': True, 'closed_only': True}
        )
    else:
        # Get the issues
        issues = graphql.get_repo_closed_issues(
            owner=config.repository_owner,
            repository=config.repository_name
        )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    for projectItem in issues:
        issue = projectItem['content']

        # Get the list of assignees
        assignees = issue['assignees']['nodes']

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        issue_id = issue['id']
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue,
                    assignees=assignees, 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue_id, comment)    
                logger.info(f'Comment added to issue {issue_id}')
          
def notify_missing_release():
    if config.is_enterprise:
        issues = graphql.get_project_issues_release(
            owner=config.repository_owner,
            owner_type=config.repository_owner_type,
            project_number=config.project_number,
            release_field_name=config.release_field_name,
            filters={'empty_release': True, 'closed_only': True}
        )
    else:
        # Get the issues
        issues = graphql.get_repo_closed_issues(
            owner=config.repository_owner,
            repository=config.repository_name
        )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    for projectItem in issues:
        issue = projectItem['content']

        # Get the list of assignees
        assignees = issue['assignees']['nodes']

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        issue_id = issue['id']
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue,
                    assignees=assignees, 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue_id, comment)    
                logger.info(f'Comment added to issue {issue_id}')
      
def notify_missing_estimate():
    if config.is_enterprise:
        issues = graphql.get_project_issues_estimate(
            owner=config.repository_owner,
            owner_type=config.repository_owner_type,
            project_number=config.project_number,
            estimate_field_name=config.estimate_field_name,
            filters={'empty_estimate': True, 'closed_only': True}
        )
    else:
        # Get the issues
        issues = graphql.get_repo_closed_issues(
            owner=config.repository_owner,
            repository=config.repository_name
        )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    for projectItem in issues:
        issue = projectItem['content']

        # Get the list of assignees
        assignees = issue['assignees']['nodes']

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        issue_id = issue['id']
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue,
                    assignees=assignees, 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue_id, comment)    
                logger.info(f'Comment added to issue {issue_id}')
                
def notify_missing_priority():
    if config.is_enterprise:
        issues = graphql.get_project_issues_priority(
            owner=config.repository_owner,
            owner_type=config.repository_owner_type,
            project_number=config.project_number,
            priority_field_name=config.priority_field_name,
            filters={'empty_priority': True, 'closed_only': True}
        )
    else:
        # Get the issues
        issues = graphql.get_repo_closed_issues(
            owner=config.repository_owner,
            repository=config.repository_name
        )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    for projectItem in issues:
        issue = projectItem['content']

        # Get the list of assignees
        assignees = issue['assignees']['nodes']

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        issue_id = issue['id']
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue,
                    assignees=assignees, 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue_id, comment)    
                logger.info(f'Comment added to issue {issue_id}')
      
def notify_missing_size():
    if config.is_enterprise:
        issues = graphql.get_project_issues_size(
            owner=config.repository_owner,
            owner_type=config.repository_owner_type,
            project_number=config.project_number,
            size_field_name=config.size_field_name,
            filters={'empty_size': True, 'closed_only': True}
        )
    else:
        # Get the issues
        issues = graphql.get_repo_closed_issues(
            owner=config.repository_owner,
            repository=config.repository_name
        )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    for projectItem in issues:
        issue = projectItem['content']

        # Get the list of assignees
        assignees = issue['assignees']['nodes']

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        issue_id = issue['id']
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue,
                    assignees=assignees, 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue_id, comment)    
                logger.info(f'Comment added to issue {issue_id}')
                
def notify_missing_week():
    if config.is_enterprise:
        issues = graphql.get_project_issues_week(
            owner=config.repository_owner,
            owner_type=config.repository_owner_type,
            project_number=config.project_number,
            week_field_name=config.week_field_name,
            filters={'empty_week': True, 'closed_only': True}
        )
    else:
        # Get the issues
        issues = graphql.get_repo_closed_issues(
            owner=config.repository_owner,
            repository=config.repository_name
        )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    for projectItem in issues:
        issue = projectItem['content']

        # Get the list of assignees
        assignees = issue['assignees']['nodes']

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        issue_id = issue['id']
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue,
                    assignees=assignees, 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue_id, comment)    
                logger.info(f'Comment added to issue {issue_id}')
    
def main():
    logger.info('Process started...')
    if config.dry_run:
        logger.info('DRY RUN MODE ON!')

    notify_missing_status()
    notify_missing_duedate()
    notify_missing_timespent()
    notify_missing_release()
    notify_missing_estimate()
    notify_missing_priority()
    notify_missing_size()
    notify_missing_week()
  

if __name__ == "__main__":
    main()
