import os,sys
import exifread
import helper
import hashlib

# Extraction of all exif data
def exif_info(filename):
    print ("Extracting EXIF data from: %s" % (filename,))
    f = open(filename,'rb')
    tags = exifread.process_file(f)
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            type_tag = tag.split(" ", 1)[0]
            tag_key = tag.split(" ", 1)[1]
            helper.sqlite_insert(tag_key,tags[tag],os.path.basename(filename))
    return filename


def md5(filename):
    print ("Calculating md5 of: %s" % (filename,))
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
            md5 = hash_md5.hexdigest()
            helper.sqlite_insert("md5",md5,os.path.basename(filename))
    return md5

def sha256(filename):
    print ("Calculating sha256 of: %s" % (filename,))
    hash_sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
            sha256 = hash_sha256.hexdigest()
            helper.sqlite_insert("sha256",sha256,os.path.basename(filename))
    return sha256

def sha512(filename):
    print ("Calculating sha512 of: %s" % (filename,))
    hash_sha512 = hashlib.sha512()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha512.update(chunk)
            sha512 = hash_sha512.hexdigest()
            helper.sqlite_insert("sha512",sha512,os.path.basename(filename))
    return sha512
