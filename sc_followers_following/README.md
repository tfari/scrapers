### get_soundcloud

This script scraps the data of the followers or following lists of a soundcloud.com user and stores it into an excel file.

geckodriver.exe must be in path to generate a client_id via Selenium. 

If the client_id no longer works, just delete the file "client_id" and run again to generate a new one.

To set the preferred output path for the files, edit the OUTPUT_PATH field in settings.json (./output by default.)

(Settings file gets created first time the script runs.)

**Requirements:**
- requests
- bs4
- playsound

**Usage:**
```
python get_soundcloud.py USERNAME | MODE | ORDER_HEADER
```
MODE and ORDER_HEADER are optional parameters, they default to 'followers' and 'country'.

**Example:**
```
python get_soundcloud.py MyUser | follower | city
```
Produces an .xlsx file with the data of the accounts that follow MyUser, sorted
by the field 'city'.