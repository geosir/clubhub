#!/bin/bash
python3 manage.py createsuperuser
python3 manage.py loaddata main/fixures/HubGroups.json
python3 manage.py loaddata main/fixures/Groups.json
python3 manage.py loaddata main/fixures/Settings.json
