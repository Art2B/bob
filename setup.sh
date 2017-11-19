#!/bin/zsh
# Create config file
cp example.config.json config.json
# Create DB file
touch iterations.db
# Install dependencies
pip install requests
pip install TwitterAPI
pip install peewee