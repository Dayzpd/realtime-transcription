
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_extensions import Purify, EventListener
from dash_extensions.enrich import html
from dash.exceptions import PreventUpdate



def navbar(
    brand : str,
    url : str,
    color : str = None
):

    color = color or 'dark'

    return dbc.Navbar(
            className='d-flex justify-content-between p-3',
            color=color,
            dark=True,
            children=[
                dbc.NavItem(
                    html.A(
                        dbc.NavbarBrand(brand, className="ms-2"),
                        className="g-0",
                        href=url,
                        style={"textDecoration": "none"},
                    )
                ),
            ]
        )
