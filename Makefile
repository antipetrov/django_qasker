build:
	docker build -t antipetrov/hasker .

run:
	docker run -it -p 8080:8080 -p 3309:3306 -v `pwd`:/hasker -w /hasker --name hasker_centos --rm antipetrov/hasker bash

