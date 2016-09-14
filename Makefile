default:
	cp opentablebench/config.py-example opentablebench/config.py
	python run.py

folders:
	mkdir -p generated/tables
	mkdir -p generated/properties
	mkdir -p generated/subject_columns
	mkdir -p generated/classes

clean:
	rm -rf generated/tables/*
	rm -rf generated/properties/*
	rm -rf generated/subject_columns/*
	rm -rf generated/classes/*

install:
	pip install -r requirements.txt
