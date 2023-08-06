from operator import indexOf
import cryptography
from cryptography.fernet import Fernet
from datetime import datetime
import string, random

def passwordToken(MinLength=100, MaxLength=120):
    #---- Generates a random token that is stored that will be used to encrypt user data ----
    passwordToken = ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation) for _ in range(random.randint(MinLength,MaxLength)))
    RandomTextPoint = random.randrange(len(passwordToken))
    RandomInputToken, RandomInputKey = encryption(''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation) for _ in range(random.randint(100,120))))
    randominputprivateKey =  RandomInputKey.decode("UTF-8") + RandomInputToken.decode("UTF-8")  
    text = passwordToken[:RandomTextPoint] + randominputprivateKey + passwordToken[RandomTextPoint:]
    privateToken, privateKey = encryption(text)
    return privateKey.decode("UTF-8") + ":" + privateToken.decode("UTF-8")   

def generateSessionToken(username, MinLength=100, MaxLength=120):
    #---- Generates a random 128 character long SessionToken 
    sessionToken = ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for _ in range(random.randint(MinLength,MaxLength)))
    return encryption(username + ":" + sessionToken)

def dataEncrpytion(text, MinLength=100, MaxLength=120):
    #---- Generate a random 128 character password with password to show on the servers and files to save ----
    RandomText = ''.join(random.choice(text + string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation) for _ in range(random.randint(MinLength,MaxLength)))
    #---- Creates a random number within the bounds of the length of passwords (basically shoves text in a random location) ----
    TextPoint = random.randrange(len(text))
    RandomTextPoint = random.randrange(len(RandomText))
    RandomToken = passwordToken(MinLength, MaxLength)
    #---- Combine all the random points and text together to store this password ----
    text = text[:TextPoint] + RandomText[:RandomTextPoint] + RandomToken + RandomText[RandomTextPoint:] + text[TextPoint:]
    TextToken, TextKey = encryption(text)
    timestamp = datetime.utcfromtimestamp(Fernet(str.encode(RandomToken.split(":")[0])).extract_timestamp(str.encode(RandomToken.split(":")[1]))).strftime(''.join(random.choice(['%d','%H','%d','%M','%d','%S']) for _ in range(int(MinLength/4),int(MaxLength/2))))
    RandomTextToken, RandomTextKey = encryption(RandomText)
    return TextKey.decode("utf-8") +":" + timestamp[0:random.randint(1, len(timestamp))] +"/" + TextToken.decode("utf-8") + ":" + timestamp[0:random.randint(1, len(timestamp))] +"/" + RandomTextToken.decode("UTF-8") + ":" + timestamp[0:random.randint(1, len(timestamp))] + "/" + RandomTextKey.decode("UTF-8") +":" + timestamp[0:random.randint(1, len(timestamp))]  + "/" + RandomToken

def encryption(text):
    #---- Changes string to byte format ----
    bytetext = str.encode(text)
    #--- Generates a special key ----
    key = Fernet.generate_key()
    encryption_type = Fernet(key)
    #---- Makes Token string an encrypted fernet with the generated key for the byte string ----
    token = encryption_type.encrypt(bytetext)
    #---- Returns encrypted text text format ----
    return token, key

def dataDecryption(EncryptedText):
    ShortenedText = EncryptedText.split(":")[len(EncryptedText.split(":"))-2]
    RandomKey = ShortenedText[ShortenedText.index("/")+1:len(ShortenedText)]
    RandomToken = EncryptedText.split(":")[len(EncryptedText.split(":"))-1]
    timestamp = datetime.utcfromtimestamp(Fernet(str.encode(RandomKey)).extract_timestamp(str.encode(RandomToken))).strftime('%d%H:%d%M:%d%S')
    Textkey = EncryptedText.split(":")[0]
    textToken = CleanToken(EncryptedText.split(":")[1], timestamp)
    RandomtextToken = CleanToken(EncryptedText.split(":")[2], timestamp)
    RandomtextKey = CleanToken(EncryptedText.split(":")[3], timestamp)
    return str(decryption(str.encode(textToken), str.encode(Textkey))).replace(RandomKey +":" + RandomToken, "").replace(str(decryption(str.encode(RandomtextToken), str.encode(RandomtextKey))), "")

def CleanToken(TokenString, timestamp):
    for x in timestamp +"%:dHMS":
        if x+"/" in TokenString:
            cleanToken = TokenString[TokenString.index(x+"/") +2: len(TokenString)]
            if TokenString.index(x+"/") < 30:
                break
    return cleanToken

def decryption(token, key):
    #---- Will decrypt the encrypted text with a token and key ----
    encryption_type = Fernet(key)
    return encryption_type.decrypt(token).decode()
