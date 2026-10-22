.PHONY: test run up down smoke
test:
	python3 -m unittest discover -s tests -v
run:
	python3 -m aiops.api
up:
	docker compose up --build -d
down:
	docker compose down
smoke:
	python3 scripts/smoke.py
