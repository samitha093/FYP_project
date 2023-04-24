up child:
	docker-compose -f docker-composer.child.yml up -d

down child:
	docker-compose -f docker-composer.child.yml down

reup child:
	docker-compose -f docker-composer.child.yml down
	docker-compose -f docker-composer.child.yml build
	docker-compose -f docker-composer.child.yml up -d

up parent:
	docker-compose -f docker-composer.parent.yml up -d

down parent:
	docker-compose -f docker-composer.parent.yml down

reup parent:
	docker-compose -f docker-composer.parent.yml down
	docker-compose -f docker-composer.parent.yml build
	docker-compose -f docker-composer.parent.yml up -d