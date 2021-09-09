import requests

# requests.get('http://0.0.0.0:5000/set_mode_bot', json={'mode': 'demo' })

# requests.get('http://0.0.0.0:5000/set_mode_bot', json={ 'mode': 'jal2_stop' })
requests.get('http://0.0.0.0:5000/set_mode_bot', json={ 'mode': 'jal2_open_down' })
