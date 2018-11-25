
# class Compressor:

#     def __init__(self, fileName, workspace="./workspace/"):
#         self.filename = fileName
#         self.workspace = workspace
#         self.extensionVoc = ".vo"
#         self.extensionPL = ".pl"
#         # Record struct format
#         self.struct = struct.Struct("<lff")
#         # create the workspace
#         if not os.path.exists(workspace):
#             print "Workspace directory does not exist"
#             # Todo throw exception
#         list


import gzip
import shutil
import os
import struct
import wordtraveller.query as query
import wordtraveller.filemanager as fm


def vbyteRec(v):
    if v<128:
       # if firstEntry: 
       #     v = v + 128
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
    savedVoc = filemanager.read_vocabulary()
    filePLCompressed = open(filemanager.getPathPLCompressed(), "w+b")
    fileVocExit = open(filemanager.getPathVocCompressed(), "w+")
    structScores = struct.Struct("<ff")
    offsetVoc = 0
    for word in savedVoc:
        pl = query.get_posting_list(savedVoc,word, filemanager,False)
        pl = sorted(pl.items(), key=lambda pl: pl[0])

        valPre = 0
        for elt in pl:
            resVbyte = vbyte(elt[0]-valPre)
            for byteToWrite in resVbyte:
                filePLCompressed.write(byteToWrite.to_bytes(1,"big"))
            record = structScores.pack(elt[1][0],elt[1][1])
            filePLCompressed.write(record)
            valPre = elt[0]
            offsetVoc += (8+len(resVbyte))
        fileVocExit.write("{},{}\n".format(word, offsetVoc))


def decompressPLVBYTE(filemanager):
   #savedVoc = filemanager.read_vocabulary() # TODO : save voc with real offsets (depends on compression)
    fileVoc = open(filemanager.getPathVocCompressed(), "r")
    savedVoc = []
    for ligne in fileVoc:
        donnees = ligne.rstrip('\n\r').split(",")
        word = donnees[0]
        offset = int(donnees[1])
        savedVoc.append((word,offset))

    fileVoc.close()
    print(savedVoc)

    structScoreOcc = struct.Struct("<ff")
    file = open(filemanager.getPathPLCompressed(), "rb")
    nbBytesRed = 0
    for wordAndOffset in savedVoc:
        print(wordAndOffset)
        offset = wordAndOffset[1]
        valPre = 0
        while nbBytesRed != offset:
     #       print(wordAndOffset)
            if(nbBytesRed>offset):
                print("ERROR")
        #file.seek(offset)
    #  structByte = struct.Struct("<c")
        #voc is strictly increasing 1, 2 ,4 for 1, 1 ,2
            record = file.read(1)
        #filed = structByte.unpack(record)
            arrayByte = []
            byte = int.from_bytes(record, byteorder='little')
            arrayByte.append(byte)
       #     print(byte)
            while (byte<128):
                record = file.read(1)
                byte = int.from_bytes(record, byteorder='little')
                arrayByte.append(byte)
           #     print(byte)
            arrayByte[-1]=arrayByte[-1]-128
            print(arrayByte)
            nbRes = 0
            for i,byte in enumerate(arrayByte):
                nbRes += byte*(128**(len(arrayByte)-1-i))
            nbBytesRed += len(arrayByte)
            #todo :substraction among pl
          #  print(nbRes)
           # print(nbRes + valPre)
            valPre = nbRes +valPre
            record = file.read(8)
            filed = structScoreOcc.unpack(record)
            score = filed[0]
            nbOcc = filed[1]
        #    print(score)
        #    print(nbOcc)
            nbBytesRed += 8
       #     print("nbBytesRed"+str(nbBytesRed))
    

    


def compressZip(path):
    with open(path, 'rb') as f_in, gzip.open(str(path)+".gz", 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)