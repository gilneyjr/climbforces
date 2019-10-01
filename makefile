ALL_DATA_PATH = ./data/all
SCRIPTS_PATH = ./scripts

USERS_SCRIPT = users.py
SUBMISSIONS_SCRIPT = submissions.py

users: $(ALL_DATA_PATH)/users.csv

$(ALL_DATA_PATH)/users.csv:
	$(SCRIPTS_PATH)/$(USERS_SCRIPT)

submissions: $(ALL_DATA_PATH)/users.csv
	$(SCRIPTS_PATH)/$(SUBMISSIONS_SCRIPT)

cleandata:
	rm -fr ./data/*