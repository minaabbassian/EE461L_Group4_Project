**Link to Heroku App:** https://final-project-group-8.herokuapp.com/

**User Instructions:** 
- First, user will see the Login / Signup form where they should enter the desired Username and Password for their account.
- Once logged-in, the user is shown the Projects page, where they can either create a new project or access an existing one by unique ID.
- Creating a new project or accessing an existing one will load the HW Set Form, displaying availability of HW Sets and providing fields for checkout / checkin of HW Sets. 
- Within the HW Set Form, at the top-right corner there is a button to Switch Project, which will return the user to the Projects page.
- At any time while the user is logged in, the top-right corner will have buttons to Download Runnable DataSets and to Logout, which open the Downloads form and log-out the user, respectively.
- The Downloads form displays 10 datasets from PhysioNet with direct links to download a zip file of the data to the user's local machine.
- Within the Downloads form, the top-right corner has buttons to Return to the HW Set Form, to Switch Project, or to Logout.

**Known Issues:**
- Currently have no encryption mechanism for username/password.
- Error in displaying preview of dataset in Downloads form.
- After clicking Logout and being returned to the home page, the user can still manually navigate to other forms. Session is not being cleared properly.