from Encrypt import Encrypt
from Decrypt import Decrypt
from App_old import App

from multiprocessing import Process

def main():

    # # Run the encrypter and decrypter in two different threads
    # encrypter = Encrypt()
    # decrypter = Decrypt()

    # Process(target=encrypter.run).start()
    # Process(target=decrypter.run).start()


    # app1 = App()
    # app2 = App()
    # Process(target=app1.run).start()
    # Process(target=app2.run).start()

    app = App()
    app.run()



if __name__ == "__main__":
    main()