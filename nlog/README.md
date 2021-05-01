# nloggenerator.py
### What is nloggenerator.py?
It's a little utility to generate random logs lines, complying with the RFC5424 syslog spec.
It uses the opensource [rfc5424-logging-handler](https://pypi.org/project/rfc5424-logging-handler/) python module.
### Running nloggenerator.py:
Simply execute it. It will generate logs out to screen, and, by default, out to port 1514. Change this to a port where you have a syslog server listening.
To stop it running, hit ctrl-c or kill it, or if it's running inside a container, stop the container.