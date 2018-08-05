import os,sys
import exifread
import sqlite3
import csv
import argparse
import magic

from os import walk

# Temporary Sqli database
# Creation of temporary database
def initialize_sqli(*arg):
	conn = sqlite3.connect('metadata.db')
	c = conn.cursor()
	try:
		c.execute('''CREATE TABLE if not exists exifdata
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
	return 1

# Creation of final csv
def create_csv(output_path):
	conn = sqlite3.connect('metadata.db')
	conn.text_factory = str
	c = conn.cursor()
	c.execute("SELECT * FROM exifdata")
	path_to_file = os.path.join(output_path, "imago.csv")
	with open(path_to_file, "wb") as csv_file:
		csv_writer = csv.writer(csv_file,delimiter=';')
		csv_writer.writerow([i[0] for i in c.description])
		csv_writer.writerows(c)

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

# Extraction of all exif data
def extract_info(filename):
	print ("Processing %s" % (os.path.basename(filename,)))
	conn = sqlite3.connect('metadata.db')
	c = conn.cursor()
	f = open(filename,'rb')
	try:
		tags = exifread.process_file(f)
		for tag in tags.keys():
		    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
			type_tag = tag.split(" ", 1)[0]
			tag_key = tag.split(" ", 1)[1]
			try:
		    		c.execute('ALTER TABLE exifdata ADD COLUMN "%s" text;' % (tag_key))
				conn.commit()
			except:
		    		pass
			query = 'UPDATE exifdata SET "%s"="%s" WHERE filename = "%s";' % (tag_key,tags[tag],os.path.basename(filename))
			c.execute(query)
			conn.commit()
	except:
		print ("Error Occuring during the processing of %s" % (filename,))
		pass
	c.close()
	return filename



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--input', help='input directory path', type=str, required=True)
	parser.add_argument('-o','--output', help='output directory path', type=str)
	parser.add_argument('-s','--sqli', help='Keep SQLite file', type=str, choices=["yes"])
	parser.add_argument('-t','--type', help='image type, can be JPEG or TIFF, if this argument it is not provided, imago will process all the image types(i.e. JPEG, TIFF)', type=str, choices=["jpeg","tiff"])
	args = parser.parse_args()
	filetype = ""

	if (args.type == "jpeg"):
		filetype = "image/jpeg"
	elif (args.type == "tiff"):
		filetype = "image/tiff"
	else:
		filetype = "image"

	base_dir = args.input
	a = initialize_sqli()
	image_list = list(list_files(base_dir, filetype))
	for filename in image_list:
		image_row("exifdata", filename)
		extract_info(filename)
	if args.output:
		create_csv(args.output)
	else:
		create_csv(".")
	if not args.sqli:
		os.remove('metadata.db')


if __name__ == "__main__":
    main()
