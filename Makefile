all: init test cleanup

init: build deploy

build:
	@echo '###################### building image ######################'
	@sudo docker build -t st1991/sampling-service:flask .
deploy:
	@echo '###################### loading containers ######################'
	@sudo docker-compose up -d
	@sleep 5
test:
	@echo '###################### testing ######################'
	@sudo python3 test.py
clean:
	@echo '###################### cleaning ######################'
	@sudo docker-compose down
	@sudo rm -r log
	@sudo rm -r data