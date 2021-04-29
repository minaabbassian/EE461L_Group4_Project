Link to Heroku App: https://final-project-group-8.herokuapp.com/

User Guide:
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

Databases: 
Logininfo
projectinfo
HWinfo
currentinfo

Logininfo 
Collection: userinfo (stores usernames and passwords) 

projectinfo
Collection: projectID (stores project name, project description, project ID, #HWSet1 checked out, and #HWSet2 checked out)

HWinfo 
Collection: HWSets (stores name of HWSet and #available of each HWSet)

currentinfo
Collection: currentsession (stores the current username of the session and the projectID of the current project in session)

