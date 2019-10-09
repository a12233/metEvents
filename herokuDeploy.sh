#!/bin/bash
heroku container:push web -a=metevents
heroku container:release web -a=metevents
heroku open -a=metevents
