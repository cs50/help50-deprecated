default: build run

pull:
	docker login
	docker pull cs50/help50

build:
	docker build -t cs50/help50 .

rebuild:
	docker build --no-cache -t cs50/help50 .

run:
	docker run -i --rm -p 80:80 -v `pwd`:/src -t cs50/help50

bash:
	docker run -i --rm -p 80:80 -v `pwd`:/src -t cs50/help50 bash
