build:
	docker build -f docker/Dockerfile --rm -t hasker_server:local .

run:
	docker-compose up -d
	docker exec haskerproject_backend_1 python manage.py collectstatic --noinput

run-debug:
	docker-compose up
	docker exec haskerproject_backend_1 python manage.py collectstatic --noinput

test:
	docker exec haskerproject_backend_1 python manage.py test


stop:
	docker-compose down

test-data:
	docker exec haskerproject_backend_1 python manage.py loaddata answers


prod:	
	docker build -f docker/Dockerfile --rm -t hasker_server:local .
	docker-compose up -d
	docker exec haskerproject_backend_1 python manage.py collectstatic --noinput
	docker exec haskerproject_backend_1 python manage.py loaddata answers