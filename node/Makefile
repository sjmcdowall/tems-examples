SHELL := /bin/bash
NAME = tems-example-node
VERSION = 1.0.0

lint:
	npm run lint

prod:
	npm run prod

dev:
	npm start

all: clean modules lint build

build:
	npm run build

clean:
	npm run clean

modules:
	npm install

.PHONY: docker build
