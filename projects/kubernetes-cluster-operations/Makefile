.PHONY: test validate up smoke down
test:
	python3 -m unittest discover -s tests -v
validate:
	bash scripts/check.sh
up:
	bash scripts/up.sh
smoke:
	bash scripts/smoke.sh
down:
	bash scripts/down.sh
