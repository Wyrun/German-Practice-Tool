from demorphy import Analyzer
analyzer = Analyzer(char_subs_allowed=True)
s = analyzer.analyze(u"Menschen")
#for anlyss in s:
#    print(anlyss) #anlyss._lemma _category

import codecs

chars = "esijanrtolcdugmphbyfvkwqxzäüößáéêàâñESIJANRTOLCDUGMPHBYFVKWQXZÄÜÖÉ"
#„"
nextSent = "„!?.\":"

currentHipperDict = ''
alreadyUsed = 0
AIm = 300
BIm = 600

#s = analyzer.analyze("dass")
#s = analyzer.analyze("Dass")

#s = analyzer.analyze("schoßen")
#s = analyzer.analyze("Schoßen")

def SaveColoredSTR(outfilePath, coloredText):
    with codecs.open(outfilePath, "w", "utf8") as file:
        for i in coloredText:
            file.write(str(i))


class MWord:
    def __init__(self, word, unknown_case):
        self.word = word
        self.TEDTT = 0 # times_encountered during the text
        self.words = [word]
        self.unknown_case = unknown_case
        self.lemmas = []
        self.times_encountered = 0
        self.frequency_group = 0
        self.frequency_rank = 0
        self.frequency = 0.
        self.c_frequency = 0.
        self.if_found = False
        self.times_have_enc = 0
        self.status = "unknown"
        self.importance = 3

    def analyze_word(self): # NOT DONE
        s = []
        if(self.unknown_case == False):
            try:
                s = analyzer.analyze(self.word)
            except:
                s = []
            if(len(s) == 0):
                self.lemmas = [self.word]
                #return [word, "NOTFOUND"] # ambiguity
            for i in s:
                self.if_found = True
                if(i._lemma not in self.lemmas):
                    self.lemmas.append(i._lemma)
        else:
            #print(self.word)
            try:
                s = analyzer.analyze(self.word[0].lower() + self.word[1:]) + analyzer.analyze(self.word)
            except:
                s = []
            if(len(s) == 0):
                self.lemmas = [self.word]
                #return [word, "NOTFOUND"] # ambiguity
            for i in s:
                self.if_found = True
                if(i._lemma not in self.lemmas):
                    self.lemmas.append(i._lemma)
        return s

    def blankWordFull(self):
        wordToReturn = ""
        for i in self.word:
            wordToReturn += " "
        return wordToReturn

    def blankWord(self):
        wordToReturn = ""
        for i in self.word:
            wordToReturn += "_"
        return wordToReturn

    def Merge(self, word):
        for i in word.lemmas:
            if(i not in self.lemmas):
                self.lemmas.append(i)
        for i in word.words:
            self.words.append(i)
        self.times_encountered += word.times_encountered
        self.frequency += word.frequency
        self.c_frequency += word.c_frequency
        if(word.if_found == True):
            word.if_found = True
        self.times_have_enc += word.times_have_enc
        if(word.status == 'known'):
            self.status = 'known'
        elif(self.status != 'known'):
            if(word.status == 'learning'):
                self.status = 'learning'
            elif(self.status != 'learning'):
                if(word.status == 'seen'):
                        self.status = 'seen'

    def OutputInfoAsDict(self):
        wordOutput = (str(self.times_encountered)+"\t")
        wordOutput += self.lemmas[0]
        for i in self.lemmas[1:]:
            wordOutput += (str('|')+str(i))
        wordOutput += ("\t"+str(self.frequency_group)+"\t"+str(self.frequency_rank)+"\t"+str(self.frequency)+"\t"+str(self.c_frequency)+"\t"+str(self.times_have_enc)+"\t"+str(self.status))
        return wordOutput

    def OutputInfo(self):
        wordOutput = (str(self.times_encountered)+"\t")
        wordOutput += self.lemmas[0]
        for i in self.lemmas[1:]:
            wordOutput += (str('|')+str(i))
        wordOutput += ("\t"+str(self.frequency_group)+"\t"+str(self.frequency_rank)+"\t"+str(self.frequency)+"\t"+str(self.c_frequency)+"\t"+str(self.times_have_enc)+"\t"+str(self.status))
        return wordOutput

def CopyWord(Word):
    CWord = MWord(Word.word, Word.unknown_case)

    CWord.word = Word.word
    CWord.words = Word.words
    CWord.unknown_case = Word.unknown_case
    CWord.lemmas = Word.lemmas
    CWord.times_encountered = Word.times_encountered
    CWord.frequency_group = Word.frequency_group
    CWord.frequency_rank = Word.frequency_rank
    CWord.frequency = Word.frequency
    CWord.c_frequency = Word.c_frequency
    CWord.if_found = Word.if_found
    CWord.times_have_enc = Word.times_have_enc
    CWord.status = Word.status

    return CWord

class MText:
    def __init__(self, path):
        self.text = ""
        self.words = []
        self.amount_of_words = 0
        self.path = path

    def ProcessTextWords(self):
        for i in range(len(self.words)):
            self.words[i].analyze_word()
        i = 0
        while(i < len(self.words)):
            if(i % 400 == 0):
                print("loading...")
            j = i + 1
            breaking = False
            while(j < len(self.words)):
                if(i != j):
                    for lemma in self.words[i].lemmas:
                        if(lemma in self.words[j].lemmas):
                            #print(self.words[i].word, self.words[i].times_encountered, self.words[i].lemmas, i)
                            #print(self.words[j].word, self.words[j].times_encountered, self.words[j].lemmas, j)
                            self.words[j].Merge(self.words[i])
                            #print(self.words[j].words, self.words[j].times_encountered, self.words[j].lemmas)
                            self.words = self.words[:i] + self.words[i + 1:]
                            if(i < j):
                                j -= 1
                            i -= 1
                            breaking = True
                            break
                if(breaking):
                    break
                j += 1
            i += 1

        # sorting:
        i2i = 0
        for wall in range(len(self.words) - 1):
            #print(wall, sorted[0])
            if(i2i % 3000 == 0):
                print("loading...")
            maxF = wall
            for i in range(wall + 1, len(self.words)):
                if(int(self.words[maxF].times_encountered) < int(self.words[i].times_encountered)):
                    #print(sorted[wall], sorted[maxF], sorted[i])
                    maxF = i
            CWord = CopyWord(self.words[wall])
            self.words[wall] = CopyWord(self.words[maxF])
            self.words[maxF] = CopyWord(CWord)
            i2i += 1

        # detailing:
        frequency_Group = 1
        frequency_Rank = 1
        for i in range(len(self.words)):
            if(i > 0 and self.words[i - 1].times_encountered > self.words[i].times_encountered):
                frequency_Group += 1
                frequency_Rank = i + 1
            self.words[i].frequency_group = frequency_Group
            self.words[i].frequency_rank = frequency_Rank
            percentage = 100. * self.words[i].times_encountered
            self.words[i].frequency = (percentage / self.amount_of_words)
            if(i == 0):
                self.words[i].c_frequency = self.words[i].frequency
            else:
                self.words[i].c_frequency = (self.words[i - 1].c_frequency + self.words[i].frequency)


    def saveDictionary(self, currentDictPath):
        with codecs.open(currentDictPath, "w", "utf8") as file:
            file.write(str(self.amount_of_words)+"\n")
            for i in self.words:
                file.write(i.OutputInfoAsDict()+"\n")

    def changeWordStatus(self, currentWord, status):
        for i in range(len(self.words)):
            for lemma in currentWord.lemmas:
                if(lemma in self.words[i].lemmas):
                    self.words[i].status = status
                    return "Done"

    def markWordAsEncountered(self, currentWord):
        for i in range(len(self.words)):
            for lemma in currentWord.lemmas:
                if(lemma in self.words[i].lemmas):
                    self.words[i].times_have_enc += 1
                    return "Done"


    def CurrentKnowledge(self, seenRequired, learningRequired, knowRequired):
        known = [0, 0.] # amount and percentage
        learning = [0, 0.]
        seen = [0, 0.]
        unknown = [0, 0.]
        asKnown = [0, 0.]
        asLearning = [0, 0.]
        asSeen = [0, 0.]
        asUnknownButImp = [0, 0.]
        asUnknown = [0, 0.]
        for i in self.words:
            if(i.status == 'known'):
                known[0] += 1
                known[1] += float(i.frequency)
            elif(i.status == 'learning'):
                learning[0] += 1
                learning[1] += float(i.frequency)
            elif(i.status == 'seen'):
                seen[0] += 1
                seen[1] += float(i.frequency)
            else:
                unknown[0] += 1
                unknown[1] += float(i.frequency)


            if(i.status == 'known' or int(i.times_have_enc) >= knowRequired):
                asKnown[0] += 1
                asKnown[1] += float(i.frequency)
            elif(i.status == 'learning' or int(i.times_have_enc) >= learningRequired):
                asLearning[0] += 1
                asLearning[1] += float(i.frequency)
            elif(i.status == 'seen' or int(i.times_have_enc) >= seenRequired):
                asSeen[0] += 1
                asSeen[1] += float(i.frequency)
            elif(i.importance < 3):
                asUnknownButImp[0] += 1
                asUnknownButImp[1] += float(i.frequency)
            else:
                asUnknown[0] += 1
                asUnknown[1] += float(i.frequency)
        return [known, learning, seen, unknown, asKnown, asLearning, asSeen, asUnknownButImp, asUnknown]

    def AddDictInfo(self, currentDict):
        for i in range(len(self.words)):
            breaking = False
            for j in range(len(currentDict.words)):
                for lemma in self.words[i].lemmas:
                    if(lemma in currentDict.words[j].lemmas):
                        self.words[i].times_have_enc = currentDict.words[j].times_have_enc
                        self.words[i].status = currentDict.words[j].status
                        self.words[i].importance = currentDict.words[j].importance
                        breaking = True
                        break
                if(breaking):
                    break

    def AddEncountered(self, currentFile):
        for i in range(len(currentFile.words)):
            breaking = False
            for j in range(len(self.words)):
                for lemma in currentFile.words[i].lemmas:
                    if(lemma in self.words[j].lemmas):
                        self.words[j].times_have_enc += currentFile.words[i].times_encountered
                        breaking = True
                        break
                if(breaking):
                    break

    def ZeroEncounters(self):
        for i in range(len(self.words)):
            self.words[i].times_have_enc = 0

    def AddEncounteredIgnoringRare(self, currentFile):
        for i in range(len(currentFile.words)):
            breaking = False
            if(currentFile.words[i].importance < 3):
                for j in range(len(self.words)):
                    for lemma in currentFile.words[i].lemmas:
                        if(lemma in self.words[j].lemmas):
                            self.words[j].times_have_enc += currentFile.words[i].times_encountered
                            breaking = True
                            break
                    if(breaking):
                        break


    def SaveTextRes(self, currentOutFilePath, whichWords, seenRequired, learningRequired, knowRequired):
        with codecs.open(currentOutFilePath, "w", "utf8") as file:
            file.write(str(self.amount_of_words)+"\n")
            for i in self.words:
                #line[1] = str(line[1])
                #if(i.if_found != 'e'):
                #    if('N' in whichWords):
                #        file.write(str(i[0])+"\t"+str(i[1])+"\t"+str(i[2])+"\t"+str(i[3])+"\t"+str(i[4])+"\t"+str(i[5])+"\t"+str(i[6])+"\t"+str("0")+"\t"+str("unknown")+"\n")
                if('K' in whichWords and (i.status == "known" or int(i.times_have_enc) >= knowRequired)):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('k' in whichWords and i.status == "known"):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('L' in whichWords and ((i.status == "learning" and int(i.times_have_enc) < knowRequired) or (i.status != "known" and int(i.times_have_enc) >= learningRequired and int(i.times_have_enc) < knowRequired))):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('l' in whichWords and i.status == "learning"):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('S' in whichWords and ((i.status == "seen" and int(i.times_have_enc) < learningRequired) or (i.status != "learning" and i.status != "known" and int(i.times_have_enc) >= seenRequired and int(i.times_have_enc) < learningRequired))):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('s' in whichWords and i.status == "seen"):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('U' in whichWords and (i.status != "seen" and i.status != "learning" and i.status != "known" and int(i.times_have_enc) < seenRequired)):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('u' in whichWords and i.status == "unknown"):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")

    def SaveTextResByEncount(self, currentOutFilePath, whichWords, seenRequired, learningRequired, knowRequired):
        with codecs.open(currentOutFilePath, "w", "utf8") as file:
            file.write(str(self.amount_of_words)+"\n")
            for i in self.words:
                #line[1] = str(line[1])
                #if(i.if_found != 'e'):
                #    if('N' in whichWords):
                #        file.write(str(i[0])+"\t"+str(i[1])+"\t"+str(i[2])+"\t"+str(i[3])+"\t"+str(i[4])+"\t"+str(i[5])+"\t"+str(i[6])+"\t"+str("0")+"\t"+str("unknown")+"\n")
                if('K' in whichWords and (i.status == "known" or int(i.times_have_enc) >= knowRequired)):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('k' in whichWords and i.status == "known"):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('L' in whichWords and ((i.status == "learning" and int(i.times_have_enc) < knowRequired) or (i.status != "known" and int(i.times_have_enc) >= learningRequired and int(i.times_have_enc) < knowRequired))):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('l' in whichWords and i.status == "learning"):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('S' in whichWords and ((i.status == "seen" and int(i.times_have_enc) < learningRequired) or (i.status != "learning" and i.status != "known" and int(i.times_have_enc) >= seenRequired and int(i.times_have_enc) < learningRequired))):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('s' in whichWords and i.status == "seen"):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('U' in whichWords and (i.status != "seen" and i.status != "learning" and i.status != "known" and int(i.times_have_enc) < seenRequired)):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")
                elif('u' in whichWords and i.status == "unknown"):
                    if(str(i.importance) in whichWords):
                        file.write(i.OutputInfoAsDict()+"\n")

    def EncTTextRes(self, whichWords, seenRequired, learningRequired, knowRequired):
        TERes = 0
        for i in self.words:
            #line[1] = str(line[1])
            #if(i.if_found != 'e'):
            #    if('N' in whichWords):
            #        file.write(str(i[0])+"\t"+str(i[1])+"\t"+str(i[2])+"\t"+str(i[3])+"\t"+str(i[4])+"\t"+str(i[5])+"\t"+str(i[6])+"\t"+str("0")+"\t"+str("unknown")+"\n")
            if('K' in whichWords and (i.status == "known" or int(i.times_have_enc) >= knowRequired)):
                if(str(i.importance) in whichWords):
                    TERes += i.times_have_enc
            elif('k' in whichWords and i.status == "known"):
                if(str(i.importance) in whichWords):
                    TERes += i.times_have_enc
            elif('L' in whichWords and ((i.status == "learning" and int(i.times_have_enc) < knowRequired) or (i.status != "known" and int(i.times_have_enc) >= learningRequired and int(i.times_have_enc) < knowRequired))):
                if(str(i.importance) in whichWords):
                    TERes += i.times_have_enc
            elif('l' in whichWords and i.status == "learning"):
                if(str(i.importance) in whichWords):
                    TERes += i.times_have_enc
            elif('S' in whichWords and ((i.status == "seen" and int(i.times_have_enc) < learningRequired) or (i.status != "learning" and i.status != "known" and int(i.times_have_enc) >= seenRequired and int(i.times_have_enc) < learningRequired))):
                if(str(i.importance) in whichWords):
                    TERes += i.times_have_enc
            elif('s' in whichWords and i.status == "seen"):
                if(str(i.importance) in whichWords):
                    TERes += i.times_have_enc
            elif('U' in whichWords and (i.status != "seen" and i.status != "learning" and i.status != "known" and int(i.times_have_enc) < seenRequired)):
                if(str(i.importance) in whichWords):
                    TERes += i.times_have_enc
            elif('u' in whichWords and i.status == "unknown"):
                if(str(i.importance) in whichWords):
                    TERes += i.times_have_enc
        return TERes

    def wilEncounterTextRes(self, whichWords, seenRequired, learningRequired, knowRequired):
        TERes = 0
        for i in self.words:
            #line[1] = str(line[1])
            #if(i.if_found != 'e'):
            #    if('N' in whichWords):
            #        file.write(str(i[0])+"\t"+str(i[1])+"\t"+str(i[2])+"\t"+str(i[3])+"\t"+str(i[4])+"\t"+str(i[5])+"\t"+str(i[6])+"\t"+str("0")+"\t"+str("unknown")+"\n")
            if('K' in whichWords and (i.status == "known" or int(i.times_have_enc) >= knowRequired)):
                if(str(i.importance) in whichWords):
                    TERes += i.times_encountered
            elif('k' in whichWords and i.status == "known"):
                if(str(i.importance) in whichWords):
                    TERes += i.times_encountered
            elif('L' in whichWords and ((i.status == "learning" and int(i.times_have_enc) < knowRequired) or (i.status != "known" and int(i.times_have_enc) >= learningRequired and int(i.times_have_enc) < knowRequired))):
                if(str(i.importance) in whichWords):
                    TERes += i.times_encountered
            elif('l' in whichWords and i.status == "learning"):
                if(str(i.importance) in whichWords):
                    TERes += i.times_encountered
            elif('S' in whichWords and ((i.status == "seen" and int(i.times_have_enc) < learningRequired) or (i.status != "learning" and i.status != "known" and int(i.times_have_enc) >= seenRequired and int(i.times_have_enc) < learningRequired))):
                if(str(i.importance) in whichWords):
                    TERes += i.times_encountered
            elif('s' in whichWords and i.status == "seen"):
                if(str(i.importance) in whichWords):
                    TERes += i.times_encountered
            elif('U' in whichWords and (i.status != "seen" and i.status != "learning" and i.status != "known" and int(i.times_have_enc) < seenRequired)):
                if(str(i.importance) in whichWords):
                    TERes += i.times_encountered
            elif('u' in whichWords and i.status == "unknown"):
                if(str(i.importance) in whichWords):
                    TERes += i.times_encountered
        return TERes

    def ColorWord(self, word, seenRequired, learningRequired, knowRequired):
        color = 'black'
        wordFound = True
        word.analyze_word()

        i = 0
        for i in range(len(currentHipperDict.words)):
            breaking = False
            for lemma in word.lemmas:
                if(lemma in currentHipperDict.words[i].lemmas):
                    word.status = currentHipperDict.words[i].status
                    word.times_have_enc = currentHipperDict.words[i].times_have_enc
                    breaking = True
                    break
            if(breaking):
                break
            i += 1

        dictWord = i
        A2Words = AIm
        B1Words = BIm
        wordC = 3
        if(dictWord < A2Words):
            wordC = 1
        elif(dictWord < B1Words):
            wordC = 2
        else:
            wordC = 3


        if(word.status == 'known' or int(word.times_have_enc) >= knowRequired):
            color = 'green'
        elif(word.status == 'learning' or int(word.times_have_enc) >= learningRequired):
            if(wordC == 1 or wordC == 2):
                color = 'yellow'
            else:
                color = 'black' #changed
        elif(word.status == 'seen' or int(word.times_have_enc) >= seenRequired):
            if(wordC == 1):
                color = 'blue'
            elif(wordC == 2):
                color = 'purple'
            else:
                color = 'black'
        else:
            if(wordC == 1):
                color = 'pink'
            elif(wordC == 2):
                color = 'red'
            else:
                color = 'black'

        if(color == 'black'):
            return [word.word]
        elif(color == 'yellow'):
            return ['<font color="#fffa00">', word.word, '</font>']
        elif(color == 'green'):
            return ['<font color="#55ff55">', word.word, '</font>']
        elif(color == 'purple'):
            return ['<font color="#a912ff">', word.word, '</font>']
        elif(color == 'pink'):
            return ['<font color="#ff25a3">', word.word, '</font>']
        elif(color == 'red'):
            return ['<font color="#ef4b4b">', word.word, '</font>']
        elif(color == 'blue'):
            return ['<font color="#3fc1c9">', word.word, '</font>']
        return [word.word]

    def ColorWordWE(self, word, seenRequired, learningRequired, knowRequired):
        color = 'black'
        wordFound = True

        wordC = 0
        for i in range(len(self.words)):
            breaking = False
            for lemma in word.lemmas:
                if(lemma in self.words[i].lemmas):
                    word.status = self.words[i].status
                    word.times_have_enc = self.words[i].times_have_enc
                    wordC = self.words[i].importance
                    breaking = True
                    break
            if(breaking):
                break




        if(word.status == 'known' or int(word.times_have_enc) >= knowRequired):
            color = 'green'
        elif(word.status == 'learning' or int(word.times_have_enc) >= learningRequired):
            if(wordC == 1 or wordC == 2):
                color = 'yellow'
            else:
                color = 'black'
        elif(word.status == 'seen' or int(word.times_have_enc) >= seenRequired):
            if(wordC == 1):
                color = 'blue'
            elif(wordC == 2):
                color = 'purple'
            else:
                color = 'black'
        else:
            if(wordC == 1):
                color = 'pink'
            elif(wordC == 2):
                color = 'red'
            else:
                color = 'black'

        if(color == 'black'):
            return [word.word]
        elif(color == 'yellow'):
            return ['<font color="#fffa00">', word.word, '</font>']
        elif(color == 'green'):
            return ['<font color="#55ff55">', word.word, '</font>']
        elif(color == 'purple'):
            return ['<font color="#a912ff">', word.word, '</font>']
        elif(color == 'pink'):
            return ['<font color="#ff25a3">', word.word, '</font>']
        elif(color == 'red'):
            return ['<font color="#ef4b4b">', word.word, '</font>']
        elif(color == 'blue'):
            return ['<font color="#3fc1c9">', word.word, '</font>']
        return [word.word]

    def ColorWordWEAKNS(self, word, seenRequired, learningRequired, knowRequired):
        color = 'black'
        wordFound = True

        wordC = 0
        for i in range(len(self.words)):
            breaking = False
            for lemma in word.lemmas:
                if(lemma in self.words[i].lemmas):
                    word.status = self.words[i].status
                    word.times_have_enc = self.words[i].times_have_enc
                    wordC = self.words[i].importance
                    breaking = True
                    break
            if(breaking):
                break




        if(word.status == 'known' or int(word.times_have_enc) >= knowRequired):
            color = 'green'
        elif(word.status == 'learning' or int(word.times_have_enc) >= learningRequired):
            if(wordC == 1 or wordC == 2):
                color = 'yellow'
            else:
                color = 'black'
        elif(word.status == 'seen' or int(word.times_have_enc) >= seenRequired):
            if(wordC == 1):
                color = 'blue'
            elif(wordC == 2):
                color = 'purple'
            else:
                color = 'black'
        else:
            if(wordC == 1):
                color = 'pink'
            elif(wordC == 2):
                color = 'red'
            else:
                color = 'black'

        if(color == 'black'):
            return [word.word]
        elif(color == 'yellow'):
            return ['<font color="#fffa00">', word.word, '</font>']
        elif(color == 'green'):
            return ['<font color="#55ff55">', word.blankWordFull(), '</font>']
        elif(color == 'purple'):
            return ['<font color="#a912ff">', word.word, '</font>']
        elif(color == 'pink'):
            return ['<font color="#ff25a3">', word.word, '</font>']
        elif(color == 'red'):
            return ['<font color="#ef4b4b">', word.word, '</font>']
        elif(color == 'blue'):
            return ['<font color="#3fc1c9">', word.word, '</font>']
        return [word.word]

    def ColorWordWEAK(self, word, seenRequired, learningRequired, knowRequired):
        color = 'black'
        wordFound = True

        wordC = 0
        for i in range(len(self.words)):
            breaking = False
            for lemma in word.lemmas:
                if(lemma in self.words[i].lemmas):
                    word.status = self.words[i].status
                    word.times_have_enc = self.words[i].times_have_enc
                    wordC = self.words[i].importance
                    breaking = True
                    break
            if(breaking):
                break




        if(word.status == 'known' or int(word.times_have_enc) >= knowRequired):
            color = 'green'
        elif(word.status == 'learning' or int(word.times_have_enc) >= learningRequired):
            if(wordC == 1 or wordC == 2):
                color = 'yellow'
            else:
                color = 'black'
        elif(word.status == 'seen' or int(word.times_have_enc) >= seenRequired):
            if(wordC == 1):
                color = 'blue'
            elif(wordC == 2):
                color = 'purple'
            else:
                color = 'black'
        else:
            if(wordC == 1):
                color = 'pink'
            elif(wordC == 2):
                color = 'red'
            else:
                color = 'black'

        if(color == 'black'):
            return [word.word]
        elif(color == 'yellow'):
            return ['<font color="#fffa00">', word.word, '</font>']
        elif(color == 'green'):
            return ['<font color="#55ff55">', word.blankWord(), '</font>']
        elif(color == 'purple'):
            return ['<font color="#a912ff">', word.word, '</font>']
        elif(color == 'pink'):
            return ['<font color="#ff25a3">', word.word, '</font>']
        elif(color == 'red'):
            return ['<font color="#ef4b4b">', word.word, '</font>']
        elif(color == 'blue'):
            return ['<font color="#3fc1c9">', word.word, '</font>']
        return [word.word]


    def ColorSTR(self, currentOutFilePath, seenRequired, learningRequired, knowRequired):
        coloredText = []
        with codecs.open(self.path, "r", "utf8") as file:
            for line in file:
                lastSentence = 0
                unknown_case = True
                #while(len(line) > 0 and (line[-1] == " " or line[-1] == "\n")):
                #    line = line[:-1]

                if(len(line) < 4):
                    coloredText.append(line)
                    continue
                #words = [] # word = ["Ich", "mightCase"]

                c = 0
                firstWC = 0
                FNonWC = 0

                while(c < len(line)):
                    if(line[c] in chars):
                        if(c == 0 or (c > 0 and line[c - 1] not in chars)):
                            firstWC = c
                            coloredText.append(line[FNonWC:c])
                        if(c == len(line) - 1):
                            word = MWord(line[firstWC:], unknown_case)
                            TextData.words.append(word)
                            TextData.amount_of_words += 1
                            word = self.ColorWord(word, seenRequired, learningRequired, knowRequired)
                            for i in word:
                                coloredText.append(i)
                            unknown_case = False
                    else:
                        if(c != 0 and line[c - 1] in chars):
                            FNonWC = c
                            word = MWord(line[firstWC:c], unknown_case)
                            word = self.ColorWord(word, seenRequired, learningRequired, knowRequired)
                            for i in word:
                                coloredText.append(i)
                            mightCase = False
                        if(line[c] in nextSent or c == 0):
                            mightCase = True
                        if(c == len(line) - 1):
                            coloredText.append(line[FNonWC:])
                    c += 1

            return coloredText

    def ColorSTRWE(self, currentOutFilePath, seenRequired, learningRequired, knowRequired):
        coloredText = []
        with codecs.open(self.path, "r", "utf8") as file:
            for line in file:
                lastSentence = 0
                unknown_case = True
                #while(len(line) > 0 and (line[-1] == " " or line[-1] == "\n")):
                #    line = line[:-1]

                if(len(line) < 4):
                    coloredText.append(line)
                    continue
                #words = [] # word = ["Ich", "mightCase"]

                c = 0
                firstWC = 0
                FNonWC = 0

                while(c < len(line)):
                    if(line[c] in chars):
                        if(c == 0 or (c > 0 and line[c - 1] not in chars)):
                            firstWC = c
                            coloredText.append(line[FNonWC:c])
                        if(c == len(line) - 1):
                            word = MWord(line[firstWC:], unknown_case)
                            TextData.words.append(word)
                            TextData.amount_of_words += 1
                            word.analyze_word()
                            wordToAdd = word
                            word = self.ColorWordWE(word, seenRequired, learningRequired, knowRequired)

                            self.markWordAsEncountered(wordToAdd)
                            for i in word:
                                coloredText.append(i)
                            unknown_case = False
                    else:
                        if(c != 0 and line[c - 1] in chars):
                            FNonWC = c
                            word = MWord(line[firstWC:c], unknown_case)

                            word.analyze_word()
                            wordToAdd = word
                            word = self.ColorWordWE(word, seenRequired, learningRequired, knowRequired)

                            self.markWordAsEncountered(wordToAdd)
                            for i in word:
                                coloredText.append(i)
                            mightCase = False
                        if(line[c] in nextSent or c == 0):
                            mightCase = True
                        if(c == len(line) - 1):
                            coloredText.append(line[FNonWC:])
                    c += 1

            return coloredText

    def ColorSTRWEAK(self, currentOutFilePath, seenRequired, learningRequired, knowRequired):
        coloredText = []
        with codecs.open(self.path, "r", "utf8") as file:
            for line in file:
                lastSentence = 0
                unknown_case = True
                #while(len(line) > 0 and (line[-1] == " " or line[-1] == "\n")):
                #    line = line[:-1]

                if(len(line) < 4):
                    coloredText.append(line)
                    continue
                #words = [] # word = ["Ich", "mightCase"]

                c = 0
                firstWC = 0
                FNonWC = 0

                while(c < len(line)):
                    if(line[c] in chars):
                        if(c == 0 or (c > 0 and line[c - 1] not in chars)):
                            firstWC = c
                            coloredText.append(line[FNonWC:c])
                        if(c == len(line) - 1):
                            word = MWord(line[firstWC:], unknown_case)
                            TextData.words.append(word)
                            TextData.amount_of_words += 1
                            word.analyze_word()
                            wordToAdd = word
                            word = self.ColorWordWEAK(word, seenRequired, learningRequired, knowRequired)

                            self.markWordAsEncountered(wordToAdd)
                            for i in word:
                                coloredText.append(i)
                            unknown_case = False
                    else:
                        if(c != 0 and line[c - 1] in chars):
                            FNonWC = c
                            word = MWord(line[firstWC:c], unknown_case)

                            word.analyze_word()
                            wordToAdd = word
                            word = self.ColorWordWEAK(word, seenRequired, learningRequired, knowRequired)

                            self.markWordAsEncountered(wordToAdd)
                            for i in word:
                                coloredText.append(i)
                            mightCase = False
                        if(line[c] in nextSent or c == 0):
                            mightCase = True
                        if(c == len(line) - 1):
                            coloredText.append(line[FNonWC:])
                    c += 1

            return coloredText
    def ColorSTRWEAKNS(self, currentOutFilePath, seenRequired, learningRequired, knowRequired):
        coloredText = []
        with codecs.open(self.path, "r", "utf8") as file:
            for line in file:
                lastSentence = 0
                unknown_case = True
                #while(len(line) > 0 and (line[-1] == " " or line[-1] == "\n")):
                #    line = line[:-1]

                if(len(line) < 4):
                    coloredText.append(line)
                    continue
                #words = [] # word = ["Ich", "mightCase"]

                c = 0
                firstWC = 0
                FNonWC = 0

                while(c < len(line)):
                    if(line[c] in chars):
                        if(c == 0 or (c > 0 and line[c - 1] not in chars)):
                            firstWC = c
                            coloredText.append(line[FNonWC:c])
                        if(c == len(line) - 1):
                            word = MWord(line[firstWC:], unknown_case)
                            TextData.words.append(word)
                            TextData.amount_of_words += 1
                            word.analyze_word()
                            wordToAdd = word
                            word = self.ColorWordWEAKNS(word, seenRequired, learningRequired, knowRequired)

                            self.markWordAsEncountered(wordToAdd)
                            for i in word:
                                coloredText.append(i)
                            unknown_case = False
                    else:
                        if(c != 0 and line[c - 1] in chars):
                            FNonWC = c
                            word = MWord(line[firstWC:c], unknown_case)

                            word.analyze_word()
                            wordToAdd = word
                            word = self.ColorWordWEAKNS(word, seenRequired, learningRequired, knowRequired)

                            self.markWordAsEncountered(wordToAdd)
                            for i in word:
                                coloredText.append(i)
                            mightCase = False
                        if(line[c] in nextSent or c == 0):
                            mightCase = True
                        if(c == len(line) - 1):
                            coloredText.append(line[FNonWC:])
                    c += 1

            return coloredText

def Clean(currentFile, currentOutFilePath):
    Text = ""
    with codecs.open(currentFile.path, "r", "utf8") as file1:
    	i = -1
    	music = False
    	it = 0
    	file = []
    	for line in file1:
    		file.append(line)
    	for line in file:
    		br = 0
    		newLine = ""
    		rid = False
    		for j in range(len(line)):
    			c = line[j]
    			if(line[j] == '♪'):
    				rid = True
    			if(c == '（' or c == '(' or c == '<' or c == '['):
    				br += 1
    			elif(c == '）' or c == ')' or c == '>' or c == ']'):
    				br -= 1
    			elif(br == 0):
    				newLine += c
    			else:
    				newLine += ' '
    			if(br < 0):
    				newLine = ' '
    				br = 0

    		if(len(newLine) < 1 or newLine[-1] != '\n'):
    			newLine += '\n'

    		if(not rid):
    			Text += newLine

    		it += 1

    with codecs.open(currentOutFilePath, "w", "utf8") as file:
    	file.write(Text)


def CleanSRT(currentFile, currentOutFilePath):
    Text = ""
    with codecs.open(currentFile.path, "r", "utf8") as file1:
    	i = -1
    	music = False
    	it = 0
    	file = []
    	for line in file1:
    		file.append(line)
    	for line in file:
    		br = 0
    		newLine = ""
    		rid = False
    		for j in range(len(line)):
    			c = line[j]
    			if(line[j] == '♪'):
    				rid = True
    			if(c == '（' or c == '(' or c == '<' or c == '['):
    				br += 1
    				newLine += ' '
    			elif(c == '）' or c == ')' or (c == '>' and br > 0) or c == ']'):
    				br -= 1
    				newLine += ' '
    			elif(br == 0):
    				newLine += c
    			else:
    				newLine += ' '
    			if(br < 0):
    				newLine = ' '
    				br = 0


    		if(rid):
    			newLine = '♪'
    		if(len(newLine) < 1 or newLine[-1] != '\n'):
    			newLine += '\n'

    		Text += newLine

    		it += 1
    with codecs.open(currentOutFilePath, "w", "utf8") as file:
    	file.write(Text)


def SaveColoredHTML(currentOutFilePath, coloredText):
    with codecs.open("base.html", "r", "utf8") as base:
        with codecs.open(currentOutFilePath, "w", "utf8") as file:
            for line in base:
                file.write(str(line))
            for i in coloredText:
                file.write(str(i))
                if('\n' in i):
                    file.write("</br>")



def OpenGHD(GitHubFilePath):
    GitHubData = MText(GitHubFilePath)
    with codecs.open(GitHubFilePath, "r", "utf8") as file:
        for line in file:
            while(len(line) > 0 and (line[-1] == " " or line[-1] == "\n" or line[-1] == "\r")):
                line = line[:-1]
            line = line.split(' ')
            #if(len(line) < 2):
            #    allWords[0] = line[0]
            #    continue
            line[0] = line[0][0].upper() + line[0][1:]
            word = MWord(line[0], True)
            word.times_encountered += int(line[1]) # otherwise = 1
            GitHubData.words.append(word)
            GitHubData.amount_of_words += int(line[1]) # otherwise = 1
    return GitHubData

def OpenText(path):
    TextData = MText(path)
    with codecs.open(path, "r", "utf8") as file:

        lastWords = []
        for line in file:
            lastSentence = 0
            unknown_case = True
            if(len(line) < 4):
                #coloredText.append(line)
                continue
            c = 0
            firstWC = 0
            FNonWC = 0

            while(c < len(line)):
                if(line[c] in chars):
                    if(c == 0 or (c > 0 and line[c - 1] not in chars)):
                        firstWC = c
                        #coloredText.append(line[FNonWC:c])
                    if(c == len(line) - 1):
                        word = MWord(line[firstWC:], unknown_case)
                        if(word.word in lastWords):
                            TextData.words.append(word)
                        else:
                            lastWords.append(word.word)
                            if(len(lastWords) > 20):
                                lastWords = lastWords[1:]
                            word.times_encountered += 1
                            TextData.words.append(word)
                            TextData.amount_of_words += 1
                        #word = ColorWord(word, dict, seenRequired, learningRequired, knowRequired)
                        #for i in word:
                        #    coloredText.append(i)
                        unknown_case = False
                else:
                    if(c != 0 and line[c - 1] in chars):
                        FNonWC = c
                        word = MWord(line[firstWC:c], unknown_case)
                        if(word.word in lastWords):
                            TextData.words.append(word)
                        else:
                            lastWords.append(word.word)
                            if(len(lastWords) > 20):
                                lastWords = lastWords[1:]
                            word.times_encountered += 1
                            TextData.words.append(word)
                            TextData.amount_of_words += 1
                        #word = ColorWord(word, dict, seenRequired, learningRequired, knowRequired)
                        #for i in word:
                        #    coloredText.append(i)
                        unknown_case = False
                    if(line[c] in nextSent or c == 0):
                        unknown_case = True
                    #if(c == len(line) - 1):
                    #    coloredText.append(line[FNonWC:])
                c += 1

    return TextData

def changeNummbers(AIm, BIm, currentUserInfo):
    with codecs.open(currentUserInfo, "w", "utf8") as file:
        file.write(str(AIm)+' '+str(BIm)+"\n")


def openLog(LogPath):
    with codecs.open(LogPath, "r", "utf8") as file:
        for line in file:
            while(len(line) > 0 and (line[-1] == " " or line[-1] == "\n" or line[-1] == "\r")):
                line = line[:-1]
            line = line.split(' ')
            #print(line)
            return line


def OpenDict(DictPath):
    DictData = MText(DictPath)
    with codecs.open(DictPath, "r", "utf8") as file:
        it1 = 0
        for line in file:
            while(len(line) > 0 and (line[-1] == " " or line[-1] == "\n" or line[-1] == "\r")):
                line = line[:-1]
            line = line.split('\t')
            if(len(line) < 2):
                #print(line[0])
                DictData.amount_of_words = line[0]
                continue
            #line[0] = line[0][0].upper() + line[0][1:]
            word = MWord(line[1].split('|')[0], False)
            word.lemmas = line[1].split('|')
            word.times_encountered = int(line[0]) # otherwise = 1
            word.frequency_group = int(line[2])
            word.frequency_rank = int(line[3])
            word.frequency = float(line[4])
            word.c_frequency = float(line[5])
            word.times_have_enc = int(line[6])
            word.status = line[7]
            word.importance = 3
            if(it1 < AIm):
                word.importance = 1
            elif(it1 < BIm):
                word.importance = 2
            it1 += 1
            DictData.words.append(word)
            #DictData.amount_of_words += int(line[0]) # otherwise = 1
    return DictData


GitHubFilePath = "Stats/GitHubData.txt"


#hiperFilePath = ''
#hiperDictPath = ''

currentWord = ''
currentFile = ''
#currentInFilePath = 'Texts/Movies/LegoMovie/TheLegoMovie.srt'
#currentInFilePath = 'Texts/Movies/IsleOfDogs/Ataris.Reise.srt'
#currentInFilePath = 'Texts/Movies/WhoAmI/WhoAmI.srt'
#currentInFilePath = 'Texts/Movies/Zootopia/Zootopia.srt'
currentInFilePath = 'textFile.txt'
currentInFilePathSrt = 'subtitles.srt'
#currentInFilePath = 'Reading.txt'
#currentInFilePath = 'Texts/Series/HowToSell/6/HowtoSell.srt'
#currentInFilePath = 'Texts/Series/BabylonBerlin/4/BabylonBerlin.srt'
#currentInFilePath = 'Texts/Series/Dark/Season2/8/dark.srt'
#currentInFilePath = 'Texts/Series/CriminalGermany/1/CriminalGermany.srt'
#currentInFilePath = 'LastRead.txt'
#currentInFilePath = 'Stats/known1.txt'
#currentOutColoredFilePath = 'Texts/Series/HowToSell/6/HowtoSellColored.srt'
#currentOutColoredFilePath = 'Texts/Series/Dark/Season2/8/DarkColored.srt'
#currentOutColoredFilePath = 'Texts/Movies/IsleOfDogs/Ataris.ReiseColored.srt'
currentOutColoredFilePath = 'subtitlesColored.srt'
#currentOutColoredFilePath = 'Texts/Movies/Zootopia/ZootopiaColored.srt'
#currentOutColoredFilePath = 'Texts/Series/CriminalGermany/1/CriminalGermanyColored.srt'
currentOutHTMLColoredFilePath = 'Colored.HTML'
#currentOutFilePath = 'Texts/Movies/LegoMovie/TheLegoMovieInfo.txt'
currentOutFilePath = 'yourStats.txt'
#currentDictPath = "StatsToUse/DictToUse.txt"
currentDictPath = "users/1/DictToUse.txt"
currentUserInfo = "users/1/log.txt"
defaultDictPath = "Dictionaries/DictDefault.txt"
#currentDictPath = "StatsToUse/BackUp/DictToUse-2019-10-9-10-18pm.txt"
processed = False
array1 = openLog(currentUserInfo)
AIm = array1[0]
BIm = array1[1]
AIm = int(AIm)
BIm = int(BIm)
print("very important words:", AIm, "not that important but still:", BIm)

currentHipperDict = OpenDict(currentDictPath)

statsRes = currentHipperDict.CurrentKnowledge(1, 4, 10)
#for i in statsRes:
#    print(i)
print()
print("you know", statsRes[4][0], "words, which is", statsRes[4][1], "%")
print("you are learning", statsRes[5][0], "words, which is", statsRes[5][1], "%")
print("you have seen", statsRes[6][0], " more words, which is", statsRes[6][1], "%")
print("you don't know", statsRes[7][0], "words, which is", statsRes[7][1], "%")
print("all unimportant words are", statsRes[8][1], "%")

print()
#for i in currentHipperDict.words[:10]:
#    print(i.OutputInfo())

for i in range(1000):
    if(not processed):
        print('if you want to change the numbers or important words, type "/changeNumbers"')
        print('if you want to upload subtitles, save the file "subtitles.srt" and type "/processSubtitles"')
        print('if you want to upload text, save it "textFile.srt" and type "/processText"')
    line = input()
    print()
    while(len(line) > 0 and (line[-1] == " " or line[-1] == "\n" or line[-1] == "\r")):
        line = line[:-1]
    if(line == "/openDict"):
        currentHipperDict = OpenDict(currentDictPath)
        for i in currentHipperDict.words[:10]:
            print(i.OutputInfo())
    elif(line == "/saveDict"):
        currentHipperDict.saveDictionary(currentDictPath)
        for i in currentHipperDict.words[:10]:
            print(i.OutputInfo())
    elif(line == "/changeNumbers"):
        print("how many words are important right now?")
        print("I recommend you multiply the amount of words you know by 2")
        AIm = input()
        while(len(AIm) > 0 and (AIm[-1] == " " or AIm[-1] == "\n" or AIm[-1] == "\r")):
            AIm = AIm[:-1]
        AIm = int(AIm)
        print("how many words are less important but you should still look them up?")
        print("I recommend you multiply the amount of words you know by 3")
        BIm = input()
        while(len(BIm) > 0 and (BIm[-1] == " " or BIm[-1] == "\n" or BIm[-1] == "\r")):
            BIm = BIm[:-1]
        BIm = int(BIm)

        changeNummbers(AIm, BIm, currentUserInfo)
        currentHipperDict = OpenDict(currentDictPath)
        print("The numbers have been changed")
    elif(line == "/openGHD"):
        GHD = OpenGHD(GitHubFilePath)
        GHD.ProcessTextWords()
        currentHipperDict = GHD
        wordList = GHD.words
        for word in wordList:
            print(word.word, word.times_encountered)
    elif(line[:4] == "/sw/"):
        currentHipperDict.changeWordStatus(currentWord, line[4:])
    elif(line[:17] == "/markWordsInText/"):
        for word in currentFile.words:
            currentHipperDict.changeWordStatus(word, line[17:])
    elif(line == "/stats"):
        statsRes = currentHipperDict.CurrentKnowledge(1, 4, 10)
        for i in statsRes:
            print(i)

    elif(line == "/processSubtitles"):
        #textToP = ProcessText(line[4:], "NO")
        currentInFilePathSrt = currentInFilePathSrt
        CleanSRT(OpenText(currentInFilePathSrt), currentInFilePathSrt[:-4]+"Clean.srt")
        currentFile = OpenText(currentInFilePathSrt[:-4]+"Clean.srt")
        #for i in currentFile.words[:10]:
        #    print(i.word, i.times_encountered)
        currentFile.ProcessTextWords()
        #for i in currentFile.words[:10]:
        #    print(i.OutputInfo())
        #print()
        currentFile.AddDictInfo(currentHipperDict)
        #for i in currentFile.words[:10]:
        #    print(i.OutputInfo())
        statsRes = currentFile.CurrentKnowledge(1, 4, 10)
        print("in these subtitles:")
        print("you know", statsRes[4][0], "words, which is", statsRes[4][1], "%")
        print("you are learning", statsRes[5][0], "words, which is", statsRes[5][1], "%")
        print("you have seen", statsRes[6][0], "words, which is", statsRes[6][1], "%")
        print("you don't know", statsRes[7][0], "words, which is", statsRes[7][1], "%")
        print(statsRes[8][0], "words are not important, which is", statsRes[8][1], "%")
        coloredText = currentFile.ColorSTRWE(currentOutColoredFilePath, 1, 4, 10)
        SaveColoredSTR(currentOutColoredFilePath, coloredText)

        currentFile = OpenText(currentInFilePathSrt[:-4]+"Clean.srt")
        currentFile.ProcessTextWords()
        currentFile.AddDictInfo(currentHipperDict)

        processed = True
        print()
        print('saved in "subtitlesColored.srt", you can now open it!')
        print('after watching please type "/saveProgress", so that I can save your progress!!!')
        print()
    elif(line == "/processText"):
        #textToP = ProcessText(line[4:], "NO")
        currentFile = OpenText(currentInFilePath)
        #for i in currentFile.words[:10]:
        #    print(i.word, i.times_encountered)
        currentFile.ProcessTextWords()
        #for i in currentFile.words[:10]:
        #    print(i.OutputInfo())
        #print()
        currentFile.AddDictInfo(currentHipperDict)
        #for i in currentFile.words[:10]:
        #    print(i.OutputInfo())
        statsRes = currentFile.CurrentKnowledge(1, 4, 10)

        print("in these text:")
        print("you know", statsRes[4][0], "words, which is", statsRes[4][1], "%")
        print("you are learning", statsRes[5][0], "words, which is", statsRes[5][1], "%")
        print("you have seen", statsRes[6][0], "words, which is", statsRes[6][1], "%")
        print("you don't know", statsRes[7][0], "words, which is", statsRes[7][1], "%")
        print(statsRes[8][0], "words are not important, which is", statsRes[8][1], "%")

        coloredText = currentFile.ColorSTRWE(currentOutHTMLColoredFilePath, 1, 4, 10)
        SaveColoredHTML(currentOutHTMLColoredFilePath, coloredText)

        currentFile = OpenText(currentInFilePath)
        currentFile.ProcessTextWords()
        currentFile.AddDictInfo(currentHipperDict)
        processed = True
        print()
        print('saved in "Colored.html", you can now open it!')
        print('after reading please type "/saveProgress", so that I can save your progress!!!')
        print()
    #elif(line == "/addEncountered"):
    #    currentHipperDict.AddEncountered(currentFile)
    elif(line == "/clean"):
        Clean(currentFile, currentOutFilePath[:-4]+"Clean.txt")
    elif(line[:11] == "/saveTextR/"): #"/saveTextR/klsuKLSUN"
        outputPath = currentOutFilePath
        currentFile.SaveTextRes(currentOutFilePath, line[11:], 1, 4, 10)

        #resList = GetRidOfNF(textToP)
        #saveTextRes(outputPath[:-4]+"-NoNF.txt", textToP, line[11:], dict[1], 1, 4, 10)
    elif(line[:11] == "/saveDictR/"): #"/saveTextR/klsuKLSUN"
        outputPath = currentOutFilePath
        currentHipperDict.SaveTextRes(currentOutFilePath, line[11:], 1, 4, 10)

        #resList = GetRidOfNF(textToP)
        #saveTextRes(outputPath[:-4]+"-NoNF.txt", textToP, line[11:], dict[1], 1, 4, 10)
    elif(line[:11] == "/EncoDictR/"): #"/saveTextR/klsuKLSUN"
        outputPath = currentOutFilePath
        currentHipperDict.SaveTextResByEncount(currentOutFilePath, line[11:], 1, 4, 10)

    elif(line[:11] == "/EncTTextR/"): #"/saveTextR/klsuKLSUN"
        outputPath = currentOutFilePath
        resTE = currentFile.EncTTextRes(line[11:], 1, 4, 10)
        print(resTE)
    elif(line[:11] == "/EncTDictR/"): #"/saveTextR/klsuKLSUN"
        outputPath = currentOutFilePath
        resTE = currentHipperDict.EncTTextRes(line[11:], 1, 4, 10)
        print(resTE)
        #resList = GetRidOfNF(textToP)
        #saveTextRes(outputPath[:-4]+"-NoNF.txt", textToP, line[11:], dict[1], 1, 4, 10)
    elif(line[:11] == "/WlEnTextR/"): #"/saveTextR/klsuKLSUN"
        outputPath = currentOutFilePath
        resTE = currentFile.wilEncounterTextRes(line[11:], 1, 4, 10)
        print(resTE)
    elif(line == "/checkText"):
        statsRes = currentFile.CheckText(1, 4, 10)

        for i in statsRes:
            print(i)
    elif(line == "/color"):
        print("ok")
        coloredText = currentFile.ColorSTR(currentOutColoredFilePath, 1, 4, 10)
        SaveColoredSTR(currentOutFilePath, coloredText)

    elif(line == "/zeroEncounters"):
        currentHipperDict.ZeroEncounters()
    elif(line == "/saveProgress"):
        currentHipperDict.AddEncounteredIgnoringRare(currentFile)
        currentHipperDict.saveDictionary(currentDictPath)
        print("now you can close the app")
        #for i in currentHipperDict.words[:10]:
        #    print(i.OutputInfo())

    elif(line[:12] == "/outputDict/"):
        print("ok")
        coloredText = currentFile.ColorSTR(currentOutColoredFilePath, 1, 4, 10)
        SaveColoredSTR(currentOutFilePath, coloredText)
    elif(line == "/colorHTML"):
        print("ok")
        coloredText = currentFile.ColorSTR(currentOutHTMLColoredFilePath, 1, 4, 10)
        SaveColoredHTML(currentOutHTMLColoredFilePath, coloredText)
        #SaveColoredSTR(outfilePath, coloredText)
    elif(line == "/colorWE"):
        print("ok")
        coloredText = currentFile.ColorSTRWE(currentOutColoredFilePath, 1, 4, 10)
        SaveColoredSTR(currentOutColoredFilePath, coloredText)
    elif(line == "/colorHTMLWE"):
        print("ok")
        coloredText = currentFile.ColorSTRWE(currentOutHTMLColoredFilePath, 1, 4, 10)
        SaveColoredHTML(currentOutHTMLColoredFilePath, coloredText)
        #SaveColoredSTR(outfilePath, coloredText)
    elif(line == "/colorWEAK"):
        print("ok")
        coloredText = currentFile.ColorSTRWEAK(currentOutColoredFilePath[:-4]+"WK.srt", 1, 4, 10)
        SaveColoredSTR(currentOutColoredFilePath[:-4]+"WK.srt", coloredText)

    elif(line == "/colorWEAKNS"):
        print("ok")
        coloredText = currentFile.ColorSTRWEAKNS(currentOutColoredFilePath[:-4]+"WKNS.srt", 1, 4, 10)
        SaveColoredSTR(currentOutColoredFilePath[:-4]+"WKNS.srt", coloredText)
    else:
        print("unknown command")
        #currentWord = MWord(line, False)
        #s = currentWord.analyze_word()
        #for i in s:
        #    print(i)
        #print("settled:")
        #print(currentWord.OutputInfo())
