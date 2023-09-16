from anunnaki.main_app import MainApp

import logging

logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)

if __name__ == '__main__':
    app = MainApp()
    app.exec()
