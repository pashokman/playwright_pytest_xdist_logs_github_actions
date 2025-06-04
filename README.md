This is an example of logging into 1 file, while using pytest-xdist (parallel test execution).


# How to run local
1. Create virtual environment.
```
python -m venv venv
```
2. Activate virtual environment.
```
.\venv\Scripts\activate
```
3. Install dependencies.
```
pip install -r requirements.txt
playwright install
```
4. Open second terminal and start log server:
```
python .\utils\logs\log_server.py
```
5. Open first terminal and run tests V(to change pytest run options, use `pytest.ini` file):
```
pytest
```

You can download `automation.log` file after test run completed.

You can download `allure-report` file after test run completed.  
To see actual results of allure, download `allure-report` artifact, extract folder from a zip file, run command:
```
allure serve allure-results
```