default:
	python dbpediatablegen/main.py

folders:
	mkdir -p dbpediatablegen/generated/tables
	mkdir -p dbpediatablegen/generated/properties
	mkdir -p dbpediatablegen/generated/subject_columns

clean:
	rm -rf dbpediatablegen/generated/tables/*
	rm -rf dbpediatablegen/generated/properties/*
	rm -rf dbpediatablegen/generated/subject_columns/*

