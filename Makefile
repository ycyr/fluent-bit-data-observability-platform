all: build start wait message

clean:
	rm -rf *.so *.h *~

build: clean
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down

full-restart: stop start

logs:
	docker-compose logs

restart-fluent-bit:
	docker-compose restart fluent-bit

show-metrics:
	curl -s http://localhost:9091/metrics | grep fluentbit

wait:
	@sleep 2

message:
	@echo "Open Grafana with http://127.0.0.1:3000/"