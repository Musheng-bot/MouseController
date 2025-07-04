from App.Application import *
from Data.DataManager import *

def main():
    app = Application()
    try:
        app.start()
        while app.is_started:
            time.sleep(3)
    except KeyboardInterrupt:
        print("Exiting...")
        pass

    return 0

def test():

    return 0

if __name__ == '__main__':
    main()