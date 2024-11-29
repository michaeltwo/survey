# Survey Management System

This is an survey management system for TDS Final Project

Running Environment: Docker or Podman. Redhat-9.1 podman-5.2.2 tested

## Installation

Prerequsites: docker. make sure port 8000(web),5432(db) are free.

Installation steps as below:
 - For linux, just use apt install(debain), yum install python(redhat).
 - For windows, just download the package form <(https://www.docker.com/products/docker-desktop/)>, and install it.
   
 Run the app
 - copy the docker-compose.yml file and credential file .env to the same folder
 - start a command/cli window, and cd to the folder mentioned above step, then run below command
```bash
docker-compose up -d
```
app guide:
if it is running locally, just open a web brower and type in <http://127.0.0.1:8000>

if it is running in a server, please input the server ip address <http://serverIP:8000>

## Usage

1. register a user, if you already have an account, can perform login directly

2. survey taker and survey craeter

3. click on logout, after operate done. 

NOTE. Remember your username and password


## Contributing

Please let us know if any confusion, 

Group: 8

Group Members: Michael F, Weihua Z, Dev S, Shubham G J

## License
This is just for TDS Final Project
Author: Michael F, Michael Z, Dev S, Shubham G J

[MIT](https://choosealicense.com/licenses/mit/)

[Django](https://docs.djangoproject.com/zh-hans/5.0/py-modindex/)
