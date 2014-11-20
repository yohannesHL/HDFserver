import HDFserver
#from flask import jsonify, abort, request, make_response, url_for
#from flask.views import MethodView
import json,requests




#print HDFserver.DATA_DIR
#HDFserver.run(debug = True)
try:
    print "root"
    req=requests.get("http://127.0.0.1:5000/")

    print req.json()

    print "List Stores"
    req=requests.get("http://127.0.0.1:5000/stores_")
    print req.json()

    print "Reteive Data"
    req=requests.get("http://127.0.0.1:5000/test/table1/10/0")
    print req.json()
except:
    pass