all: docker

docker: Dockerfile app.py
	docker build -t "remix/natlang" .

run:
	docker run -p 5003:8000 -d --rm remix/natlang
