# WorkTimeManagementApp
A web app to record work time for projects and keep track of customer invoicing and elapsed workload. Developers record work time done for customer projects which are managed by managers. Projects can have workload or cost limits which cause alerts based on the accumulated invoicing.

Planned app features are aimed to include:
- Users can login to the app and create new developer, manager (and maybe also customer) credentials.
- Developers and managers can add, remove and modify done tasks towards a customer's projects.
  - Developers can only modify their own tasks.
  - They can also view statistics of all done work for a specific customer or project over a period of time.
- The type of the work has a specific cost allocated to it as well as if the developer doing the work is senior or not.
  - This cost will affect the invoicing for that project's customer.
- Project's can have cost limits that will cause alerts if the project invoicing is nearing that limit.
  - These limits can also be set on workload in which case the time is measured.
- Customer's or projects can be modified or removed by managers at which point the done work will be assigned to a customer/project that can't otherwise be selected when inputting work time.
- A task consists of 
  - amount of the work in hours and minutes
  - date, when the work was done
  - customer
  - project
  - task type
  - invoiceable, a checkbox selection
  - Note section for description of the done work
