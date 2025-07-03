from App.Application import *
from Data.DataManager import *

def main():
    app = Application()
    try:
        app.start()
        while app.is_started:
            time.sleep(3)
    except KeyboardInterrupt:
        pass
    finally:
        app.stop()

    return 0

def test():

    return 0

if __name__ == '__main__':
    test()