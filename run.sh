#!/bin/bash

until python run.py; do
  echo "Probably 5xx from SPARQL endpoint, exit code $?. Respawning.." >&2
  sleep 1
done
