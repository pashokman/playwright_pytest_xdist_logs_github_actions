In this framework I implemented:
- logging into 1 file, while using pytest-xdist (parallel test execution),
- allure reporting, 
- screenshot and video on failure and also attached it to allure-report,
- moved pytest options into a pytest.ini file,
- pytest marker into test,
- rerun functionality to avoid flacky tests,
- cleanup allure-results (report) and test-results (screenshots and videos on failure) folders before each pytest run,
- test data moved into separate file,
- trace on failed tests,
- secret variable - BASE_URL.

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
To see Report, download `allure-report` artifact, extract folder from a zip file, run the command:
```
allure serve allure-results
```

To see the trace of failed test you should download `playwright-screenshots-videos-traces-on-failure` artifact, extract from a zip file, run the command (before using this command should install NodeJS):
```
npx playwright show-trace test-results/tests-test-try-py-test-item-names-text-webkit-incorrect-login-incorrect-pwd/trace.zip
```