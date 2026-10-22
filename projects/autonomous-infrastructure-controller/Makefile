.PHONY: test demo image
test:
	python3 -m unittest discover -s tests -v
demo:
	python3 -m controller.cli --replicas 3 --utilization 0.92
image:
	docker build -t infrastructure-controller:local .
