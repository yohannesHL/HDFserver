#!flask/bin/python

from flask import Flask,make_response,abort
from flask.ext.restful import Api, Resource
import pandas as pd
import os,sys
from configs import DATA_DIR,exts


app = Flask(__name__, static_url_path = "")
api = Api(app)

def output_json(obj, code, headers=None):
    import json
    resp = make_response(json.dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}

api.representations = DEFAULT_REPRESENTATIONS

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET')
	return response

@app.errorhandler(404)
def page_not_found(e):
    return {'Error': 'Resource Not found'},404

def set_data_dir(data_dir):
    global DATA_DIR
    DATA_DIR=data_dir

def DSfiles():
    """
     generator to get all HDF files from the data path defined in DATA_DIR
     yields full filename
    """

    DIR=os.path.abspath(DATA_DIR)

    #walk through data directory
    for root, dirs, files in os.walk(DIR):
        for name in files:
            filename=os.path.join(root,name)
            for ext in exts:
                if filename.endswith(ext):
                    yield filename

def get_datasets():
    #datasets={}
    for dfile in DSfiles():

        with pd.get_store(dfile) as storer:
           #datasets[dfile]=storer.keys()
           yield dfile,storer.keys()
    #return datasets


def get_filename(root):
    ret=[]
    for dfile, dataset in get_datasets():
        for ext in exts:
            if dfile.replace(ext,"").split("\\")[-1]== root:
                ret.append(dfile)
    assert len(ret)==1,"%s data files found , expected 1" % len(ret)

    return ret[0]


def load(root,keys,start,stop):
    filename=get_filename(root)
    with pd.get_store(filename) as storer:
        for key in keys:

            yield key, storer.select(key, start=start, stop=stop)


class Chunks(Resource):
    def get(self,root, keys, chunksz,seek_idx):
        start = chunksz * (seek_idx)
        stop = start + chunksz

        keys = keys.split(',')
        pieces={}

        for piece in load(root,keys, start=start, stop=stop):
            pieces[piece[0]]=piece[1].to_json(orient='index',date_format='iso',date_unit='s')

        if len(pieces) == 0:
            return {'Error': ' Index Out of Range '}
        return pieces
class Keys(Resource):
    def get(self,root):


        #keys = keys.split(',')
        dfile=get_filename(root)
        with pd.get_store(dfile) as storer:
            keys=storer.keys()
        print keys
        return {'keys': keys},201
class Stores(Resource):
    def get(self):
        dsets={}
        for dfile, ds in get_datasets():
            dsets[dfile] = ds

        #keys = keys.split(',')


        return dsets

class Root(Resource):
    def get(self):
        return {
            'status': 'OK',
            'usage': {'/stores_/ ':' To list hdf5 stores in the directory',
                      '/keys/<filename>/':'  To list keys in the hdf5 file. Where <filename> is the hdf5 file with the extension dropped. ',
                      '/test/table1/100/0/':' To retreive data for rows 0 to 99  from table1 in the hdf5 file test.h5'
                      }
        }

api.add_resource(Root, '/')
api.add_resource(Stores, '/stores_/')
api.add_resource(Keys, '/<string:root>/')
api.add_resource(Chunks, '/<string:root>/<string:keys>/<int:chunksz>/<int:seek_idx>/', endpoint = 'chunk')


#TODO: get/set attr  /aribute/key/ or atach comands to post method
#api.add_resource(DomainAPI, '/attr/<root>/<key>/<string:nlist>/', endpoint = 'instruments')

def run(*args,**kwargs):

    app.run(*args,**kwargs)


if __name__ == '__main__':

    aargs=[]

    for arg in sys.argv:
        arg=arg.split("-")[-1].split("=")
        if len(arg)>1:
            if "data_dir" in arg:
                global DATA_DIR
                DATA_DIR=arg[1]
                print "Changed DATA_DIR to %s" % DATA_DIR
                continue
            try :
                int(arg[1])
                aargs.append( "%s=%s" % (arg[0],arg[1]) )
            except :
                #Is String , pad with ''
                aargs.append( "%s='%s'" % (arg[0],arg[1]) )

    if aargs:

        #print 'app.run(' + ",".join(aargs) + ")"
        eval('app.run(' + ",".join(aargs) + ")")
    else:

        app.run(debug = True)


