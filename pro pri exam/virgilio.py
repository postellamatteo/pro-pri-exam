import os
import json

class Virgilio:
    def __init__(self,directory:str): #costr piglia percorso assoluto
        self.directory=directory

    class CantoNotFoundError(Exception): #eccezione personalizzata
        pass

    #ES 1 leggi canto x e restituisci tutte o n righe
    def read_canto_lines(self,canto_number,strip_lines:bool=False,num_lines:int=None): 
        # es 15, verifica se cantoN è int (grazie del suggerimento :D)
        if not isinstance(canto_number,int):
            raise TypeError("canto_number must be an integer")

        #es16 verifica se esiste il num canto cercato
        if canto_number<1 or canto_number>34: 
            return f"canto_number must be between 1 and 34."

        file_path=os.path.join(self.directory,f"Canto_{canto_number}.txt")
        lines=[] #creo array per lines
        try:
            with open(file_path,"r", encoding="utf-8") as f:
                if num_lines is not None:
                    for _ in range(num_lines): #legge solo n righe
                        line=f.readline()
                        if not line:
                            break
                        lines.append(line)
                else:
                    lines=f.readlines()#legge tutto
        except Exception:#es17,segnala errori in apertuta file
            return f"error while opening{file_path}"

        # es13 se strip_lines=True strippa le lines :D
        if strip_lines: 
            lines=[line.strip() for line in lines]
        
        return lines #lista righe o errore

    #es2 restituisce il num di versi nel canto n
    def count_verses(self,canto_number:int):
        lines=self.read_canto_lines(canto_number)
        if isinstance(lines,str):
            return 0
        return len(lines)

     #es3 conta terzine in canto n
    def count_tercets(self,canto_number:int):
        tutti=self.count_verses(canto_number)
        return tutti//3

    #es4 quante volte "word" nel canto x
    def count_word(self,canto_number:int,word:str): 
        lines=self.read_canto_lines(canto_number)
        if isinstance(lines, str):
            return 0
        canto_text="".join(lines)#grazie del secondo suggerimento :D
        return canto_text.count(word)
    

    #es5 primo verso che contiene word
    def get_verse_with_word(self,canto_number:int,word:str): 
        lines=self.read_canto_lines(canto_number)
        if isinstance(lines,str):
            return ""  # In caso di errore lettura file
        for verso in lines:
            if word in verso:
                return verso
        return ""

    #es6 tutti i versi del cant N con word 
    def get_verses_with_word(self,canto_number:int,word:str): 
        lines=self.read_canto_lines(canto_number)
        if isinstance(lines,str):
            return []

        trovati=[]
        for verso in lines:
            if word in verso:
                trovati.append(verso)
        return trovati

    #es7 verso più lungo del canto x
    def get_longest_verse(self,canto_number:int): 
        lines=self.read_canto_lines(canto_number,strip_lines=True)
        if isinstance(lines,str):
            return ""

        più_lungo=""
        lun_max=0
        for verso in lines:
            if len(verso)>lun_max:
                più_lungo=verso
                lun_max=len(verso)
        return più_lungo
    
    #es8 cerca canto più lungo
    def get_longest_canto(self): 
        num_più_lungo=None
        num_versi=0

        for i in range(1,35):
            if self.count_verses(i) > num_versi:
                num_più_lungo=i
                num_versi=self.count_verses(i)
        return{
            "canto_number": num_più_lungo,
            "canto_len": num_versi
            }

    #es9 conta ricorrenze parole in lista words
    def count_words(self, canto_number: int, words: list): 
        lines=self.read_canto_lines(canto_number)
        if isinstance(lines, str):
            return {}

        testo_canto="".join(lines)
        risultato={}
        for w in words:
            risultato[w]=testo_canto.count(w)

        output_path=os.path.join(self.directory, "word_counts.json")# es18 dizionario nel json  
        try:
            with open(output_path,"w",encoding="utf-8")as outfile:
                json.dump(risultato,outfile,ensure_ascii=False,indent=2)
        except Exception:
            pass #errore scrittura
        return risultato

    #es 10 restituisce tutti i versi di tutti i canti
    def get_hell_verses(self): 
        tutti=[]
        for i in range(1, 35):
            lines=self.read_canto_lines(i, strip_lines=True)
            if isinstance(lines, list):
                tutti.extend(lines)
        return tutti

    #es 11 conta i versi di tutti i canti
    def count_hell_verses(self): 
        tutti=0
        for i in range(1, 35):
            tutti+=self.count_verses(i)
        return tutti

    #es12 lunghezza media versi inferno  (strippati)
    def get_hell_verse_mean_len(self): 
        tutti=self.get_hell_verses()
        if not tutti:
            return 0.0
        
        strippati=[v.strip() for v in tutti]
        total_length=sum(len(v) for v in strippati)
        return total_length/len(strippati)


path_canti=r"/Users/postella/Documents/py1/pro pri exam/canti" #assoluto
v=Virgilio(path_canti)
x=100
#print(f"prime 5 righe del canto {x}:\n{v.read_canto_lines(x, strip_lines=True, num_lines=5)}\n") 
#print(f"num versi canto  {x}: {v.count_verses(x)}")
#print(f"num terzine canto  {x}: {v.count_tercets(x)}") #es3 conta terzine 
#print(f"num 'dante' canto  {x}: {v.count_word(x, "Dante")}")
#print(f"primo verso in cui appare 'dante' {v.get_verse_with_word(x, "Dante")}")
#print(f"verso più lungo canto {x}: {v.get_longest_verse(x)}")
#print(f"canto con più versi: {v.get_longest_canto()}")
#print(f"conteggio parole 'Dante' e 'amore' nel Canto {x}: {v.count_words(x, ["Dante", "amore"])}")
#print(f"primi 3 versi dell'Inferno:\n{v.get_hell_verses()[:3]}")#es10
#print(f"num versi inferno:{v.count_hell_verses()}") #es11
#print(f"lung media versi inferno:{v.get_hell_verse_mean_len()}") #es12 