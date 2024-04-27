import random

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

primeNumber:int = int(input("Enter the prime number: "))
primitiveRoot:int = CreatePrimitiveRoot(primeNumber)
if primitiveRoot == 0:
    Exception("Primitive root not found")
print(f"Prime number: {primeNumber}, Primitive root: {primitiveRoot}")

#send primeNumber and primitiveRoot to receiver
 

class Sender:
    def __init__(self:"Sender",primeNumber:int,primitiveRoot:int)->None:
        self.primeNumber:int = primeNumber
        self.primitiveRoot:int = primitiveRoot
        self.secretKey:int = 0
        self.publicKey:int = 0
        self.encryptionKey:int = 0
    def CreateKeys(self:"Sender")->None:
        self.secretKey = random.randint(1,self.primeNumber)
        self.publicKey = (self.primitiveRoot**self.secretKey)%self.primeNumber
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
            

sender:Sender = Sender(primeNumber,primeNumber)
sender.CreateKeys()

#send publicKey to receiver

#recive publicKey from sender
reciverPublicKey:int = 0
sender.CreateEncryptionKey(reciverPublicKey)
 

message:str = input("\nEnter the message:")
encryptedMessage:str = sender.EncryptMessage(message)

#send encryptedMessage to receiver