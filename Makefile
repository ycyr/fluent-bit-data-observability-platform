all: build start logs wait show-metrics

clean:
	rm -rf *.so *.h *~

build: clean
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs

restart-fluent-bit:
	docker-compose restart fluent-bit

show-metrics:
	curl -s http://localhost:9091/metrics | grep fluentbit

wait:
	sleep 2