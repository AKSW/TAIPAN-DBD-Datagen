default:
	cp opentablebench/config.py-example opentablebench/config.py
	python run.py

folders:
	mkdir -p data/
	mkdir -p data/cache
	mkdir -p generated/tables
	mkdir -p generated/properties
	mkdir -p generated/subject_columns
	mkdir -p generated/classes
	mkdir -p generated/rdf

clean:
	rm -rf data/*
	rm -rf data/cache/*
	rm -rf generated/tables/*
	rm -rf generated/properties/*
	rm -rf generated/subject_columns/*
	rm -rf generated/classes/*
	rm -rf generated/rdf/*

install:
	pip install -r requirements.txt
