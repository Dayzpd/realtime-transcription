
import dash_bootstrap_components as dbc
from dash_extensions import WebSocket, Purify
from dash_extensions.enrich import html

from app import components

def apply(app):

    app.layout = \
        dbc.Container(
            fluid=True,
            class_name='m-0 p-0',
            children=[
                components.navbar('', '', 'dark'),
                WebSocket(id="ws", url="ws://127.0.0.1:8000/english"),
                html.Div(
                    children=Purify(id="transcription"),
                    style={ 
                        "overflowY" : "scroll",
                        "height" : "300px",
                        "flexDirection" : "column-reverse",
                        "display" : "flex",
                    }
                )
            ]
        )
