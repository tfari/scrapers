### get_soundcloud

This script scraps the data of the followers or following lists of a soundcloud.com user and stores it into an excel file.

geckodriver.exe must be in path to generate a client_id via Selenium. 

If the client_id no longer works, just delete the file "client_id" and run again to generate a new one.


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