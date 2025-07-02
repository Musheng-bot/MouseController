from screen import *

def main():
    app = Application()
    try:
        app.start()
        while app.is_started:
            time.sleep(3)
    except KeyboardInterrupt:
        app.stop()
    finally:
        app.stop()

    return 0

def test():
    a = time.time()
    time.sleep(1.5)
    print(time.time() - a)

if __name__ == '__main__':
    main()