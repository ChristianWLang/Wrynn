#!/usr/bin/env python3
"""
Getter of images.
"""

from functools import partial

import multiprocessing
import requests
import json
import os


class Getter:
    def __init__(self):
        self.base = 'https://isic-archive.com/api/v1'

    def _write(self, directory, r):

        try:
            _id = r['_id']
            d = directory + _id + '/'

            if not os.path.exists(d):
                os.mkdir(d)

                img = self.download_image(_id)
                metadata = self.download_metadata(_id)

                print('id : {} | Writing'.format(_id))
                with open('{}/metadata.json'.format(d), 'w') as out:
                    json.dump(metadata, out)
                
                with open('{}/img.jpg'.format(d), 'wb') as out:
                    out.write(img)

            return True

        except:
            return False

    def download_metadata(self, _id):
        res = requests.get('{}/image/{}'.format(self.base, _id))
        return res.json()

    def download_image(self, _id):
        res = requests.get('{}/image/{}/download'.format(self.base, _id))
        return res.content

    def download_images(self, directory, limit, step):
        if not os.path.exists(directory):
            os.mkdir(directory)

        func = partial(self._write, directory)

        offset = 0
        res = requests.get('{}/image'.format(self.base), params = {'limit': limit, 'offset': offset}).json()

        while len(res) > 0:

            with multiprocessing.Pool() as pool:
                result_map = pool.map(func, res)
                print(result_map)

            offset += step
            res = requests.get('{}/image'.format(self.base), params = {'limit': limit, 'offset': offset}).json()

        return

    def get_images(self, limit, step):
        res = requests.get('{}/image'.format(self.base), params = {'limit': 100})
        print(res.url)
        return res.json()
