#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os,sys
import csv
import magic
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


# Temporary Sqli database
# Creation of temporary database
def initialize_sqli(*arg):
	conn = sqlite3.connect('metadata.db')
	c = conn.cursor()
	try:
		c.execute('''CREATE TABLE if not exists evidences
			     (filename text )''')
		conn.commit()
	except:
		print "Problem during table creation"
	finally:
		c.close()
	return True


# Temporary Sqli database
# Creation of a row for each image
def image_row(table, filename):
	conn = sqlite3.connect('metadata.db')
	conn.text_factory = str
	c = conn.cursor()
	c.execute("INSERT INTO %s (filename) VALUES (?)"%(table), (os.path.basename(filename),))
	conn.commit()
	c.close()
	return True


# Creation of final csv
def create_csv(output_path):
	conn = sqlite3.connect('metadata.db')
	conn.text_factory = str
	c = conn.cursor()
	c.execute("SELECT * FROM evidences")
	path_to_file = os.path.join(output_path, "imago.csv")
	with open(path_to_file, "wb") as csv_file:
		csv_writer = csv.writer(csv_file,delimiter=';')
		csv_writer.writerow([i[0] for i in c.description])
		csv_writer.writerows(c)

#insert into sqliteDB
def sqlite_insert(table, value, filename):
	conn = sqlite3.connect('metadata.db')
	c = conn.cursor()
	try:
		c.execute('ALTER TABLE evidences ADD COLUMN "%s" text;' % (table))
		conn.commit()
	except:
		pass
	query = 'UPDATE evidences SET "%s"="%s" WHERE filename = "%s";' % (table,value,filename)
	c.execute(query)
	conn.commit()
	c.close()


# Find all images recursively
def list_files(directory, filetype):
	rootdir = directory
	image_list = []

	for folder, subs, files in os.walk(rootdir):
		for filename in files:
			path_to_file = os.path.join(folder, filename)
			if filetype == "image":
				if "image" in magic.from_file(path_to_file, mime=True):
					image_list.append(path_to_file)

			if magic.from_file(path_to_file, mime=True) == filetype:
				image_list.append(path_to_file)
	return image_list


def to_degress(value):
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)
