from flask import Flask                                                                    
from flask_jsonrpc import JSONRPC
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api')

import login
import power
import role
import user
import select
import assets

