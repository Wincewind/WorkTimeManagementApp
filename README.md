# WorkTimeManagementApp
A web app to record work time for projects and keep track of customer invoicing and elapsed workload. Developers record work time done for customer projects which are managed by managers. Projects can have workload or cost limits which cause alerts based on the accumulated invoicing.

Current progress can be viewed online at http://tsoha-worktime-manager.fly.dev/

When signing in, the site might crash sometimes. Reloading the page/signing in again should work. I think it has something to do with the time it takes for the db connections to wake up with fly.io after the apps have been idle for long enough.   

## How to setup and run locally (tested in Uni Linux environment, some steps/commands might be different on Windows or Mac):
1.  Clone the repository or download it as a zip:
```bash
git clone https://github.com/Wincewind/WorkTimeManagementApp.git
```

2.  In the project folder, create a virtual environment and activate it
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```

3.  Install required modules in the virtual env
```bash
pip install -r requirements.txt
```

4.  Start your PostgreSQL database if it's not running yet and create the required tables in psql using the schema.sql in the root folder.

**Note that this will delete any existing tables of the same name!**
```bash
psql < schema.sql
```

5.  Create .env file for the environment variables and assign appropriate values for them

The values in .env.example should work if it's just renamed to ".env", but generating your own secure SECRET_KEY is **highly** recommended!

6.  The app should now be ready to run start. Remember to change active directory to src folder before running flask
```bash
cd src
```

## App features currently implemented are marked with a ✔:

- [x] Simple visuals created using Bootstrap ver 5.2 and customized when needed to create a more personalized look.
- [x] Navigation bar where different pages and their functions can be selected.
  - [x] With insufficient user role level, users can't access some pages (e.g. developer shouldn't access customer or project management)  and these navbar selections are also disabled.
  - [x] Add navbar to the layout.html.
- [x] Home Page view where 
  - [x] tasks can be created
  - [x] a weekday table, that shows user's recorded tasks for that day.
  - [x] date selection that can be used to change the week to display.
  - [x] task cards can be clicked to open a menu to edit the task.
- [x] Users can login to the app and create new developer and manager level credentials.
  - [ ] customer role.
- Developers and managers can
  - [x] add
  - [x] remove
  - [x] modify

  done tasks towards a customer's projects.
  - [x] Users see only their tasks on the home page view.
  - [x] Developers can only modify their own tasks.
- [ ] Statistical view where users can query for customer and project details from specific period of time.
- [x] The type of the work has a specific cost allocated to it. 
  - [ ] senior developer modifier to this cost.
  - [ ] This cost will affect the invoicing for that project's customer.
- [x] Project's can have cost limits 
  - [ ] that will cause alerts if the project invoicing is nearing that limit.
  - [x] These limits can also be set on workload in which case the time is measured.
  - [ ] When applying cost or hour limit to project, the current recorded hour/cost balance is displayed beside it.
- [x] Customers can be created, modified or removed by managers at which point the customer and its projects are set to visible = FALSE.
  - [x] When set invisible, customers and projects won't appear in selections, but any existing marked tasks will be visible.
- [x] Projects can be created, edited or removed.
- A task consists of 
  - [x] amount of the work in hours and minutes
  - [x] date, when the work was done
  - [x] customer
  - [x] project
  - [x] task type
  - [x] invoiceable, a checkbox selection
  - [x] Note section for description of the done work
