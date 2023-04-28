import pathlib

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy, ClientsideFunction

from app import layout


CLIENTSIDE_CALLBACKS = dict(src='assets/callbacks.js', type='text/javascript')
fffCLIENTSIDE_CALLBACKS = dict(src='assets/callbacks.js', type='text/javascript')
FONTAWESOME = dict(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css", integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==", crossorigin="anonymous", referrerpolicy="no-referrer")

ASSETS = pathlib.Path(__file__).resolve().parent / 'assets'

app = DashProxy(
    __name__,
    external_scripts=[CLIENTSIDE_CALLBACKS],
    external_stylesheets=[dbc.themes.SKETCHY, FONTAWESOME],
    assets_url_path='assets',
    assets_folder=str(ASSETS)
)

layout.apply(app)


app.clientside_callback(ClientsideFunction(namespace='transcription', function_name='update'), Output("transcription", "html"), Input("transcription", "html"), Input("ws", "message"))
