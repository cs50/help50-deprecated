build:
	docker build -t cs50/help50 .

rebuild:
	docker build --no-cache -t cs50/help50 .

up:
	docker-compose up

shell:
	docker run -i --name help50 -p 8080:8080 --rm -v "$(PWD)":/srv/www -t cs50/help50 bash -l
