# FLASKAPI_TASK1

first of all to run the app. install flask. 

create an environment with python and run the command

`pip install -r requirements.txt`

now simply run the app : `python flask_api_task1.py`

go to postman : server will be shown in the command, defauls is `http://127.0.0.1:5000` or `localhost:5000`

For Sum :`http://127.0.0.1:5000/sum`

go to body :

`{
  "numbers": [1,3,4,10,15,20]
}`

output will be :

`{
    "sum": 8
}`

for concatenate: `http://127.0.0.1:5000/concatenate`

go to body :

`input : {
  "string1": "welcome to",
  "string2": " uktob.ai"
}`

output : 

`{
    "concatenated_string": "welcome to uktob.ai"
}
`

# FLASK TASK 2

run the app : `python flask_api_task2.py`

endpoints: 

`/register`

input :

`{
  "username": "nafseer",
  "password": "nafseer"
}`

output:

`{
    "message": "User registered successfully"
}`

`/login`

input:

`{
  "username": "nafseer",
  "password": "nafseer"
}`




