import pytest
from fixture.application import Application
import json
import os.path

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


#@pytest.fixture(scope="session")
#def app(request):
#    global fixture
#    config = load_config(request.config.getoption("--target"))
#    web_config = config['web']
#    webadmin_config = config['webadmin']
#    browser = request.config.getoption("--browser")
#    fixture = Application(browser=browser, base_url=web_config['baseUrl'])
#    username = webadmin_config['username']
#    password = webadmin_config['password']
#    fixture.session.ensure_login(username, password)

#    def fin():
#        fixture.session.ensure_logout()
#        fixture.destroy()
#    request.addfinalizer(fin)
#    return fixture

#@pytest.fixture(scope="session")
#def app(request):
#    global fixture
#    config = load_config(request.config.getoption("--target"))
#    web_config = config["web"]
#    webadmin_config = config["webadmin"]
#    browser = request.config.getoption("--browser")
#    if fixture is None or not fixture.is_valid():
#        fixture = Application(browser=browser, base_url=web_config['baseUrl'])
#        username = webadmin_config['username']
#        password = webadmin_config['password']
#        fixture.session.ensure_login(username, password)
#    return fixture

@pytest.fixture
def app(request):
    global fixture
    config = load_config(request.config.getoption("--target"))
    browser = request.config.getoption("--browser")
    web_config = config["web"]
    webadmin_config = config["webadmin"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    fixture.session.ensure_login(username=webadmin_config['username'], password=webadmin_config['password'])
    return fixture

@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")
