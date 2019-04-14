#!/usr/bin/env python3
"""
Main Wrynn algorithm.
"""

from .database.getter import Getter
import requests


def main():

    getter = Getter()
    getter.download_images('tmp/', 5000, 5000)

    return
if __name__ == '__main__':
    main()
