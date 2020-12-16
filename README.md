# FSND - Capstone Project: HAUS

1.[Motivation](#motivation)

2.[Project setup](#project-setup)

3.[API documentation](#api-documentation)

4.[Roles & Permissions](#roles&permissions)

### Motivation

Haus is a platform that is aimed for use within a mid to large scale housing complex in order to facilitate and encourage neighbourly interaction. As an inhabitant of the building that one lives in, one has the possibility to post an inquiry in a time of need or respond to an inquiry posted by another neighbour that is in need. 

### Project Setup

- Clone the project: 

  `git clone https://github.com/katotopark/haus`

- Install the dependencies:

  `pip install -r requirements.txt`

- Export environment variables:

  `./setup.sh` or `sh  setup.sh` or `bash setup.sh`

- Create Local Database:

  Use `DATABASE_PATH` variable to export the database URI as an environment variable

- Run database migrations:

  `flask db init`

  `flask db migrate`

  `flask db upgrade`

- Run the app:
  
  `flask run`

- Run tests:

  `python test_app.py`

### API Documentation:

- **GET** `/inhabitants`

  Returns a formatted list of all inhabitants.

- **GET** `/inquiries`

Returns a formatted list of all inquiries.

- **POST** `/inquiries`

  Creates a new inquiry provided with inquirer_id, items, and tag.

- **PATCH** `/inquiries/:id`

  Changes inquiry status provided with the id. 

- **DELETE** `/inquiries/:id`

  Deletes an inquiry provided with the id.

### Roles & Permissions:

**GET** `/authorization/url` can be used as a convenience for the reviewer to generate the Auth0 login link in order to acquire an access token. For each role listed below sample login data has also been provided to facilitate the reviewing process.

- Superintendent:

  The role is for the caretaker of the building. 
  
  Permissions: they can *get inhabitants*.

  Sample mail address: `superintendent@superintendent.com`

  Sample password: `hausHAUS1234`

- Inhabitant:

  The role is for the resident of the building. 
  
  Permissions: they can *read, post, delete, patch inquiries*.

  Sample mail address: `inhabitant@inhabitant.com`

  Sample password: `hausHAUS1234`