# django_qasker


Home-grown stackeoverflow QA site. Vanilla Django. Hardcore.


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