import pytest


# see https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
# the goal here is to let fixtures know if a test succeeded or not by checking `request.node.report_call.passed` etc
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()
    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "report_" + report.when, report)
