up:
	docker-compose up -d


down:
	docker-compose down

reup:
	docker-compose down
	docker-compose build
	docker-compose up -d