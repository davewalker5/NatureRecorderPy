import time
from behave import given, when, then
from selenium.webdriver.common.by import By


@given("I navigate to the locations list page")
@when("I navigate to the locations list page")
def _(context):
    url = context.flask_runner.make_url("locations/list")
    context.browser.get(url)
    assert "Locations" in context.browser.title


@when("I fill in the location details")
def _(context):
    # Having clicked, we need to sleep this thread to allow the server round trip to  refresh the page.
    # WebDriverWait won't work in this context
    time.sleep(1)
    row = context.table.rows[0]
    context.browser.find_element(By.NAME, "name").send_keys(row["Name"])
    context.browser.find_element(By.NAME, "address").send_keys(row["Address"])
    context.browser.find_element(By.NAME, "city").send_keys(row["City"])
    context.browser.find_element(By.NAME, "county").send_keys(row["County"])
    context.browser.find_element(By.NAME, "postcode").send_keys(row["Postcode"])
    context.browser.find_element(By.NAME, "country").send_keys(row["Country"])
    context.browser.find_element(By.NAME, "latitude").send_keys(row["Latitude"])
    context.browser.find_element(By.NAME, "longitude").send_keys(row["Longitude"])


@then("There will be {number} locations in the locations list")
@then("There will be {number} location in the locations list")
def _(context, number):
    # Having clicked, we need to sleep this thread to allow the server round trip to pull the results and
    # refresh the page. WebDriverWait won't work in this context
    time.sleep(1)
    table = context.browser.find_element(By.CLASS_NAME, "striped")
    table_body = table.find_element(By.XPATH, ".//tbody")
    table_rows = table_body.find_elements(By.XPATH, ".//tr")
    expected = int(number)
    actual = len(table_rows)
    assert actual == expected


@then("The locations list will be empty")
def _(context):
    # Having clicked, we need to sleep this thread to allow the server round trip to pull the results and
    # refresh the page. WebDriverWait won't work in this context
    time.sleep(1)
    xpath = f"//span[text()='There are no locations in the database']"
    _ = context.browser.find_element(By.XPATH, xpath)
