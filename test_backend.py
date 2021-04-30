import app
import pytest

# init the testing environment
# - creates an app with the TESTING config flag set True
@pytest.fixture
def client():
    app.app.testing = True
    client = app.app.test_client()
    yield client

def login(client, username, password):
    return client.post('/form_login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

# test the landing page for expected content
def test_landing(client):
    landing = client.get('/') #request the data
    html = landing.data.decode() #convert request to html code

    #check for Login form, submit button
    assert "<h2><b>Login Form</b></h2>" in html
    assert "<button type=\"submit\" value='LOGIN'>Login</button>" in html
    #check for Signup form, submit button
    assert "<h2><b>Signup Form</b></h2>" in html
    assert "<button type=\"submit\" value='SIGNUP'>Sign Up</button>" in html

    #check that the request was successful
    assert landing.status_code == 200

# test the login functionality
def test_login_correct(client):
    # test login with correct info
    html = login(client, 'james', 'password').data.decode()
    assert "<i>Current User: james</i>" in html
    assert "<h2 class=\"form_label\">Create Project</h2>" in html
    assert "<h2>Sign Into Project</h2>" in html    

def test_login_incorrect_password(client):
    # test login with incorrect password
    html = login(client, 'james', 'pwd').data.decode()
    assert "<h2><b>Login Form</b></h2>" in html
    assert "<i>Invalid Password!</i>" in html
    assert "<h2><b>Signup Form</b></h2>" in html

def test_login_incorrect_username(client):
    # test login with incorrect username
    html = login(client, 'jamess', 'password').data.decode()
    assert "<h2><b>Login Form</b></h2>" in html
    assert "<i>Invalid Username!</i>" in html
    assert "<h2><b>Signup Form</b></h2>" in html

# test logout - should return to landing
def test_logout(client):
    request = logout(client)
    assert client.get('/').data == request.data