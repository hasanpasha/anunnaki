#!/usr/bin/env python

from anunnaki.main_app import MainApp

import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    app = MainApp()
    app.exec()
