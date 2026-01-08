import sys, os
from backend.app import *
from common.config_read import *
from common.mysql_connect import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=4900)