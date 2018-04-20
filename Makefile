build:
	docker build --rm -t hasker_server:local .

run:
	docker-compose up -d
	docker exec -it haskerproject_backend_1 python manage.py collectstatic --noinput

stop:
	docker-compose down

