
USER GUIDE:

ATTENTION USERS! Welcome to our final project! 
A user can use this application to create and manage software projects.
A user can create a login upon first use, and then continue to use this to login to the application in the future.
Once a user is logged in, then they will be presented with a project page.
On this project page, a user can either create a new project with a name and ID, or a user can log into an existing
project (created by either that user or another user) to upload their new code given they possess the respective ID.
Furthermore, once a user enters a project, they can check out certain hardware sets to be able to test their code. 
The hardware set page should give an option to check in or check out hardware sets based upon the availability.

Also, there is a page where users can directly download datasets from physionet in order to test their own code.
There should also be functionality to logout, switch user, switch project, go back a page, etc. on each page.

So, Users should get started!

Minimum hardware and software requirements:
All you need is access to a web application through google chrome, safari, firefox, etc. with running network

How to Start:
Begin by clicking on this link to our app!
Link to Heroku App: https://final-project-group-8.herokuapp.com/

Walkthrough and Screenshots of main features:

![image](https://user-images.githubusercontent.com/45637628/116601222-de96b180-a8ef-11eb-976f-1840f0baaf71.png)

First, one will sign-up/login. This is an example of a possible input.
![image](https://user-images.githubusercontent.com/45637628/116601331-fff79d80-a8ef-11eb-8dea-7994b9a0c4a3.png)

Next, you will be presented with the project login page. Verify that your username is at the top! 
![image](https://user-images.githubusercontent.com/45637628/116601408-19004e80-a8f0-11eb-9f55-3823597212d5.png)

You can either create a project or sign into one. This is an example of a possible input.
![image](https://user-images.githubusercontent.com/45637628/116601503-333a2c80-a8f0-11eb-9ebc-7bc27cfd3c15.png)

Next, you will be presented with the hardware sets. You can either check out or check in sets based upon the availability's displayed at the top. 
You will input the number you want checked in or out as well as the Project ID that you are in. 
![image](https://user-images.githubusercontent.com/45637628/116601626-51a02800-a8f0-11eb-8cfb-3bcafb497216.png)

AS you check in or check out, you will see the availabilities update.

![image](https://user-images.githubusercontent.com/45637628/116601847-90ce7900-a8f0-11eb-9fdc-e6ae88b453a7.png)

These are examples of potential outputs displayed at the top.

Next, at the top, you may have noticed the link to the page "Download Runnable DataSets". Upon clicking on this, there is a list of datasets from physionet displayed with their descriptions. You can directly click on the link, and then the downloads should begin immediately. This is used for testing. 
![image](https://user-images.githubusercontent.com/45637628/116601947-ab085700-a8f0-11eb-8f81-ec4891a607ef.png)

After all of this, at the top, there are selections to return, switch project, or logout. This is your turn to play around with our application for your best use!
![image](https://user-images.githubusercontent.com/45637628/116602091-df7c1300-a8f0-11eb-8859-52a7b6354e58.png)


Explanations of Error Messages:
There could occur error messages based on types of input.
For example, if you input the wrong login, there can appear "invalid password" or "invalid username" - self explanatory
![image](https://user-images.githubusercontent.com/45637628/116606858-f160b480-a8f6-11eb-9374-9f6c332f2bcc.png)


Also, if you enter a project ID that does not exist, it will alert "ProjectId not found", and if you create a project with an existing ID, it should show 
"ProjectID taken"

![image](https://user-images.githubusercontent.com/45637628/116607120-3e448b00-a8f7-11eb-8a7c-832f533dfd5d.png)



Futhermore, the hardware set page should alert with errors that display "valid" or "invalid" based upon checkout and checkin requests. 


Troubleshooting and Questions:

Contact Sarah Orsak

sarahorsak@utexas.edu

214-592-2292 

For further questions or development problems. 


IMPLEMENTATION INFORMATION:

Databases (Using MongoDB): 
Logininfo
projectinfo
HWinfo
currentinfo

Logininfo 
Collection: userinfo (stores username and password for every user) 
![image](https://user-images.githubusercontent.com/48300313/116608126-713b4e80-a8f8-11eb-9bba-b2dfd261a68f.png)

projectinfo
Collection: projectID (stores project name, project description, project ID, #HWSet1 checked out, and #HWSet2 checked out for every project created)

HWinfo 
Collection: HWSets (stores name of HWSet and #available of each HWSet)

currentinfo
Collection: currentsession (stores the current username of the session and the projectID of the current project in session)

FrontEnd implemented with HTML
BackEnd implemented with Python Flask
Deployed to Heroku

