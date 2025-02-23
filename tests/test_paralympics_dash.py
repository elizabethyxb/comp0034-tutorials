import requests
from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains

def test_server_live(dash_duo):
    """
    GIVEN the app is running
    WHEN an HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    # Start the app in a server
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Delay to wait 2 seconds for the page to load
    dash_duo.driver.implicitly_wait(2)

    # Get the url for the web app root
    # You can print this to see what it is e.g. print(f'The server url is {url}')
    url = dash_duo.driver.current_url

    # Requests is a python library and here is used to make an HTTP request to the sever url
    response = requests.get(url)

    # Finally, use the pytest assertion to check that the status code in the HTTP response is 200
    assert response.status_code == 200

def test_home_h1_text_equals(dash_duo):
    """
    GIVEN the app is running
    WHEN the home page is available
    THEN the H1 heading with an id of 'title' should have the text "Paralympics Dashboard"
    """
    # As before, use the import_app to run the Dash app in a threaded server
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Wait for the H1 heading to be available on the page, timeout if this does not happen within 4 seconds
    dash_duo.wait_for_element("h1", timeout=4)  # Dash function version

    # Find the text content of the H1 heading element
    h1_text = dash_duo.find_element("h1").text  # Dash function version

    # Assertion checks that the heading has the expected text
    assert h1_text == "Paralympics Data Analytics"

def test_dropdown_values(dash_duo):
    """
    GIVEN the app is running
    WHEN the home page is available
    THEN the dropdown with an id of 'dropdown-category' should have values "events", "sports", "countries", "participants"
    """
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Wait for the dropdown to be available on the page, timeout if this does not happen within 4 seconds
    dash_duo.wait_for_element_by_id("dropdown-category", timeout=4)

    # Find the dropdown element
    dropdown = dash_duo.find_element("#dropdown-category")

    # Get the options from the dropdown
    options = dropdown.find_elements_by_tag_name("option")

    # Get the values from the options
    values = [option.get_attribute("value") for option in options]

    
    # Assertion checks that the dropdown has the expected values
    assert values == ["", "events", "sports", "countries", "participants"]

def test_bar_chart_updates(dash_duo):
    """
    GIVEN the app is running
    AND the checkboxes are available on the page
    WHEN both checkboxes are selected
    THEN the two charts should be in the div with the id 'bar-div' (can be tested with the class=dash-graph)
    """

    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Wait until the checkbox element is displayed
    dash_duo.wait_for_element_by_id("checklist-games-type", timeout=2)

    # Select the 'Winter' checkbox. Summer is already selected by default.
    winter_checkbox = dash_duo.find_element("#checklist-games-type input[value='winter']")
    # Click the checkbox
    winter_checkbox.click()

    # Wait for the bar chart elements to be present
    dash_duo.wait_for_element_by_id("bar-chart-winter", timeout=10)
    dash_duo.wait_for_element_by_id("bar-chart-summer", timeout=3)

    # Find div with the id 'bar-div' that contains the charts
    bar_div = dash_duo.find_element("#bar-div")
    # count the number of elements in bar_div with the class 'dash-graph'
    # This is a list of elements that have the class 'dash-graph'
    # The length of this list is the number of elements with that class
    num_charts = len(bar_div.find_elements_by_class_name("dash-graph"))
    # Alternatively, use ID selector to find 'bar-chart-winter' and 'bar-chart-summer'
    winter_chart = len(bar_div.find_elements_by_id("bar-chart-winter"))
    summer_chart = len(bar_div.find_elements_by_id("bar-chart-summer"))

    # There should be 2 charts
    assert winter_chart == 1
    assert summer_chart == 1
    assert num_charts == 2


def test_line_chart_changes(dash_duo):
    """
    GIVEN the app is running
    WHEN the dropdown is used to select "Sports"
    THEN the line chart should be displayed
    AND the chart title should include the word "sports"
    """

    # Start the app in a server
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Find the title displayed in the plotly express chart
    # The .gtitle class name was found using the browser developer tools to inspect the element
    dash_duo.wait_for_element_by_id("line-chart", timeout=2)
    line_chart_title_start = dash_duo.find_element("#line-chart .gtitle").text

    # This uses a Dash testing method to find the element by its id, not the selenium method
    dash_duo.wait_for_element_by_id("dropdown-category", timeout=2)

    # Find the dropdown element by its id and select the option with the text "Sports"
    # see https://www.testim.io/blog/selenium-select-dropdown scroll down to the Python example
    sport_opt_xpath = "//select[@id='dropdown-category']/option[text()='Sports']"
    dash_duo.driver.find_element(by=By.XPATH, value=sport_opt_xpath).click()

    # Wait for the #line-chart element to be present and updated
    # dash_duo.wait_for_element_by_id("line-chart", timeout=2)

    WebDriverWait(dash_duo.driver, 3).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#line-chart .gtitle'), 'sports')
    )

    # Find the title displayed in the plotly express chart
    chart_title_end = dash_duo.find_element("#line-chart .gtitle").text

    # Assert that the title includes the word "sports" and the title has changed
    assert "sports" in chart_title_end.lower()
    assert line_chart_title_start != chart_title_end

def test_map_marker_hover_updates_card(dash_duo):
    """
    GIVEN the app is running which has a <div id='map>
    THEN there should not be any elements with a class of 'card' one the page
    WHEN a marker in the map is selected
    THEN there should be one more card on the page then there was at the start
    AND there should be a text value for the h6 heading in the card
    """
    # Start the app in a server
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Wait for the div with id of card to be on the page
    dash_duo.wait_for_element("#card", timeout=2)

    # There is no card so finding elements with a bootstrap class of 'card' should have a length of 0
    cards = dash_duo.find_elements(".card")
    cards_count_start = len(cards)

    # Find the first map marker
    marker_selector = '#map-fig > div.js-plotly-plot > div > div > svg:nth-child(1) > g.geolayer > g > g.layer.frontplot > g > g > path:nth-child(1)'
    marker = dash_duo.driver.find_element(By.CSS_SELECTOR, marker_selector)

    # Use the Actions API and build a chain to move to the marker and hover
    ActionChains(dash_duo.driver).move_to_element(marker).pause(2).perform()

    # Wait for the element with class of 'card'
    dash_duo.wait_for_element(".card", timeout=1)

    # Count the cards again
    cards = dash_duo.find_elements(".card")
    cards_count_end = len(cards)

    # Find the card title and get the textContent attribute value
    title_selector = '//*[@id="card"]/div/div/h4'
    card_title = dash_duo.driver.find_element(by=By.XPATH,value=title_selector)
    text = card_title.get_attribute("textContent")

    # The card title should have changed and there should be more cards
    assert text != ""
    assert cards_count_end > cards_count_start
