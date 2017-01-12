clean:
	rm -rf lib
install: clean
	pip2 install -t lib -r requirements.txt
build:
	cd lib; cp ../*.py .; cp -r ../templates .; cp ../app.yaml .
deploy:
	cd lib; gcloud app deploy
test:
	cd lib; python2 server.py
