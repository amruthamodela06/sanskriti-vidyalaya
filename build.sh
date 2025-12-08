#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create upload directories
mkdir -p app/static/uploads/gallery
mkdir -p app/static/uploads/staff
mkdir -p app/static/uploads/timetables
mkdir -p app/static/uploads/blogs
