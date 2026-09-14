import os
import dash
from dash import callback, Input, Output, State
from dash import no_update

from constants import DEFAULT_BACKEND_URL

import requests

@callback(
     Output('findings', 'children'),
     Input('name-button','n_clicks'),
     State('name', 'value'),
     prevent_initial_call=True)
def update_main(n, name):
    if not n:
        return dash.no_update
    
    if not name:
        return dash.no_update

    headers = {
        'accept': 'application/json',
    }

    params = {
        'name': name,
    }

    BACKEND_URL = os.environ.get('BACKEND_URL', DEFAULT_BACKEND_URL)


    response = requests.get(f'{BACKEND_URL}/age', params=params, headers=headers)
    if response.status_code != 200:
        return f'{name} is not your friend... sad!'
    
    data = response.json()
    data = data[0]

    return f"{data['first_name']} {data['last_name']} is {data['age']} years old!"
