DATA_PATH = ./data
SCRIPTS_PATH = ./scripts

USERS_SCRIPT = users.py
SUBMISSIONS_SCRIPT = submissions.py

users: $(DATA_PATH)/users.csv

$(DATA_PATH)/users.csv:
	$(SCRIPTS_PATH)/$(USERS_SCRIPT)

submissions: $(DATA_PATH)/users.csv
	$(SCRIPTS_PATH)/$(SUBMISSIONS_SCRIPT)

cleandata:
	rm -fr ./data/*