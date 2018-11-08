from pathlib import Path


def displayResults(results, path):
    if(len(results)):
        for i, result in enumerate(results):
            id = result[0]
            score = result[1]
            print('{} . DocID[{}] - Score({})'.format(i+1, id, score))
            # print ("postion: {}".format(i+1))
            # print ("score: {}".format(score))
            # print ("doc id: {}".format(id))
    else:
        print("No results to show")


def displayResultsText(results, path="./data/latimesMini/"):
    if(len(results)):
        docs_ids_to_find = [0]*len(results)
        for i, result in enumerate(results):
            id = result[0]
            docs_ids_to_find[i] = id
        docs = getFullText(path, docs_ids_to_find)

        for i, result in enumerate(results):
            id = result[0]
            score = result[1]
            print("position: {}".format(i+1))
            print("score: {}".format(score))
            print("doc id: {}".format(id))
            if id in docs:
                print("full text: {}".format(docs[id]))
            else:
                print("full text for doc {} not found".format(id))
    else:
        print("No results to show")


def getFullText(path, docs_ids_to_find):

    pathlist = Path(path).glob('**/la*')
    docs = dict()

    for newspaper_path in pathlist:
        file = open(newspaper_path, "r")
        currDocId = 0
        isInText = False
        isInParagraph = False
        inDocToFind = False

        currDocumentText = ""
        for line in file:
            if line.startswith("<DOCID>"):
                currDocId = int(line[len("<DOCID> "):-len(" </DOCID>\n")])
                inDocToFind = False
                for doc_id_to_find in docs_ids_to_find:
                    if currDocId == doc_id_to_find:
                        inDocToFind = True
            elif inDocToFind:

                if line.startswith("</DOC>"):
                    # We use the data we accumulate during the process
                    docs[currDocId] = currDocumentText
                    currDocumentText = ""
                elif line.startswith("<TEXT>"):
                    isInText = True
                elif line.startswith("</TEXT>"):
                    isInText = False
                elif line.startswith("<P>") and isInText:
                    isInParagraph = True
                elif line.startswith("</P>") and isInText:
                    isInParagraph = False
                elif line.startswith("<"):
                    pass
                elif isInText and isInParagraph:
                    currDocumentText += line
        file.close()

    return docs


if __name__ == "__main__":
    results = [(2, 0.515215665102005), (1, 0.3872962221503258), (20,0.24924767762422562), (21, 0.22536922246217728), (5, 0.184548731893301)]
    path = "./data/latimesMini/"
    getFullText(path, results)
