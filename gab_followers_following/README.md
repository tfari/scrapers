### Deprecated
Gab changed its API and now hides followers behind a login screen. At the moment of writing this api.gab.com times out.

### get_gab

This script scraps the data of the followers or following lists of a gab.ai user and stores it into an excel file.

To set the preferred output path for the files, edit the OUTPUT_PATH field in settings.json (./output by default.)

(Settings file gets created first time the script runs.)

**Usage:**
```
python get_gab.py USERNAME | MODE | ORDER_HEADER | NUM_THREADS | MAX_PASSES | SLEEP_PASS
```
MODE, ORDER_HEADER, NUM_THREADS, MAX_PASSES and SLEEP_PASS are optional parameters, they default to 'followers', 'bio' and 100 respectively.


**Example:**
```
python get_gab.py MyUser following name 23 10 2
```
Produces an .xlsx file with the data of the accounts that MyUser follows, sorted by the field 'name'. It distributes
the HTTP requests along 23 threads, performs 10 passes over the erros, and sleeps 2 seconds between each pass.


