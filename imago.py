import os,sys
import argparse
import extractor
import helper
from os import walk

def main():
	print """\
##################################################
# imago.py                                       #
# Digital evidences from images!                 #
# Made with <3 by Matteo Redaelli aka solventred #
##################################################
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--input', help='input directory path', type=str, required=True)
	parser.add_argument('-o','--output', help='output directory path', type=str)
	parser.add_argument('-s','--sqli', help='Keep SQLite file', type=str, choices=["yes"])
	parser.add_argument('-t','--type', help='Image type, can be JPEG or TIFF, if this argument it is not provided, imago will process all the image types(i.e. JPEG, TIFF)', type=str, choices=["jpeg","tiff"])
	parser.add_argument('-d','--digest', help='Calculate hash digest', type=str, choices=["md5", "sha256", "sha512", "all"])
	parser.add_argument('-e','--ela', help='Error Level Analysis, works only with JPEG. *BETA*', type=str, choices=["yes"])
	args = parser.parse_args()
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
		helper.image_row("evidences", filename)
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
		extractor.exif_info(filename)
		if args.ela:
			extractor.ela(filename,output_path)
		print ("Processing of %s completed!" % (filename,))
		helper.create_csv(output_path)
	if not args.sqli:
		os.remove('metadata.db')
	elif args.sqli and args.output:
		os.rename("metadata.db", os.path.join(args.output,"metadata.db"))

if __name__ == "__main__":
    main()
