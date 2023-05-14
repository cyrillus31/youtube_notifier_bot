#! /bin/bash

sqlite3 ../data.db '.mode csv' '.headers on' '.output o.csv' 'SELECT * FROM videos'

