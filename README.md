[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

[![Build Status](https://travis-ci.org/redaelli/imago-forensics.svg?branch=master)](https://travis-ci.org/redaelli/imago-forensics) [![Requirements Status](https://requires.io/github/redaelli/imago-forensics/requirements.svg?branch=master)](https://requires.io/github/redaelli/imago-forensics/requirements/?branch=master)
[![GitHub license](https://img.shields.io/github/license/Day8/re-frame.svg?style=flat-square)](LICENSE)
# imago-forensics 🕵️
Imago is a python tool that extract digital evidences from images recursively.
This  tool is useful throughout a digital forensic investigation. If you need to extract digital evidences and you have a lot of images, through this tool you will be able to compare them easily. Imago allows to extract the evidences into a CSV file or in a sqlite database. If in a JPEG exif are present GPS coordinates, Imago can extract the longitude and latitude and it can convert them to degrees and to retrieve relevant information like city, nation, zip code...
Imago offers also the possibility to calculate Error Level Analysis, and to detect nudity these functionalities are in BETA.

# Setup

## Setup via pip

1. Install imago:

```console
$ pip install imago
```
2. Once installed, one new binary should be available: :

```console
$ imago 
```
And then it should output the imago's banner


## Requirements:
```
python 2.7
exifread 2.1.2
python-magic 0.4.15
argparse 1.4.0
pillow 5.2.0
nudepy 0.4
imagehash 4.0
geopy 1.16.0

```
# Usage

```
usage: imago.py [-h] -i INPUT [-x] [-g] [-e] [-n] [-d {md5,sha256,sha512,all}]
                [-p {ahash,phash,dhash,whash,all}] [-o OUTPUT] [-s]
                [-t {jpeg,tiff}]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input directory path
  -x, --exif            Extract exif metadata
  -g, --gps             Extract, parse and convert to coordinates, GPS exif
                        metadata from images (if any)It works only with JPEG.
  -e, --ela             Extract, Error Level Analysis image,It works only with
                        JPEG. *BETA*
  -n, --nude            Detect Nudity, It works only with JPEG, *BETA*
  -d {md5,sha256,sha512,all}, --digest {md5,sha256,sha512,all}
                        Calculate perceptual image hashing
  -p {ahash,phash,dhash,whash,all}, --percentualhash {ahash,phash,dhash,whash,all}
                        Calculate hash digest
  -o OUTPUT, --output OUTPUT
                        Output directory path
  -s, --sqli            Keep SQLite file after the computation
  -t {jpeg,tiff}, --type {jpeg,tiff}
                        Select the image, this flag can be JPEG or TIFF, if
                        this argument it is not provided, imago will process
                        all the image types(i.e. JPEG, TIFF)



```
The only required argument is -i which is the base directory from which imago will start to search for image file.
You should also provide at least one type of extraction (i.e. exif, data, gps, digest).

# Example:

```console
$ imago -i /home/solvent/cases/c23/DCIM/ -o /home/solvent/cases/c23/ -x -s -t jpeg -d all
```

Where:
* -i path: is the base directory, where imago will search for file
* -o path: the output directory where imago will save the CSV file, with the extracted metadata
* -x : imago will extract EXIF metadata.
* -s: the temporary SQLite database will not be deleted after the processing.
* -t jpeg: imago will search only for jpeg images.
* -d all: imago will calculate md5, sha256, sha512 for the jpeg images.

# Features:

| Task          | Status        |
| ------------- |:-------------:|
| Recursive directory navigation  | ✔️ |
| file mtime (UTC) | ✔️ |
| file ctime (UTC) | ✔️ |
| file atime (UTC) | ✔️ |
| file size (bytes)| ✔️ |
| MIME type | ✔️ |
| Exif support  | ✔️ |
| CSV export  | ✔️ |
| Sqlite export  | ✔️ |
| md5, sha256, sha512  | ✔️ |
| [Error Level Analysis](https://blackhat.com/presentations/bh-dc-08/Krawetz/Whitepaper/bh-dc-08-krawetz-WP.pdf) | ✔️ BETA |
| Full GPS support  | ✔️ |
| [Nudity detection](https://github.com/hhatto/nude.py) | ✔️ BETA|
| [Perceptual Image Hashing](https://github.com/JohannesBuchner/imagehash) | ✔️|
| [aHash](http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html) | ✔️ |
| [pHash](http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html)| ✔️ |
| [dHash](http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html) | ✔️ |
| [wHash](https://fullstackml.com/2016/07/02/wavelet-image-hash-in-python/)| ✔️ |



# ToDo:



| Task          | Status        |
| ------------- |:-------------:|
| **Test code** | ❌ |
| Comments and Suggestions are welcome | 👍 |


## 📑 Copyright and Licenses
Code copyright 2018 Redaelli.
Code released under the [MIT license](LICENSE).
