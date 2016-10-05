default:
	cp opentablebench/config.py-example opentablebench/config.py
	python run.py

folders:
	mkdir -p data/
	mkdir -p data/cache
	mkdir -p data/cache/entities
	mkdir -p data/cache/labels
	mkdir -p logs/
	mkdir -p generated/tables
	mkdir -p generated/properties
	mkdir -p generated/subject_columns
	mkdir -p generated/classes
	mkdir -p generated/rdf

clean_generated:
	rm -rf generated/tables/*
	rm -rf generated/properties/*
	rm -rf generated/subject_columns/*
	rm -rf generated/classes/*
	rm -rf generated/rdf/*

clean_cache:
	rm -rf data/cache/entities/*
	rm -rf data/cache/labels/*

install:
	pip install -r requirements.txt
