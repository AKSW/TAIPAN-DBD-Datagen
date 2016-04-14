default:
	cp dbpediatablegen/config.py-example dbpediatablegen/config.py
	python dbpediatablegen/main.py

folders:
	mkdir -p dbpediatablegen/generated/tables
	mkdir -p dbpediatablegen/generated/properties
	mkdir -p dbpediatablegen/generated/subject_columns
	mkdir -p dbpediatablegen/generated/classes

clean:
	rm -rf dbpediatablegen/generated/tables/*
	rm -rf dbpediatablegen/generated/properties/*
	rm -rf dbpediatablegen/generated/subject_columns/*
	rm -rf dbpediatablegen/generated/classes/*

