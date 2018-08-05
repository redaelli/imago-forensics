# imago-forensics 🕵️
Imago is a python tool for extracting digital evidence from images recursively.
This  tool can be useful during a digital forensic investigation, where you have a lot of images and you need to extract metadata information in order to compare the images and find evidences.

# Installation

## Installation via pip:

To install imago.py simply run:
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
                        image type, can be JPEG or TIFF, if this argument it
                        is not provided, imago will process all the image types(i.e. JPEG, TIFF)

```
The only required argument is -i which is the base directory

# Example

python imago.py -i /home/solvent/cases/c23/DCIM/ -o /home/solvent/cases/c23/ -s yes -

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
| Filesystem metadata support  | ❌ |
| Full GPS support  | ❌ |
| XMP extraction  | ❌ |
| XMP export  | ❌ |
