# nightstand-capstone
a reading app for the Open Library API - capstone project for NSS 

### Overview
nightStand accesses the Open Library API (currently only with a small demo version of the API) to manage a user's reading list (their Nightstand) and participate in reading groups. The user can search for books from the API and add them to their bookshelf, as well as join groups that are reading that book and discuss it through the app. When a user adds a book, they may set due dates for each chapter, which the app uses to suggest certain chapters to be read each day in the dashboard view based on urgency. In that view the user also sees a progress bar for each book based on how many chapters they have completed, along with recent comments made about those books.  In the group view, users can see which chapters each of the members have completed or are late in reading, and get a list of comments only from members of that reading group. 

This app could be used by a person wanting to manage a large backlog of books they want to read or a student managing their reading assignments for school.  The group functionality was designed for a book club or class to keep track of everyone's progress while at the same time providing a forum for discussion.  

### Technology
This app was built with Python and the Django framework, with minimal Javascript with jQuery for interactivity on each view.  My __learning goals__ for this project were to deepen my understanding of Django and its built-in functionality, and to see how much I could do with Django without a front-end framework. Building a REST API with Django along with a front-end framework like React.js (see other examples of that in my other repos) would have been another way to approach creating this app, but I was specifically building this project as an educational experience in Django. 

### Using the app

If you would like to run this app locally follow these instructions (You must have Python installed on your computer, or if you use virtualenv, python will come with the environment):

First, create a directory on your computer where you would like the project to live.  Create a virtual environment inside that directory (I use [virtualenv](https://virtualenv.pypa.io/en/stable/) for this purpose, which you must have installed if you wish to use it):

Mac:
```
virtualenv my-env-name
source my-env-name/bin/activate
```
Windows users need to use `path/to/env/Scripts/activate.bat` to activate the environment

Once your environment is activated, clone the repo into your directory as well:
```
git clone https://github.com/joshdbarton/nightstand-capstone.git
```
Change to that directory and install requirements:

```
cd nightstand
pip install -r requirements.txt
```
Migrate the database and create a superuser:
```
python manage.py makemigrations nightstand_dashboard
python manage.py migrate
python manage.py createsuperuser
```
Run your dev server:
```
python manage.py runserver
```

That's it!  Navigate to http://127.0.0.1:8000/ to start using the app. You can register new users, or use the superuser you already created to log in.  Note that the API contains 15 books for demonstration purposes only. If you would like to see all of the books that are there, search for "e". 

