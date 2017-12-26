HDF REST server
===============


**HDF REST server** is a simple RESTful service for HDF5 data stores .

#### What is HDFdata store you ask?
HDF5 is a data model, library, and file format for storing and managing data. HDF5 is suitable for handling large datasets. HDF5 file sizes are much smaller than other comparable data files. And it is superior to mySQL in terms of read/write speed.  [learn more here](http://www.pytables.org/moin)

### Description:
The  current implementation provides a RESTful interface to view contents of HDF5 data stores. Proving you the ability to query your data store like `localhost/q/HDFfile/table/LIMIT/chunkNum`.
These data files need to be located in a predefined Directory. GET request are currently handled.
In later updates PUT, POST, DELETE  request will be implemented to allow creating/modifying data stores using the RESTful interface. 


## Getting started
This Package has the following requirements:

 * [pandas](https://github.com/pydata/pandas), and pytables for data handling
 * [Flask](http://flask.pocoo.org/), as the http server
 * [Flask-restful](https://github.com/flask-restful/flask-restful) , to install use: pip install flask-restful

## Install

To install simply run:

        python setup.py install

## Basic Usage

First thing first we need to edit DATA_DIR in the configs.py  to the directory where your data stores are located.
This can achieved in different ways


Firstly you can use *set_data_dir* method  :

    import HDFserver
	HDFserver.set_data_dir( directory )


###Lets Now Run the REST server.

    import HDFserver
	HDFserver.run(port=7000,...)
	


### Via Command Line
You can use one of following commands to start the server 

    python HDFserver.py

####Setting parameters
You can set data directory by supplying data_dir argument. All the usual arguments handled by flask can be included . 

    python HDFserver.py -data_dir=DATA_DIR -port=7000 -host=127.0.0.1


## Consuming

To get a list of hdf5 stores in the directory use:

        /stores_/


To list keys in the hdf5 file. Where <filename> is the hdf5 file with the extension dropped:

        /keys/<filename>/


To retreive data for rows 0 to 99  from table1 in the hdf5 file test.h5:

        /test/table1/100/0/

### Example

        import requests

        print requests.get("http://127.0.0.1:5000/test/table1/100/1").json()


Returns:
   
        {u'table1': u'{"0":{"0":0.7429897161,"1":0.8484121687,"2":0.5145762482,"3":0.1149139957,"4":0.8896877559},
        "1":{"0":0.8473583747,"1":0.7616489838,"2":0.9482270932,"3":0.7261994593,"4":0.6119108996},
        "2":{"0":0.6861526421,"1":0.0728248119,"2":0.3953423794,"3":0.4815486616,"4":0.6398098313}
        }
        }


### Author
Yohannes Libanos

