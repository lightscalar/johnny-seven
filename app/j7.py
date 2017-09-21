'''Launch all servers, etc., for Johnny-Seven!'''
from subprocess import Popen
from time import sleep

# Main control loop for handling process launch, restarting failed servers...
# ----------------
# PORTS
# ----------------
# STATIC    - 5000
# SOCK API  - 5200
# GAZEPOINT - 4242

# Serve the static site.
static_site = Popen(['python', 'static.py'])

# Launch the UI's socket server!
sock_api = Popen(['python', 'sock.py'])

# Monitor processes; shut down on keyboard break.
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    static_site.kill()
    sock_api.kill()

