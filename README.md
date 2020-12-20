# FSND - Capstone Project: HAUS

The application is deployed via Heroku at [this address](https://haus-fsnd.herokuapp.com/).

1.[Motivation](#motivation)

2.[Project setup](#project-setup)

3.[API documentation](#api-documentation)

4.[Roles & Permissions](#roles&permissions)

### Motivation

Haus is a platform that is aimed for use within a mid to large scale housing complex in order to facilitate and encourage neighbourly interaction. As an inhabitant of the building that one lives in, one has the possibility to post an inquiry in a time of need or respond to an inquiry posted by another neighbour that is in need.

### Project Setup

- Clone the project:

  `git clone https://github.com/katotopark/haus`

- Set up a virtual environment (e.g virtualenv - See [documentation](https://virtualenv.pypa.io/en/stable/)):

  `pip3 install virtualenv`

- Install the dependencies:

  `pip3 install -r requirements.txt`

- Export environment variables:

  `./setup.sh` or `sh setup.sh` or `bash setup.sh`

- Create Local Database:

  Use `DATABASE_URL` variable to export the database URI as an environment variable

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

  Sample request: `curl http://localhost:5000/inhabitants -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"`

  Sample response: `{ "inhabitants": [{"name": "John Smith", "email": "john_smith@haus.com", "flat_number": 1029}], "success": True, "total_count": 1 }`

- **GET** `/inquiries`

  Returns a formatted list of all inquiries.

  Sample request: `curl http://localhost:5000/inquiries -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"`

  Sample response: `{ "inquiries": [{ "inquirer_id": 1, "items": "Some items", "status", "active", "tag": "Some tag" }], "success": True, "total_count": 1 }`

- **POST** `/inquiries`

  Creates a new inquiry provided with inquirer_id, items, and tag.

  Sample request: `curl http://localhost:5000/inhabitants -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" d '{"inquirer_id": 1, "items": "Some items", "tag": "Some tag"}'`

  Sample response: `{ "inquiries": [{ "inquirer_id": 1, "items": "Some items", "status", "active", "tag": "Some tag" }], "success": True, "total_count": 1 }`

- **PATCH** `/inquiries/:id`

  Changes inquiry status provided with the id.

  Sample request: `curl http://localhost:5000/inhabitants -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"`

  Sample response: `{ "inquiry": { "inquirer_id": 1, "items": "Some items", "status", "active", "tag": "Some tag" }, "success": true }`

- **DELETE** `/inquiries/:id`

  Deletes an inquiry provided with the id.

  Sample request: `curl http://localhost:5000/inhabitants -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"`

  Sample response: `{"inquiries": [], "success": true, "total_count": 0}`

### Roles & Permissions:

**GET** `/authorization/url` can be used as a convenience for the reviewer to generate the Auth0 login link in order to acquire an access token. For each role listed below sample login data has also been provided to facilitate the reviewing process.

- Superintendent:

  The role is for the caretaker of the building.

  Permissions: they can _get inhabitants_ and _get inquiries_.

  Sample mail address: `superintendent@superintendent.com`

  Sample password: `hausHAUS1234`

- Inhabitant:

  The role is for the resident of the building.

  Permissions: they can _read, post, delete, patch inquiries_.

  Sample mail address: `inhabitant@inhabitant.com`

  Sample password: `hausHAUS1234`
