#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import argparse
import extractor
import helper
from os import walk

def main(args=None):
	print """\
##################################################
# imago.py                                       #
# Digital evidences from images!                 #
# Made with <3 by Matteo Redaelli                #
# Twitter: @solventred                           #
##################################################
	"""
	if args is None:
		args = sys.argv[1:]
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--input', help='Input directory path', type=str, required=True)
	parser.add_argument('-x','--exif', help='Extract exif metadata', action='store_true')
	parser.add_argument('-g','--gps', help='Extract, parse and convert to coordinates, GPS exif metadata from images (if any)It works only with JPEG.', action='store_true')
	parser.add_argument('-e','--ela', help='Extract, Error Level Analysis image,It works only with JPEG. *BETA*', action='store_true')
	parser.add_argument('-n','--nude', help='Detect Nudity, It works only with JPEG, *BETA*', action='store_true')
	parser.add_argument('-d','--digest', help='Calculate perceptual image hashing', type=str, choices=["md5", "sha256", "sha512", "all"])
	parser.add_argument('-p','--percentualhash', help='Calculate hash digest', type=str, choices=["ahash", "phash", "dhash","whash","all"])
	parser.add_argument('-o','--output', help='Output directory path', type=str)
	parser.add_argument('-s','--sqli', help='Keep SQLite file after the computation', action='store_true')
	parser.add_argument('-t','--type', help='Select the image, this flag can be JPEG or TIFF, if this argument it is not provided, imago will process all the image types(i.e. JPEG, TIFF)', type=str, choices=["jpeg","tiff"])
	args = parser.parse_args()

	if (args.exif or args.gps or args.ela or args.digest or args.nude or args.percentualhash):

		filetype = ""
		if (args.type == "jpeg"):
			filetype = "image/jpeg"
		elif (args.type == "tiff"):
			filetype = "image/tiff"
		else:
			filetype = "image"
		if args.output:
			output_path = args.output
		else:
			output_path = "."
		base_dir = args.input
		helper.initialize_sqli()
		image_list = list(helper.list_files(base_dir, filetype))
		for filename in image_list:
			print ("Processing %s" % (filename,))
			# Creation of the SQLite row for the file
			helper.image_row("evidences", filename)
			extractor.basic_info(filename)
			if args.nude:
				extractor.detect_nudity(filename)
			if args.gps:
				extractor.PIL_exif_data_GPS(filename)

			if args.percentualhash == "ahash":
				extractor.ahash(filename)
			elif args.percentualhash == "phash":
				extractor.phash(filename)
			elif args.percentualhash == "dhash":
				extractor.dhash(filename)
			elif args.percentualhash == "whash":
				extractor.whash(filename)
			elif args.percentualhash == "all":
				extractor.ahash(filename)
				extractor.phash(filename)
				extractor.whash(filename)
				extractor.dhash(filename)

			if args.digest == "md5":
				extractor.md5(filename)
			elif args.digest == "sha256":
				extractor.sha256(filename)
			elif args.digest == "sha512":
				extractor.sha512(filename)
			elif args.digest == "all":
				extractor.md5(filename)
				extractor.sha256(filename)
				extractor.sha512(filename)
			if args.exif:
				extractor.exif_info(filename)
			if args.ela:
				extractor.ela(filename,output_path)
			print ("Processing of %s completed!" % (filename,))

		# Creation of the file CSV
		helper.create_csv(output_path)
		if not args.sqli:
			os.remove('metadata.db')
		elif args.sqli and args.output:
			os.rename("metadata.db", os.path.join(args.output,"metadata.db"))
	else:
		print("ERROR: Select at least one type of extraction")

if __name__ == "__main__":
    main()
