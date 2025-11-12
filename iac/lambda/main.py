import json
import os
import hmac
import hashlib
import requests
from datetime import datetime

# Environment variables
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')


def verify_signature(payload_body, signature_header):
    """Verify that the webhook came from GitHub"""
    if not signature_header or not WEBHOOK_SECRET:
        return False

    hash_object = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        msg=payload_body.encode('utf-8'),
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)


def create_check_run(repo_owner, repo_name, head_sha, status, conclusion=None):
    """Create or update a GitHub check run"""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/check-runs"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "name": "Test Check",
        "head_sha": head_sha,
        "status": status,
    }

    if conclusion:
        data["conclusion"] = conclusion
        data["completed_at"] = datetime.utcnow().isoformat() + "Z"

    if status == "in_progress":
        data["started_at"] = datetime.utcnow().isoformat() + "Z"
        data["output"] = {
            "title": "Running tests",
            "summary": "Test check is in progress..."
        }
    elif conclusion == "success":
        data["output"] = {
            "title": "Tests passed",
            "summary": "All tests have passed successfully! ✅"
        }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def has_test_label(issue):
    """Check if the issue has the 'test' label"""
    labels = issue.get('labels', [])
    return any(label.get('name', '').lower() == 'test' for label in labels)


def lambda_handler(event, context):
    """Main Lambda handler function"""

    try:
        # Get the request body and headers
        body = event.get('body', '{}')
        headers = event.get('headers', {})

        # Verify webhook signature
        signature = headers.get('X-Hub-Signature-256', headers.get('x-hub-signature-256'))
        if not verify_signature(body, signature):
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Invalid signature'})
            }

        # Parse the payload
        payload = json.loads(body)

        # Get event type
        event_type = headers.get('X-GitHub-Event', headers.get('x-github-event'))

        print(f"Received event type: {event_type}")

        # Handle issue events
        if event_type == 'issues':
            action = payload.get('action')
            issue = payload.get('issue', {})
            repository = payload.get('repository', {})

            print(f"Issue action: {action}")
            print(f"Issue number: {issue.get('number')}")

            # Check if issue has 'test' label
            if has_test_label(issue):
                print("Issue has 'test' label - running checks")

                # Get repository info
                repo_owner = repository.get('owner', {}).get('login')
                repo_name = repository.get('name')

                # For issues, we need to use the default branch's HEAD SHA
                # In a real scenario, you might want to get this from the PR if it's linked
                default_branch = repository.get('default_branch', 'main')

                # Get the latest commit SHA from the default branch
                branch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{default_branch}"
                branch_response = requests.get(
                    branch_url,
                    headers={
                        "Authorization": f"Bearer {GITHUB_TOKEN}",
                        "Accept": "application/vnd.github.v3+json"
                    }
                )
                head_sha = branch_response.json().get('commit', {}).get('sha')

                # Create check run - in progress
                create_check_run(repo_owner, repo_name, head_sha, "in_progress")

                # TODO: Here you would ping your test endpoint
                # For now, we simulate tests passing
                tests_passed = True

                # Update check run - completed
                conclusion = "success" if tests_passed else "failure"
                create_check_run(repo_owner, repo_name, head_sha, "completed", conclusion)

                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Tests completed successfully',
                        'tests_passed': tests_passed
                    })
                }
            else:
                print("Issue does not have 'test' label - skipping")
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'No test label found, skipping'})
                }

        # Handle pull request events (if you want to support PRs too)
        elif event_type == 'pull_request':
            action = payload.get('action')
            pr = payload.get('pull_request', {})
            repository = payload.get('repository', {})

            # Check if PR has 'test' label
            if has_test_label(pr):
                print("PR has 'test' label - running checks")

                repo_owner = repository.get('owner', {}).get('login')
                repo_name = repository.get('name')
                head_sha = pr.get('head', {}).get('sha')

                # Create check run
                create_check_run(repo_owner, repo_name, head_sha, "in_progress")

                # TODO: Ping test endpoint
                tests_passed = True

                conclusion = "success" if tests_passed else "failure"
                create_check_run(repo_owner, repo_name, head_sha, "completed", conclusion)

                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Tests completed successfully',
                        'tests_passed': tests_passed
                    })
                }

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Event processed'})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }