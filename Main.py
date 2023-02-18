from Encrypt import Encrypt
from Decrypt import Decrypt

from multiprocessing import Process

def main():

    # Run the encrypter and decrypter in two different threads
    encrypter = Encrypt()
    decrypter = Decrypt()

    Process(target=encrypter.run).start()
    Process(target=decrypter.run).start()


if __name__ == "__main__":
    main()