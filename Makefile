build:
	docker build -f docker/Dockerfile --rm -t hasker_server:local .

run:
	docker-compose up -d
	docker exec haskerproject_backend_1 python manage.py collectstatic --noinput

stop:
	docker-compose down

