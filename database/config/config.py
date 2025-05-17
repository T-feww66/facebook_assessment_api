import os

host = "localhost"
if os.getenv("IN_DOCKER") == "true":
    host = "host.docker.internal"

DB_CONFIG = {
    "host": host,
    "user": "root",
    "password": "",
    "database": "thuctap"
}


# NNNN@@.1111 mk ultraview
# remote desktop 
# ultraview
