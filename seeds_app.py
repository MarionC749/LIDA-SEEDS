#CREATING THE SEEDS DASHBOARD

import dash

from layouts.main_layout import create_main_layout
from callbacks.existing_callbacks import create_existing_callbacks
from callbacks.dvpt_callbacks import create_dvpt_callbacks

# ------ CREATE DASH APP ------
app = dash.Dash(__name__,
                suppress_callback_exceptions= True)
server= app.server

# ------ LOAD APP LAYOUT ------
app.layout = create_main_layout()

# ------ REGISTER CALLBACKS ------
create_existing_callbacks(app)
create_dvpt_callbacks(app)


# ------ RUN APP ------
# For local development, debug=True
# When deploying, debug=False

if __name__ == '__main__':
    app.run(debug= True)