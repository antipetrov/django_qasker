# django_qasker

Home-grown stackeoverflow-like QA service. Vanilla Django. Hardcore. Now with avatars.


## Demo-site

http://37.139.2.116

login: demouser
password: demopass

## Usage

**make prod**

Rebuilds & launches docker-based server conig:
- hasker-backend
- mysql
- nginx

Also updates DB with fresh migrations.

**make build**

Rebulds docker image for hasker-backend

**make run**

starts all services using docker-compose

**make stop**

stops all services

**make test-data**

loads initial data (django fixtures) to get you up to speed.

**make test**

runs tests