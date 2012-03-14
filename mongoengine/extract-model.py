#!/usr/bin/env python

# Reverse engineer a mongoengine Document class skeleton
# from an existing MongoDB collection.

import argparse
from datetime import datetime

import pymongo
import bson

args = None

def main():
    connection = pymongo.Connection(args.host)
    db = connection[args.db]
    collection = db[args.collection]
    make_class(collection)

def make_class(collection):
    print "class %s(Document)" % collection.name.capitalize()
    print "    meta = {"
    print "        'collection': '%s'," % collection.name
    print "        'allow_inheritance': False,"
    print "        'index_background': True,"
    print "        'index_types': False,"
    make_indexes(collection)
    print
    make_fields(collection)
    print
    make_basic_methods(collection)

def make_basic_methods(self):
    print "    def __unicode__(self):"
    print "        raise NotImplementedError"
    print
    print "    def __repr__(self):"
    print "        raise NotImplementedError"

def make_fields(collection):
    fields = {}
    doc_count = 0
    for doc in collection.find().limit(args.docs):
        doc_count += 1
        for field_name, value in doc.iteritems():
            if field_name not in fields:
                fields[field_name] = (0, set())
            count, types = fields[field_name]
            count += 1
            if value is not None:
                types.add(type(value))
            fields[field_name] = (count, types)

    for field_name in sorted(fields.keys()):
        count, types = fields[field_name]
        spec = find_spec(count, doc_count, types)
        print "    %s = %s" % (field_name, spec)
        
field_map = {
    int: 'IntField',
    float: 'FloatField',
    str: 'StringField',
    unicode: 'StringField',
    bool: 'BooleanField',
    dict: 'DictField',
    bson.objectid.ObjectId: 'ObjectIdField',
    datetime: 'DateTimeField',
    }

def find_spec(count, doc_count, types):
    if len(types) > 1:
        return "!! multiple types (%s)" % types
    if len(types) == 0:
        return "StringType()  # No non-None values found, assuming string"
    data_type = types.pop()
    try:
        field_type = field_map[data_type]
    except KeyError:
        return "!! Unknown field type (%s)" % data_type
    return "%s(%s)" % (field_type, "required=True" if count == doc_count else "")
            
def make_indexes(collection):
    info = collection.index_information()
    print "        'indexes': ["
    for data in info.values():
        i = {}
        i['fields'] = tuple(('%s' if direction > 0 else '-%s') % field for field, direction in data['key'])
        if data.get('unique'):
            i['unique'] = True
        if data.get('sparse'):
            i['sparse'] = True
        print '            %s,' % i
    print "        ],"

def parse_command_line():
    parser = argparse.ArgumentParser(description='Reverse engineer mongoengine Document subclass from mongodb collection')
    parser.add_argument('--host', help='mongo db host', default='localhost')
    parser.add_argument('--db', help='mongo db database', default='test')
    parser.add_argument('--docs', help="number of documents to examine while intuiting schema", type=int, default=100)
    parser.add_argument('collection', help='collection name')
    global args
    args = parser.parse_args()

if __name__ == '__main__':
    parse_command_line()
    main()
