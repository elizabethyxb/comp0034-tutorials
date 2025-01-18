# Imports for Dash and Dash.html
from dash import Dash, html
import dash_bootstrap_components as dbc
import dash

# Variable that defines the meta tag for the viewport
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap components (dbc)
external_stylesheets = [dbc.themes.LITERA]

# Create an instance of the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags, use_pages=True)

# From https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Event Details", href=dash.page_registry['pages.events']['path'])),
        dbc.NavItem(dbc.NavLink("Charts", href=dash.page_registry['pages.charts']['path'])),
    ],
    brand="Paralympics Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
)
# Add an HTML layout to the Dash app
app.layout = dbc.Container([
    # Add an HTML div with the text 'Hello World'
    navbar,
    dash.page_container
    ])

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5050)