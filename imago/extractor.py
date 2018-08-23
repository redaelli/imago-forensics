import os,sys
import exifread
import helper
import hashlib
import magic
from PIL import Image, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS, GPSTAGS
import imagehash
import nude
from nude import Nude
import datetime
from geopy.geocoders import Nominatim


def basic_info(filename):
    print ("Extraction of basic information: %s" % (filename,))
    statinfo = os.stat(filename)
    mime = magic.from_file(filename, mime=True)
    helper.sqlite_insert("MIME",mime,os.path.basename(filename))
    helper.sqlite_insert("Size_Bytes",str(statinfo.st_size),os.path.basename(filename))
    helper.sqlite_insert("Last_Modification_Time_UTC",str(datetime.datetime.utcfromtimestamp(statinfo.st_mtime).strftime("%Y-%m-%d %H:%M:%S")),os.path.basename(filename))
    helper.sqlite_insert("Last_Access_Time_UTC",str(datetime.datetime.utcfromtimestamp(statinfo.st_atime).strftime("%Y-%m-%d %H:%M:%S")),os.path.basename(filename))
    helper.sqlite_insert("Creation_Time_UTC",str(datetime.datetime.utcfromtimestamp(statinfo.st_ctime).strftime("%Y-%m-%d %H:%M:%S")),os.path.basename(filename))
    return statinfo, mime

# Extraction of all exif data
def exif_info(filename):
    print ("Extraction of EXIF data from: %s" % (filename,))
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


#modified version of a gist by: https://github.com/ewencp
##BETA##
def ela(filename, output_path):
    print "****ELA is in BETA****"
    if magic.from_file(filename, mime=True) == "image/jpeg":
        quality_level = 85
        tmp_img = os.path.join(output_path,os.path.basename(filename)+".tmp.jpg")
        ela = os.path.join(output_path,os.path.basename(filename)+".ela.jpg")
        image = Image.open(filename)
        image.save(tmp_img, 'JPEG', quality=quality_level)
        tmp_img_file = Image.open(tmp_img)
        ela_image = ImageChops.difference(image, tmp_img_file)
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        scale = 255.0/max_diff
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        ela_image.save(ela)
        os.remove(tmp_img)
    else:
        print "ELA works only with JPEG"


#Modified version of a gist by: https://github.com/erans
def PIL_exif_data_GPS(filename):
    if magic.from_file(filename, mime=True) == "image/jpeg":
        print ("Extraction of GPS data from: %s" % (filename,))
        image = Image.open(filename)
        exif_data = {}
        exif = image._getexif()
        latitude = None
        longitude = None
        if exif:
            for tag, value in exif.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]
                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value
        if "GPSInfo" in exif_data:
            gps_info = exif_data["GPSInfo"]
            gps_longitude = None
            gps_latitude = None
            if "GPSLatitude" in gps_info:
                gps_latitude = gps_info["GPSLatitude"]
            if "GPSLatitudeRef" in gps_info:
                gps_latitude_ref = gps_info["GPSLatitudeRef"]
            if "GPSLongitude" in gps_info:
                gps_longitude = gps_info["GPSLongitude"]
            if "GPSLongitudeRef" in gps_info:
                gps_longitude_ref = gps_info["GPSLongitudeRef"]
            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                latitude = helper.to_degress(gps_latitude)
                if gps_latitude_ref != "N":
                    latitude = 0 - latitude
                longitude = helper.to_degress(gps_longitude)
                if gps_longitude_ref != "E":
                    longitude = 0 - longitude

        helper.sqlite_insert("Parsed_GPS_Latitude",str(latitude),os.path.basename(filename))
        helper.sqlite_insert("Parsed_GPS_Langitude",str(longitude),os.path.basename(filename))

        try:
            if latitude != None and longitude != None:
                geolocator = Nominatim(user_agent="imago-forensics")
                ls = str(latitude)+","+str(longitude)
                location = geolocator.reverse(ls)
                address = location.raw["address"]
                for a in address.keys():
                    helper.sqlite_insert(a,str(address[a]),os.path.basename(filename))
        except:
    		print "Problem during geopy decode"

        return latitude, longitude
    else:
        print "GPS works only with JPEG"
    return None


# based on nude.py
# https://github.com/hhatto/nude.py
# BETA
def detect_nudity(filename):
    if magic.from_file(filename, mime=True) == "image/jpeg":
        print ("Check if the image contains nudity: %s" % (filename,))
        n = Nude(filename)
        n.parse()
        nudity = str(n.result)
        helper.sqlite_insert("Nudity",nudity,os.path.basename(filename))
        return nudity
    else:
        print "Nudity Detection works only with JPEG"
        return None

#based on JohannesBuchner imagehash
#https://github.com/JohannesBuchner/imagehash


def ahash(filename):
    if "image" in magic.from_file(filename, mime=True):
        print ("Calculating aHash of: %s" % (filename,))
        hash = imagehash.average_hash(Image.open(filename))
        helper.sqlite_insert("aHash",str(hash),os.path.basename(filename))
        return hash
    else:
        print "aHash works only with images"
        return None

#based on JohannesBuchner imagehash
#https://github.com/JohannesBuchner/imagehash
def phash(filename):
    if "image" in magic.from_file(filename, mime=True):
        print ("Calculating pHash of: %s" % (filename,))
        hash = imagehash.phash(Image.open(filename))
        helper.sqlite_insert("pHash",str(hash),os.path.basename(filename))
        return hash
    else:
        print "pHash works only with images"
        return None

#based on JohannesBuchner imagehash
#https://github.com/JohannesBuchner/imagehash
def whash(filename):
    if "image" in magic.from_file(filename, mime=True):
        print ("Calculating wHash of: %s" % (filename,))
        hash = imagehash.whash(Image.open(filename))
        helper.sqlite_insert("wHash",str(hash),os.path.basename(filename))
        return hash
    else:
        print "wHash works only with image images"
        return None

#based on JohannesBuchner imagehash
#https://github.com/JohannesBuchner/imagehash
def dhash(filename):
    if "image" in magic.from_file(filename, mime=True):
        print ("Calculating dHash Vertical of: %s" % (filename,))
        hash = imagehash.average_hash(Image.open(filename))
        helper.sqlite_insert("dHash",str(hash),os.path.basename(filename))
        return hash
    else:
        print "dHash vertical works only with image images"
        return None
