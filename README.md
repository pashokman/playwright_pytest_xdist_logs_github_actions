This is an example of logging into 1 file, while using pytest-xdist (parallel test execution).

# How to run local
Before next steps install dependencies.
1. Open second terminal and start log server:
```
python .\utils\logs\log_server.py
```
2. Open first terminal and start testing:
```
pytest -v -s -k test_item_names_text --browser webkit -n 3
```
3. Check the results in `automation.log` file. 

You can download log file after test run completed.

You can download allure-report after test run completed.  
To see actual results of allure-report, download allure artifact, extract folder from a zip file, run command:
```
allure serve allure-results
```