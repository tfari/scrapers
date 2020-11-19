### check_urls.py 
Filter and extract some basic information of a list of domains.

We tested using the .csv subset of those provided by [NICathon](https://www.opendatacordoba.org/NICathon/data.html), in check_ar_csv.py.
<br/>
<br/>
**Usage:**

Simply call thread_urls_check() in check_urls.py with the desired parameters.

Results are saved in .xlsx format. Down domains are filtered out of the results list.


**We save the following data:**
* Status code of domain GET call
* Url of the domain
* Registrar
* Redirected URL
* Title of the page
* Data acquired via the [builtwith](https://pypi.org/project/builtwith/) module


**Warning**:

 There's a minor bottleneck due to regex catastrophe within builtwith's .contains() method, i've cloned builtwith to 
 ./timeout_builtwith and modified builtwith() by adding an optional timeout on the loops that call the function. 
 This helps reduce the bottlenecked time by cancelling the call once the time is over the limit. Given that the offense 
 is within a re.search() call, it stills takes a while before cancelling, but i've reduced average elapsed time of the 
 worst-case offenders from over a couple hours to 25 minutes.
 <br/>

The next step in trying to fix this issue would be using something like timeout-decorator to decorate
.contains(), but said solution is Unix specific.
