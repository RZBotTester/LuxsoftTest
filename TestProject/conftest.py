import pytest

def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="https://api.github.com",
                     help="GitHub API URL")
    parser.addoption("--user", action="store", default="user",
                     help="GitHub user")
    parser.addoption("--token", action="store", default="token",
                     help="GitHub password")
    
@pytest.fixture
def get_url_name_token(request):
    url_name_token = {}
    url_name_token['url'] = request.config.getoption("--url")
    url_name_token['user'] = request.config.getoption("--user")
    url_name_token['token'] = request.config.getoption("--token")
    return url_name_token