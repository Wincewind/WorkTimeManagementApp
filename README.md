# WorkTimeManagementApp
A web app to record work time for projects and keep track of customer invoicing and elapsed workload. Developers record work time done for customer projects which are managed by managers. Projects can have workload or cost limits which cause alerts based on the accumulated invoicing.

## App features currently implemented are marked with a ✔:
- [x] Users can login to the app and create new developer and manager level credentials.
  - [ ] customer role.
- Developers and managers can
  - [x] add
  - [ ] remove
  - [ ] modify

  done tasks towards a customer's projects.
  - [x] Users see only their tasks on the home page view.
  - [ ] Developers can only modify their own tasks.
- [ ] Statistical view where users can query for customer and project details from specific period of time.
- [x] The type of the work has a specific cost allocated to it. 
  - [ ] senior developer modifier to this cost.
  - [ ] This cost will affect the invoicing for that project's customer.
- [x] Project's can have cost limits 
  - [ ] that will cause alerts if the project invoicing is nearing that limit.
  - [ ] These limits can also be set on workload in which case the time is measured.
- [x] Customers can be created, modified or removed by managers at which point the customer and its projects are set to visible = FALSE.
  - [x] When set invisible, customers and projects won't appear in selections, but any existing marked tasks will be visible.
- [ ] Projects can be created, edited or removed.
- A task consists of 
  - [x] amount of the work in hours and minutes
  - [x] date, when the work was done
  - [x] customer
  - [x] project
  - [x] task type
  - [x] invoiceable, a checkbox selection
  - [x] Note section for description of the done work
