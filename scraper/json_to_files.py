"""
    Takes the json dump from ASOS and turns it into images sorted into directories for TensorFlow
"""

import json
import os
import urllib2
from shutil import copyfile

# Originally from http://stackoverflow.com/a/22776/4178733
def download_image(url, path):
    u = urllib2.urlopen(url)
    with open(path, 'wb') as f:
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (path, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status


def main():
    with open('men.json') as f:
        data = json.load(f)
        # for item in data:
        #     if item['product_code']:
        #         download_image(item['image_url'], 'men-images/' + item['product_code'] + '.jpg')
        for item in data:
            if item['product_code']:
                if item['colour']:
                    # make directory for colour if it doesn't exit
                    directory = 'sorted_by_colour/' + item['colour']
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    # store image there with same file name
                    copyfile('men-images-processed/' + item['product_code'] + '.jpg', directory
                             + '/' + item['product_code'] + '.jpg')


main()
