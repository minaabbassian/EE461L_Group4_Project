import app
import pytest

# ideally, would have separate database for testing
# - not exactly necessary on a PoC application, 
# - here, we test with the standard mongodb connection

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

# test downloads page for expected content
def test_downloads(client):
    html = client.get('/download').data.decode()
    assert "<u>Download and Test with DataSets from Physionet!</u>" in html
    assert ".zip" in html

# test signup an existing user
def test_signup_existing(client):
    html = client.post('/form_signup', data=dict(
        username="james",
        password="password"
    ), follow_redirects=True).data.decode()
    assert "<h2><b>Login Form</b></h2>" in html
    assert "<i>Username Taken!</i>" in html

# test create project with empty fields
def test_create_project_missing(client):
    html = client.post('/form_createproject', data=dict(
        projectName="",
        projectID="8675309",
        description="a description"), follow_redirects=True).data.decode()
    assert "<h2 class=\"form_label\">Create Project</h2>" in html
    assert "<i>Please enter a Project Name!</i>" in html

    html = client.post('/form_createproject', data=dict(
        projectName="a name",
        projectID="",
        description="a description"), follow_redirects=True).data.decode()
    assert "<h2 class=\"form_label\">Create Project</h2>" in html
    assert "<i>Please enter a Project ID!</i>" in html

    html = client.post('/form_createproject', data=dict(
        projectName="a name",
        projectID="8675309",
        description=""), follow_redirects=True).data.decode()
    assert "<h2 class=\"form_label\">Create Project</h2>" in html
    assert "<i>Please enter a Project Description!</i>" in html

# test create project with existing ID
def test_create_project_existing(client):
    html = client.post('/form_createproject', data=dict(
        projectName="a name",
        projectID="8675309",
        description="a description"), follow_redirects=True).data.decode()
    assert "<h2 class=\"form_label\">Create Project</h2>" in html
    assert "<i>ProjectID taken!</i>" in html

# test sign in to project
def test_project_login(client):
    html = client.post('/form_signintoproject', data=dict(
        projectID="8675309"), follow_redirects=True).data.decode()
    assert "<h1 class=\"form_label\"><u>HW SET FORM</u></h1>" in html
    assert "<u>Project Name: test_project_pytest</u>" in html

# test checkout HWSets
def test_checkout_hwset_1(client):
    client.post('/form_signintoproject', data=dict(
        projectID="8675309"), follow_redirects=True)
    # missing projectID
    html = client.post('/form_checkout1', data=dict(
        projID=""), follow_redirects=True).data.decode()
    assert "Please enter Project ID" in html
    # incorrect projectID
    html = client.post('/form_checkout1', data=dict(
        projID="0"), follow_redirects=True).data.decode()
    assert "Please enter the correct Project ID" in html
    # amount not a number
    html = client.post('/form_checkout1', data=dict(
        projID="8675309",
        set1amount="aaa"), follow_redirects=True).data.decode()
    assert "Please enter a Valid Number" in html
    # amount a negative number
    html = client.post('/form_checkout1', data=dict(
        projID="8675309",
        set1amount=-20), follow_redirects=True).data.decode()
    assert "Please enter a valid number" in html
    # checkout 0
    amount = app.getCheckedOutHWSet1("8675309")
    html = client.post('/form_checkout1', data=dict(
        projID="8675309",
        set1amount=0), follow_redirects=True).data.decode()
    assert "valid!" in html
    assert amount == app.getCheckedOutHWSet1("8675309")
    # checkout total availability + 1
    availability = app.remainingHWSet1()
    html = client.post('/form_checkout1', data=dict(
        projID="8675309",
        set1amount=availability+1), follow_redirects=True).data.decode()
    assert "invalid!" in html
    assert availability == app.remainingHWSet1()
    # checkout total availability
    availability = app.remainingHWSet1()
    html = client.post('/form_checkout1', data=dict(
        projID="8675309",
        set1amount=availability), follow_redirects=True).data.decode()
    assert "valid!" in html
    assert "Availability of HWSet1:" not in html

def test_checkout_hwset_2(client):
    client.post('/form_signintoproject', data=dict(
        projectID="8675309"), follow_redirects=True)
    # missing projectID
    html = client.post('/form_checkout2', data=dict(
        projID=""), follow_redirects=True).data.decode()
    assert "Please enter Project ID" in html
    # incorrect projectID
    html = client.post('/form_checkout2', data=dict(
        projID="0"), follow_redirects=True).data.decode()
    assert "Please enter the correct Project ID" in html
    # amount not a number
    html = client.post('/form_checkout2', data=dict(
        projID="8675309",
        set2amount="aaa"), follow_redirects=True).data.decode()
    assert "Please enter a valid number" in html
    # amount a negative number
    html = client.post('/form_checkout2', data=dict(
        projID="8675309",
        set2amount=-20), follow_redirects=True).data.decode()
    assert "Please enter a valid number" in html
    # checkout 0
    amount = app.getCheckedOutHWSet2("8675309")
    html = client.post('/form_checkout2', data=dict(
        projID="8675309",
        set2amount=0), follow_redirects=True).data.decode()
    assert "valid!" in html
    assert amount == app.getCheckedOutHWSet2("8675309")
    # checkout total availability + 1
    availability = app.remainingHWSet2()
    html = client.post('/form_checkout2', data=dict(
        projID="8675309",
        set2amount=availability+1), follow_redirects=True).data.decode()
    assert "invalid!" in html
    assert availability == app.remainingHWSet2()
    # checkout total availability
    availability = app.remainingHWSet2()
    html = client.post('/form_checkout2', data=dict(
        projID="8675309",
        set2amount=availability), follow_redirects=True).data.decode()
    assert "valid!" in html
    assert "Availability of HWSet2:" not in html

# test checkin HWSets
def test_checkin_hwset_1(client):
    client.post('/form_signintoproject', data=dict(
        projectID="8675309"), follow_redirects=True)
    # missing projectID
    html = client.post('/form_checkin1', data=dict(
        projID=""), follow_redirects=True).data.decode()
    assert "Please enter Project ID" in html
    # incorrect projectID
    html = client.post('/form_checkin1', data=dict(
        projID="0"), follow_redirects=True).data.decode()
    assert "Please enter the correct Project ID" in html
    # amount not a number
    html = client.post('/form_checkin1', data=dict(
        projID="8675309",
        set1amount="aaa"), follow_redirects=True).data.decode()
    assert "Please enter a valid number" in html
    # amount a negative number
    html = client.post('/form_checkin1', data=dict(
        projID="8675309",
        set1amount=-20), follow_redirects=True).data.decode()
    assert "Please enter a valid number" in html
    # checkin 0
    amount = app.getCheckedOutHWSet1("8675309")
    html = client.post('/form_checkin1', data=dict(
        projID="8675309",
        set1amount=0), follow_redirects=True).data.decode()
    assert "valid!" in html
    assert amount == app.getCheckedOutHWSet1("8675309")
    # checkin total amount
    amount = app.getCheckedOutHWSet1("8675309")
    html = client.post('/form_checkin1', data=dict(
        projID="8675309",
        set1amount=amount), follow_redirects=True).data.decode()
    assert "valid!" in html
    assert "Number of HWSet1 Checked Out: none" in html

def test_checkin_hwset_2(client):
    client.post('/form_signintoproject', data=dict(
        projectID="8675309"), follow_redirects=True)
    # missing projectID
    html = client.post('/form_checkin2', data=dict(
        projID=""), follow_redirects=True).data.decode()
    assert "Please enter Project ID" in html
    # incorrect projectID
    html = client.post('/form_checkin2', data=dict(
        projID="0"), follow_redirects=True).data.decode()
    assert "Please enter the correct Project ID" in html
    # amount not a number
    html = client.post('/form_checkin2', data=dict(
        projID="8675309",
        set2amount="aaa"), follow_redirects=True).data.decode()
    assert "Please enter a valid number" in html
    # amount a negative number
    html = client.post('/form_checkin2', data=dict(
        projID="8675309",
        set2amount=-20), follow_redirects=True).data.decode()
    assert "Please enter a valid number" in html
    # checkin 0
    amount = app.getCheckedOutHWSet2("8675309")
    html = client.post('/form_checkin2', data=dict(
        projID="8675309",
        set2amount=0), follow_redirects=True).data.decode()
    assert "valid!" in html
    assert amount == app.getCheckedOutHWSet2("8675309")
    # checkin total amount
    amount = app.getCheckedOutHWSet2("8675309")
    html = client.post('/form_checkin2', data=dict(
        projID="8675309",
        set2amount=amount), follow_redirects=True).data.decode()
    assert "valid!" in html
    assert "Number of HWSet2 Checked Out: none" in html


def test_check_out_and_in(client):
    # check out 1 and check in 1 from each HWSet
    client.post('/form_signintoproject', data=dict(
        projectID="8675309"), follow_redirects=True)
    amount = app.getCheckedOutHWSet1("8675309")
    html = client.post('/form_checkout1', data=dict(
        projID="8675309",
        set1amount=1), follow_redirects=True).data.decode()
    assert "valid!" in html
    
    html = client.post('/form_checkin1', data=dict(
        projID="8675309",
        set1amount=1), follow_redirects=True).data.decode()
    assert "valid!" in html
    assert amount == app.getCheckedOutHWSet1("8675309")

    amount = app.getCheckedOutHWSet2("8675309")
    html = client.post('/form_checkout2', data=dict(
        projID="8675309",
        set2amount=1), follow_redirects=True).data.decode()
    assert "valid!" in html
    
    html = client.post('/form_checkin2', data=dict(
        projID="8675309",
        set2amount=1), follow_redirects=True).data.decode()
    assert "valid!" in html
    assert amount == app.getCheckedOutHWSet2("8675309") 