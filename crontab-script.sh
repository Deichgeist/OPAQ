#!/bin/bash
git pull origin
./opaq.py > /dev/null 2>&1 
git add opaq.json
git commit -m "Update of JSON data"
git push origin
