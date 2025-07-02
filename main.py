from screen import *

def main():
    app = Application()
    try:
        app.start()
        while app.is_started:
            time.sleep(3)
    except KeyboardInterrupt:
        app.stop()




    return 0

if __name__ == '__main__':
    main()