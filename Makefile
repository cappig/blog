.PHONY: build test clean katex deploy down

katex:
	python scripts/katex.py

build:
	python scripts/generate.py

test:
	python scripts/test.py

clean:
	rm -rf site/


deploy: build
	docker-compose up -d --build

down:
	docker-compose down
