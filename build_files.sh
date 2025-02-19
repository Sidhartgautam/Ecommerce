#!/bin/bash

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo "Applying database migrations..."
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Deployment successful!"
