import os
import datetime
import pytest
from pytest_bdd import scenario, given, when, then

from github_helpers.api_helpers import GithubAuth, RepoOperator, BranchOperator, CommitOperator, PullRequestOperator
from workflow_helpers.file_helpers import TextTestFileGenerator

feature_file_dir = 'features'
feature_file_name = 'gitflow.feature'

feature = os.path.abspath(os.path.join(os.path.dirname(
    __file__), '..', feature_file_dir, feature_file_name))


def set_scenario_helpers_and_auth(get_args_to_auth):
    
    url = get_args_to_auth['url']
    user = get_args_to_auth['user']
    token = get_args_to_auth['token']
    
    # scenario pytest variables
    pytest.created_repo = None
    pytest.created_branch = None
    # We can't auth to the github API using the username and password since 13.11.2020 according to 
    # https://docs.github.com/en/rest/overview/other-authentication-methods#via-oauth-and-personal-access-tokens
    # Just use the token instead
    pytest.auth = GithubAuth(user, token, url)
    pytest.repo_operator = RepoOperator(pytest.auth)
    pytest.branch_operator = BranchOperator(pytest.auth)
    pytest.commit_operator = CommitOperator(pytest.auth)
    pytest.pulls_operator = PullRequestOperator(pytest.auth)


@pytest.mark.parametrize(
    ['git_flow_task', 'feature', 'git_flow_feature'],
    [('repo_1_', 'feature', 'feature_1'),
     ('repo_2_', 'bugfix', 'bugfix_1')]
)
@scenario(feature, 'Create a new repo with a feature branch and with a first commit')
def test_create_repo(git_flow_task, feature, git_flow_feature):
    pass


@given('user logs in GitHub using basic authentication')
def user_logs_in_github(get_url_name_token):
    set_scenario_helpers_and_auth(get_url_name_token)
    
    print('\n*authentication')
    auth_response = pytest.auth.authenticate()
    assert auth_response.status_code == 200, 'Authentication failed'


@when('user creates repository with name "<git_flow_task>" + suffix current time')
def user_creates_a_new_repo(git_flow_task):
    print('*user_creates_a_new_repo')
    time_suffix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    create_repo_name = git_flow_task + time_suffix
    
    assert pytest.repo_operator.create_repo(create_repo_name).status_code == 201, 'Repository was not created'
    pytest.created_repo = create_repo_name
    

@when('user creates branch "<feature>/<git_flow_feature>"')
def user_creates_a_new_feature_branch(feature, git_flow_feature):
    print('*user creates branch')
    create_branch_name = '{ftr}/{gf_ftr}'.format(ftr = feature, gf_ftr = git_flow_feature)
    
    assert pytest.branch_operator.create_branch(create_branch_name, 
                                         pytest.created_repo).status_code == 201, 'Branch was not created'
    pytest.created_branch = create_branch_name


@when('user commits auto generated file')
def user_commit_auto_generated():
    print('*user commits auto generated file')
    
    file_name_and_content = TextTestFileGenerator().generate_file_name_and_content()
    
    assert pytest.commit_operator.create_commit_auto_generated(pytest.created_repo, 
                                                        pytest.created_branch, 
                                                        file_name_and_content[0], 
                                                        file_name_and_content[1]).status_code == 201, 'Commit was not created'


@then('user creates pull request to master branch')
def user_creates_a_pull_request():
    print('*user creates pull request to master branch')
    
    assert pytest.pulls_operator.create_pull_requests_to_main(pytest.created_branch, 
                                                       pytest.created_repo).status_code == 201, 'Pull request was not created'
