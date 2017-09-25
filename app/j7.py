'''Launch all servers, etc., for Johnny-Seven!'''
from subprocess import Popen
from time import sleep

# Main control loop for handling process launch, restarting failed servers...
# ----------------
# PORTS
# ----------------
# STATIC    - 5000
# REST API  - 5100
# GAZEPOINT - 4242

# Serve the static site.
static_site = Popen(['python', 'static.py'])

# Launch the UI's socket server!
rest_api = Popen(['python', 'rest.py'])

# Monitor processes; shut down on keyboard break.
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    static_site.kill()
    rest_api.kill()

