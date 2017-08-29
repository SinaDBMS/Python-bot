from threading import Thread

from flask import Flask
from bot_thread import start_bot_thread

application = Flask(__name__)

# thread1 = Thread(target=threaded_function)
thread2 = Thread(target=start_bot_thread())
# thread1.start()
thread2.start()


@application.route("/")
def hello():
    return "Hello World!"


print("line28")
if __name__ == "__main__":
    application.run()
    print("line31")
