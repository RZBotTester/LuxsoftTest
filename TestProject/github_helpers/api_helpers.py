"""``
This module contains a group of classes and methods to
work with GitHub API using requests library.

Author: Roman Zanevski
"""
import requests
import json

class GithubAuth:
    """Class to authenticate user in GitHub API"""
    def __init__(self, username, token, url):
        
        self._username = username
        self._token = token
        self._url = url
    
    @property
    def username(self):
        return self._username
    
    @property
    def token(self):
        return self._token
    
    @property
    def url(self):
        return self._url
    
    def authenticate(self):
        return requests.get('{url}/user'.format(url = self._url), auth = (self._username, self._token))



class GithubOperator:
    '''Base class for all operators to work with GitHub API'''
     
    def __init__(self, auth):
        self._auth = auth
        self._repo_name = None
        self._headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer {token}'.format(token = self._auth.token),
        }



class RepoOperator(GithubOperator):
    """Repo operator for testing purposes (Extend this class to implement more methods)"""
    def __init__(self, auth):
        super().__init__(auth)

    
    def create_repo(self, repo_name):
        payload = {
            'name': repo_name,
            'description': 'This is a test repo',
            'homepage': 'https://github.com',
            'private': False,
            'is_template': True,
            'auto_init': True,
        }
        print('creating_repo https://github.com/{user}/{repo}'.format(user = self._auth.username, repo = repo_name))
        return requests.post(url = '{url}/user/repos'.format(url=self._auth.url), 
                             headers = self._headers, 
                             data = json.dumps(payload))
    

    def delete_repo(self):
        #Implement logic to delete repo
        print('delete_repo')
   
        
class BranchOperator(GithubOperator):
    '''Branch operator for testing purposes (Extend this class to implement more methods)'''
    def __init__(self, auth):
        super().__init__(auth)
    
            
    def create_branch(self, branch_name, repo_name):

        url_refs = "{url}/repos/{repo_owner}/{repo_name}/git/refs".format(
            url = self._auth.url, 
            repo_owner = self._auth.username, 
            repo_name = repo_name)
        
        url_heads = url_refs + "/heads"
        
        branches = requests.get(url_heads, headers=self._headers).json()
        branch, sha = branches[-1]['ref'], branches[-1]['object']['sha']
        
        payload = {
            "ref": "refs/heads/{new_branch}".format(new_branch=branch_name),
            "sha": sha
        }
        return requests.post(url = url_refs,
                            data = json.dumps(payload),
                            headers = self._headers)


class CommitOperator(GithubOperator):
    '''Commit operator for testing purposes (Extend this class to implement more methods)'''
    def __init__(self, auth):
        super().__init__(auth)
        
    def create_commit_auto_generated(self, repo_name, branch_name, file_name, file_content):
        c_url = "{g_url}/repos/{repo_owner}/{repo_name}/contents/{file_name}".format(
            g_url=self._auth.url, 
            repo_owner=self._auth.username, 
            repo_name=repo_name, 
            file_name=file_name)
        
        payload = {
            'message': 'Test commit',
            'content': file_content,
            'branch': branch_name,
        }
        return requests.put(url = c_url,
                            headers = self._headers, 
                            data = json.dumps(payload))
        
        
class PullRequestOperator(GithubOperator):
    '''Pull request operator for testing purposes (Extend this class to implement more methods)'''
    def __init__(self, auth):
        super().__init__(auth)
    
    def create_pull_requests_to_main(self, branch_name, repo_name):
        pr_url = '{g_url}/repos/{repo_owner}/{repo_name}/pulls'.format(
            g_url = self._auth.url, 
            repo_owner = self._auth.username, 
            repo_name = repo_name)
        
        payload = {
            'title': 'Test PR',
            'body': 'This is a test PR',
            'head': branch_name,
            'base': 'main',
        }
        return requests.post(url = pr_url, 
                             headers = self._headers, 
                             data = json.dumps(payload))