.PHONY: build test clean katex deploy down

build:
	python scripts/generate.py

test:
	python scripts/test.py

clean:
	rm -rf site/

katex:
	python scripts/katex.py

deploy: build
	docker-compose up -d --build

down:
	docker-compose down