#!/bin/bash

gunicorn --chdir /usr/app --workers 1 --bind 0.0.0.0:5000 app:app
