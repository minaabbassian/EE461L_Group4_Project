import app
import pytest

# init the testing environment
# - creates an app with the TESTING config flag set True
@pytest.fixture
def client():
    app.app.testing = True
    client = app.app.test_client()
    yield client


# test the landing page for expected content
def test_landing(client):
    landing = client.get("/") #request the data
    html = landing.data.decode() #convert request to html code

    #check for Login form, submit button
    assert "<h2><b>Login Form</b></h2>" in html
    assert "<button type=\"submit\" value='LOGIN'>Login</button>" in html
    #check for Signup form, submit button
    assert "<h2><b>Signup Form</b></h2>" in html
    assert "<button type=\"submit\" value='SIGNUP'>Sign Up</button>" in html

    #check that the request was successful
    assert landing.status_code == 200
