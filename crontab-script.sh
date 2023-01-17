#!/bin/bash
git pull origin
./opaq.py 
git add opaq.json
git commit -m "Update of JSON data"
git push origin
