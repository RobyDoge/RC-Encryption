import random


#recives the primenumber and primiteveroot



primeNumber:int = 0
primitiveRoot:int = 0


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
    def CreateEncryptionKey(self:"Reciver",reciverPublicKey:int)->None:
        self.encryptionKey = (reciverPublicKey**self.secretKey)%self.primeNumber
    def DecryptMessage(self:"Reciver",encryptedMessage:str)->str:
        decryptedMessage:str = ""
        print(f"Encrypted message: {encryptedMessage}")
        for character in encryptedMessage:
            if character.isalpha():
                if character.isupper():
                    decryptedMessage += chr((ord(character)-self.encryptionKey-65)%26+65)
                else:
                    decryptedMessage += chr((ord(character)-self.encryptionKey-97)%26+97)
            else:  
                decryptedMessage += character
        print(f"Decrypted message: {decryptedMessage}")
        return decryptedMessage


reciver:Reciver = Reciver(primeNumber,primitiveRoot)
reciver.CreateKeys()

#send publicKey to sender
#recive publicKey from sender
senderPublicKey:int = 0

reciver.CreateEncryptionKey(senderPublicKey)

#get encrypted message from sender
encryptedMessage:str = ""
decryptedMessage:str = reciver.DecryptMessage(encryptedMessage)
