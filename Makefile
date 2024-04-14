dev:
	docker-compose up eleconsurp_api

rename:
	@echo "Enter a project name: "; \
	read proj_name; \
	bash ./name_replacer_mac.sh "$$proj_name"

db-revision:
	docker-compose run eleconsurp_api alembic revision --autogenerate

db-migrate:
	docker-compose run eleconsurp_api alembic upgrade head

format:
	pipenv run sort
	pipenv run format

lint:
	pipenv run lint

