## Fun-A-Holics

👉 In the time of Zoom meetings and Work from Home environment, searching for fun recreational activities (to do nearby with safety precautions or at home) to uplift the mood has become a necessity and we want to build a scalable cloud solution (using PAAS offered by google cloud platform GCP) to address this problem. This application will provide an interactive Web-Interface to help users find recreational activities (indoor and outdoor) based on criteria such as the number of group members, minimum age/maximum age information, budget, location preferences, category of activities, status of event etc. All the effort of filtering the virtual events or outdoor activities suiting their budget and other requirements will be taken care of by the Fun-A-Holics app. This app will help users find recurring events (like online yoga, gaming) created by us even on days when user created events are limited. In case of outdoor events, we have  included COVID test results as a prerequisite. Only those who successfully submit the negative covid testing results or covid vaccination report at the start of the event are eligible to attend the event. 

#### Team Members:
    Gunda Akshay Kumar (1217179379)
    Kusuma Kumari Vanteru (1217031218)
    Tejaswi Paruchuri (1213268054)

#### Technologies used:

  * 👉 Front-end: HTML5, CSS, Bootstrap
  * 👉 Back-end: Python Flask framework
  * 👉 Google cloud platform PAAS services:
              * Google App Engine
              * Google Cloud Scheduler
              * Google Cloud SQL
  * 👉 APIs:
              * Google Mail API
  * 👉  Database:
              * MySQL

#### To run the application locally
👉 Use the following commands to run the application locally.
```
sudo apt-update 
sudo apt-upgrade 
sudo apt install python3-pip 
pip3 --version 
python3 -m pip install -r requirements
python run.py
```
👉 It runs the application on 5000 port which can be accessed using localhost:5000 if running on the local machine<br>

#### To Deploy the application on Google App Engine (GAE)
👉 Deploy the code in google app engine instance and execute gcloud app deploy. It will install all the required dependencies that are mentioned in requirements.txt and on successful deployment generates a url which can be used to access application.
```
gcloud app deploy
```
👉 After that, execute gcloud app deploy cron.yaml to create scheduled jobs.
```
gcloud app deploy cron.yaml
```
