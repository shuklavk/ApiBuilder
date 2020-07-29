# APIBuilder
This project is live [HERE](https://apibuilder.app/). Original project is in a private repo on Azure Devops. I worked with other teammates, but this README will focus on only my **individual** contributions/experiences. 

## Inspiration
After participating in multiple hackathons, I started noticing a common pattern for the backend: create a server, create the basic CRUD routes, and connect the server to a database. What if we could make a website, that would take your database tables, and do all the steps to create a backend for you? This way you would not have to spend time setting up a server and database, you can focus on the more difficult features. 

Also, we had the idea of making it user friendly for those who do not know how to code. They could use a drag-and-drop frontend html file, and use our service for the backend code. Then, just connect the two sides and voila, a complete web app done in less than 30 minutes. 

We need to stop focusing on the mundane tasks!   

## What it does
Significantly decreases the time it takes someone to create a backend service which consists:
* Database (SQLite)
* CRUD Routes (Node or Flask [your choice!])
* Exportable Javascript Library (No need to worry about the actual routing, if you have no idea what it is! Just pass in the correct parameters in the functions)

The web app bundles all these files and exports as one ZIP file.

### Steps on how to use:
* Pick an API Name 
* Add Route Groups (Same concept of adding tables to a database Ex: Users, Cars, etc)
* Add attributes to the Route Groups (Example for the Users route Group: firstName, lastName, age, isMarried, etc)
* Generate API!
* Connect files to any frontend files (either by importing JS library into the html, or using the routes directly)
* Run app

## How I built it

#### Frontend

Before: 

<img width="568" alt="Screen Shot 2020-07-29 at 1 12 21 AM" src="https://user-images.githubusercontent.com/45616379/88774969-f363d000-d138-11ea-8fc9-6a15a2a43f17.png">

After: 

![Screen Shot 2020-07-29 at 1 16 47 AM](https://user-images.githubusercontent.com/45616379/88775152-34f47b00-d139-11ea-8820-27225582c685.png)

The original website was written in vanilla HTML/CSS all in one page. Also, the original website did not have automatic updates. This meant if you deleted something, you would have to refresh to see the updates. I took on the challenge of completely rehauling the frontend. I designed, developed, and structured this website using React. I also used Fluent UI (Microsoft's UI Library).  

#### Backend

In the backend, I handled the templating system. The backend is written in Python (Flask) with SQLAlchemy to interact with the database. The way that the templating system works is that there are a bunch of string variables which hold the meat of the rendered files. In appropriate locations, where the value is dependent on what the user entered I have the string formatted with "<" and ">". For example, a template would look something like this:

"Hi my name is <<a>name>"
  
Then, I would pass in a tokens dictionary that substitutes all parts of the template strings that are surrounded with "<" and ">" with the entered value from the user. 

## What's next for API Builder

There are many exciting features still in development! Firstly, authentication is the first feature that will be implemented. Currently, the user is tied their localStorage, but we will be having user accounts where you can store multiple APIs rather than just one. 

Another huge thing we are working on is autodeploying VMs. We want to be able to deploy a VM for our potentially paid users, so they can use their routes directly. 
