import gzip
import shutil
import os
import struct
import wordtraveller.query as query
import wordtraveller.filemanager as fm


def vbyteRec(v):
    if v<128:
        return [v]
    else:
        k = int(v/128)
        v2 = v%128
        b = vbyteRec(v2)
        return vbyteRec(k) + b
def vbyte(v):
    res = vbyteRec(v)
    res[-1] = res[-1]+128
    return res

def compressPLVBYTEFromSavedVocAndPL(filemanager):
    filePLCompressed = open(filemanager.getPathPLCompressed(), "w+b")
    fileVocExit = open(filemanager.getPathVocCompressed(), "w+")
    filePL = open(filemanager.getPathPL(),"rb")
    structScores = struct.Struct("<ff")
    structVocInput = struct.Struct("<lff")
    fileVoc = open(filemanager.getPathVoc(),"r")
    offsetVocEntryPre = 0
    for ligne in fileVoc:
        donnees = ligne.rstrip('\n\r').split(",")
        word = donnees[0]
        offsetVocEntry = int(donnees[1])

#        pl = query.get_posting_list(savedVoc,word, filemanager,False)
#        pl = sorted(pl.items(), key=lambda pl: pl[0])
        offsetVocExit = 0
        valPre = 0

        for x in range(0, offsetVocEntry-offsetVocEntryPre):
            record = filePL.read(filemanager.CONST_SIZE_ON_DISK)
            filed = structVocInput.unpack(record)
            idDoc = filed[0]
            score = filed[1]
            nbOccurenciesInDoc = filed[2]
            resVbyte = vbyte(idDoc-valPre)
            for byteToWrite in resVbyte:
                filePLCompressed.write(byteToWrite.to_bytes(1,"big"))
            record = structScores.pack(score,nbOccurenciesInDoc)
            filePLCompressed.write(record)
            valPre = idDoc
            offsetVocExit += (8+len(resVbyte))
        fileVocExit.write("{},{}\n".format(word, offsetVocExit))
        offsetVocEntryPre = offsetVocEntry
    fileVocExit.close()
    filePLCompressed.close()


def decompressPLVBYTE(filemanager):
    fileVoc = open(filemanager.getPathVocCompressed(), "r")
    fileVocToSave = open(filemanager.getPathVoc(),"w+")
    filePLToSave = open(filemanager.getPathPL(),"w+b")
    
    savedVoc = []
    for ligne in fileVoc:
        donnees = ligne.rstrip('\n\r').split(",")
        word = donnees[0]
        offset = int(donnees[1])
        savedVoc.append((word,offset))

    fileVoc.close()

    structScoreOcc = struct.Struct("<ff")
    structPLExit = struct.Struct("<lff")
    filePLCompressed = open(filemanager.getPathPLCompressed(), "rb")
    nbEntryPL = 0
    for wordAndOffset in savedVoc:
        word = wordAndOffset[0]
        offset = wordAndOffset[1]
        valPre = 0
        nbBytesRed = 0
        
        while nbBytesRed != offset:
            if(nbBytesRed>offset):
                print("ERROR")
            record = filePLCompressed.read(1)
            arrayByte = []
            byte = int.from_bytes(record, byteorder='little')
            arrayByte.append(byte)
            while (byte<128):
                record = filePLCompressed.read(1)
                byte = int.from_bytes(record, byteorder='little')
                arrayByte.append(byte)
            arrayByte[-1]=arrayByte[-1]-128
            nbRes = 0
            for i,byte in enumerate(arrayByte):
                nbRes += byte*(128**(len(arrayByte)-1-i))
            nbBytesRed += len(arrayByte)
            valPre = nbRes +valPre
            nbRes = valPre
            record = filePLCompressed.read(8)
            filed = structScoreOcc.unpack(record)
            score = filed[0]
            nbOcc = filed[1]
            record = structPLExit.pack(nbRes, score, nbOcc)
            filePLToSave.write(record)
            
            nbBytesRed += 8
            nbEntryPL += 1
        fileVocToSave.write("{},{}\n".format(word, nbEntryPL))
    
    filePLToSave.close()
    fileVocToSave.close()
    filePLCompressed.close()

def compressZip(path):
    with open(path, 'rb') as f_in, gzip.open(str(path)+".gz", 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def decompressZip(pathIn, pathOut):
    with gzip.open(pathIn + ".gz", 'rb') as f_in:
        with open(pathOut, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)