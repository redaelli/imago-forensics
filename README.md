# imago-forensics 🕵️
Imago is a python tool that extract digital evidences from images recursively.
This  tool is useful throughout a digital forensic investigation. If you need to extract digital evidences and you have a lot of images, through this tool you will be able to compare them easily. Imago allows to extract the evidences into a CSV file or in a sqlite database.

# Installation

## Installation of the requirements via pip:

To install imago requirements simply run:
```
pip install -r requirements.txt

```
## Requirements:
```
python 2.7
exifread version 2.1.2
python-magic version 0.4.15
argparse version 1.2.1
```
# Usage

```
usage: imago.py [-h] -i INPUT [-o OUTPUT] [-s {yes}] [-t {jpeg,tiff}]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output directory path
  -s {yes}, --sqli {yes}
                        Keep SQLite file
  -t {jpeg,tiff}, --type {jpeg,tiff}
                        Image type, can be JPEG or TIFF, if this argument it
                        is not provided, imago will process all the image types(i.e. JPEG, TIFF)
  -d {md5,sha256,sha512,all}, --digest {md5,sha256,sha512,all}
                        Calculate hash digest
```
The only required argument is -i which is the base directory

# Example

```
python imago.py -i /home/solvent/cases/c23/DCIM/ -o /home/solvent/cases/c23/ -s yes -t jpeg -d all
```

Where:
* -i path: is the base directory, where imago will search for file
* -o path: the output directory where imago will save the CSV file, with the extracted metadata
* -s yes: the temporary SQLite database will not be deleted after the processing.
* -t jpeg: imago will search only for jpeg images.
* -d all: imago will calculate md5, sha256, sha512 for the jpeg images.

# ToDo

| Task          | Status        |
| ------------- |:-------------:|
| Exif support  | ✔️ |
| JPEG support  | ✔️ |
| Tiff support  | ✔️ |
| Recursive directory navigation  | ✔️ |
| CSV export  | ✔️ |
| Exif support  | ✔️ |
| Sqlite export  | ✔️ |
| md5, sha256, sha512  | ✔️ |
| ELA | ❌ |
| Filesystem metadata support  | ❌ |
| Full GPS support  | ❌ |
| XMP extraction  | ❌ |


## Copyright and Licenses
Code copyright 2018 Redaelli.
Code released under the [MIT license](LICENSE).
