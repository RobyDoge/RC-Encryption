import random
import socket

class Reciver:
    def __init__(self:"Reciver",primeNumber:int,primitiveRoot:int)->None:
        self.primeNumber:int = primeNumber
        self.primitiveRoot:int = primitiveRoot
        self.secretKey:int = 0
        self.publicKey:int = 0
        self.encryptionKey:int = 0
    def CreateKeys(self:"Reciver")->None:
        self.secretKey = random.randint(1,self.primeNumber)
        self.publicKey = (self.primitiveRoot**self.secretKey)%self.primeNumber
    def CreateEncryptionKey(self:"Reciver",senderPublicKey:int)->None:
        self.encryptionKey = (senderPublicKey**self.secretKey)%self.primeNumber
    def DecryptMessage(self:"Reciver",encryptedMessage:str)->str:
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
    
    def EncryptMessage(self:"Reciver",message:str)->str:
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

def Client():
    host = socket.gethostname()
    port = 12345
    client_socket = socket.socket()
    client_socket.connect((host, port))
    setup:str = client_socket.recv(1024).decode()
    primeNumber,primitiveRoot,senderPublicKey = setup.split(",")
    primeNumber = int(primeNumber)
    primitiveRoot = int(primitiveRoot)
    senderPublicKey = int(senderPublicKey)  
    reciver:Reciver = Reciver(primeNumber,primitiveRoot)
    reciver.CreateKeys()
    client_socket.send(str(reciver.publicKey).encode())
    reciver.CreateEncryptionKey(senderPublicKey)
    
    while True:
        encryptedMessage:str = client_socket.recv(1024).decode()
        decryptedMessage:str = reciver.DecryptMessage(encryptedMessage)
        if decryptedMessage == "bye":
            break
        message = input("Enter your message (Type 'bye' to exit): ")
        encryptedMessage = reciver.EncryptMessage(message)
        client_socket.send(encryptedMessage.encode())
        if(message == "bye"):
            break
    # Close the connection
    client_socket.close()

Client()