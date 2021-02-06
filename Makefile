.PHONY: run-redis
run-redis:
	@docker run \
		-i -t -d --rm \
		-p 6379:6379\
		-v `pwd`/namaphio/data:/data\
		--name namaphio-redis\
		redis:alpine

.PHONY: kill-redis
kill-redis:
	@docker stop namaphio-redis

.PHONY: bash-redis
bash-redis:
	@docker exec\
		-i -t namaphio-redis\
		sh

.PHONY: start-io
start-io:
	@uvicorn namaphio:app --reload --port 8080 --host 0.0.0.0
