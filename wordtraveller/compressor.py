
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

def vbyte(v,firstEntry = True):
    if v<128:
        if firstEntry: 
            v = v + 128
        return [v]
    else:
        k = int(v/128)
        v2 = v%128
        b = vbyte(v2, True)
        
        return vbyte(k,False) + b

def compressPLVBYTE(path,filemanager):
    savedVoc = filemanager.read_vocabulary()
    file = open(path, "w+b")
    for word in savedVoc:
        pl = query.get_posting_list(savedVoc,word, filemanager,False)
        pl = sorted(pl.items(), key=lambda pl: pl[0])
        print(word)
        print(pl)
        structScores = struct.Struct("<ff")
        valPre = 0
        i=0
        for elt in pl:
            if i==0:
                print(elt)
                print(vbyte(elt[0]))
                i=1

            structByte = struct.Struct("<c")
            #TODO : Use to_bytes to simplify EVERYTHING (inclutig vbyte function)
            for byteToWrite in vbyte(elt[0]-valPre):
                #print(byteToWrite.to_bytes(1,"big"))
                record = structByte.pack(byteToWrite.to_bytes(1,"big"))
                file.write(record)
            record = structScores.pack(elt[1][0],elt[1][1])
            file.write(record)
            valPre = elt[0]


def decompressPLVBYTE(path,filemanager):
    savedVoc = filemanager.read_vocabulary()
    file = open(path, "rb")
    structByte = struct.Struct("<c")
    #voc is strictly increasing 1, 2 ,4 for 1, 1 ,2
    record = file.read(1)
    filed = structByte.unpack(record)
    arrayByte = []
    byte = filed[0]
    arrayByte.append(byte)
    while (int(byte)<128):
        record = file.read(1)
        filed = structByte.unpack(record)
        byte = filed[0]
        arrayByte.append(byte)
    arrayByte[-1]=arrayByte[-1]-128
    nbRes = 0
    for byte,i in enumerate(arrayByte):
        nbRes += byte*128**(len(arrayByte)-1-i)
    print(nbRes)
    


def compressZip(path):
    with open(path, 'rb') as f_in, gzip.open(str(path)+'.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)