import random
import socket

def CreatePrimitiveRoot(primeNumber:int)->int:
    primitiveRoot:int = 0
    for root in range(1, primeNumber):
        remainders:set = set()
        for power in range(1,primeNumber):
            remainder:int = (root**power)%primeNumber
            if remainder in remainders:
                break
            remainders.add(remainder)
        if len(remainders) == primeNumber-1:
            return root            
    return primitiveRoot   

class Sender:
    def __init__(self:"Sender",primeNumber:int,primitiveRoot:int)->None:
        self.primeNumber:int = primeNumber
        self.primitiveRoot:int = primitiveRoot
        self.secretKey:int = 0
        self.publicKey:int = 0
        self.encryptionKey:int = 0
    def CreateKeys(self:"Sender")->None:
        self.secretKey = random.randint(1,self.primeNumber)
        self.publicKey = (self.primitiveRoot**self.secretKey)
        self.publicKey = self.publicKey%self.primeNumber
    def CreateEncryptionKey(self:"Sender",reciverPublicKey:int)->None:
        self.encryptionKey = (reciverPublicKey**self.secretKey)%self.primeNumber
    def EncryptMessage(self:"Sender",message:str)->str:
        encryptedMessage:str = ""
        for character in message:
            if character.isalpha():
                if character.isupper():
                    encryptedMessage += chr((ord(character)+self.encryptionKey-65)%26+65)
                else:
                    encryptedMessage += chr((ord(character)+self.encryptionKey-97)%26+97)
            else:  
                encryptedMessage += character
        print(f"Encrypted message: {encryptedMessage}")
        return encryptedMessage
    def DecryptMessage(self:"Sender",encryptedMessage:str)->str:
        decryptedMessage:str = ""
        print(f"Encrypted message: {encryptedMessage}")
        for character in encryptedMessage:
            if character.isalpha():
                if character.isupper():
                    decryptedMessage += chr((ord(character)+(26-self.encryptionKey)-65)%26+65)
                else:
                    decryptedMessage += chr((ord(character)+(26-self.encryptionKey)-97)%26+97)
            else:  
                decryptedMessage += character
        print(f"Decrypted message: {decryptedMessage}")
        return decryptedMessage


def Server():
    host = socket.gethostname()
    port = 12345
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    c, address = server_socket.accept()

    #create prime number and primitive root
    primeNumber:int = int(input("Enter the prime number: "))
    primitiveRoot:int = CreatePrimitiveRoot(primeNumber)
    if primitiveRoot == 0:
        Exception("Primitive root not found")
    print(f"Prime number: {primeNumber}, Primitive root: {primitiveRoot}")

    #create the sender class
    sender:Sender = Sender(primeNumber,primitiveRoot)
    sender.CreateKeys()
    setup:str = f"{primeNumber},{primitiveRoot},{sender.publicKey}"
    c.send(setup.encode())
    reciverPublicKey:int =int(c.recv(1024).decode())  
    sender.CreateEncryptionKey(reciverPublicKey)


    while True:
        message:str = input("\nEnter the message:")
        encryptedMessage:str = sender.EncryptMessage(message)
        c.send(encryptedMessage.encode())
        if(message == "bye"):
            break
        reciverMessage:str = c.recv(1024).decode()
        decryptedMessage:str = sender.DecryptMessage(reciverMessage)
        if decryptedMessage == "bye":
            break


    # Close the client connection
    c.close()


 



#send encryptedMessage to receiver


Server()