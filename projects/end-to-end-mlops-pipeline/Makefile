.PHONY: test run up down
test:
	python3 -m unittest discover -s tests -v
run:
	python3 run.py examples/scenario.json
up:
	docker compose up --build -d
down:
	docker compose down
