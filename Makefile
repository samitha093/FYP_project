up_child:
	docker-compose -f docker-composer.child.yml up -d

down_child:
	docker-compose -f docker-composer.child.yml down

reup_child:
	docker-compose -f docker-composer.child.yml down
	docker-compose -f docker-composer.child.yml build
	docker-compose -f docker-composer.child.yml up -d

up_parent:
	docker-compose -f docker-composer.parent.yml up -d

down_parent:
	docker-compose -f docker-composer.parent.yml down

reup_parent:
	docker-compose -f docker-composer.parent.yml down
	docker-compose -f docker-composer.parent.yml build
	docker-compose -f docker-composer.parent.yml up -d

up_dev:
	docker-compose -f docker-composer.dev.yml up -d

down_dev:
	docker-compose -f docker-composer.dev.yml down

reup_dev:
	docker-compose -f docker-composer.dev.yml down
	docker-compose -f docker-composer.dev.yml build
	docker-compose -f docker-composer.dev.yml up -d
