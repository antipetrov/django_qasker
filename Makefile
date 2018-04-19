build:
	docker build --rm -t hasker_server:local .

run:
	docker-compose up -d

stop:
	docker-compose down

