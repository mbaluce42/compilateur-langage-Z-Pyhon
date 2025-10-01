###############################################################################
#       Réalisation d’un compilateur pour le langage Z en Python              #
#                            de                                               #
#                     MBAYA Luce-Emmanuel                                     #
#                         GROUPE 2125                                         #
#                                                                             #
#      !!!!! POUR FAIRE UN NOMBRE NEGATIF (NEG) utiliser l'op "_" !!!!!       #
#                                                                             #
#                                                                             #
###############################################################################

nbrPrint=0# si nbrprint =1 c qu'il y a une instr 'print' ca va permettre de cree l'entete print
nbrInput=0# si nbrprint=1 c qu'il y a une instr 'input' ca va me permettre de cree l'entete input
varList= []# liste de toute les variables parcourue dans le prog sans doublon
# va me permette de faire la declaration des variable et du type
varCible="" #la ou une variable est stocké
res="" # garde la variable analyser avant '='(variable du resultat du calcul)



def Prog():
    SymboleSuivant(0)
    if SymboleCourant(6) == "start>":
        SymboleSuivant(6)
        codeCible.append("void main()")
        codeCible.append("{")
        codeCible.append("\t_asm")
        codeCible.append("\t{")
        SuiteInstr()

        for i in range(0,(len(varList))):
            if varList[i][0] == 'i':
                codeCible.insert(0, "int " + varList[i] + ";" + "")
            elif varList[i][0] == 's':
                codeCible.insert(0, "short " + varList[i] + ";" + "")
            elif varList[i][0] == 'b':
                codeCible.insert(0, "char " + varList[i] + ";" + "")

        if nbrInput>=1:
            codeCible.insert(0, "int varSaisie;")
            codeCible.insert(0, 'const char msgEntrez[] = "Entrez une valeur : ";')
            codeCible.insert(0, 'const char msgSaisie[] = " %d";')

        if nbrPrint>=1:
            codeCible.insert(0, 'const char msgAffichage[] = "Valeur = %d\\n";')
            codeCible.insert(0, "#include <stdio.h>")

        if SymboleCourant(5) == "<stop":
            SymboleSuivant(5)
            if varList==[]:
                codeCible.append("\t\tpop eax")
            codeCible.append("\t}")
            codeCible.append("}")

            return True
        else:
            return False
    else:
        return False

# ----------------------------------------

def SuiteInstr():
    Instr()
    while SymboleCourant(1) == ';':
        SymboleSuivant(1)
        Instr()
# ----------------------------------------
def Instr():

    if Reg32() == True:
        regCible = SymboleCourant(3)
        SymboleSuivant(3)
        if SymboleCourant(1) == '=':
            SymboleSuivant(1)
            OR()
            codeCible.append("\t\tpop " + regCible)

    if Print()== True:
        #global InOutStock
        if SymboleCourant(5)=="print":
            global nbrPrint
            nbrPrint=1
            #InOutStock=SymboleCourant(5)
            SymboleSuivant(5)
            OR()
            codeCible.append("\t\tpush offset msgAffichage")
            codeCible.append("\t\tcall dword ptr printf")
            codeCible.append("\t\tadd esp, 8")

        elif SymboleCourant(5)=="input":
            global nbrInput
            nbrInput=1
            #InOutStock=SymboleCourant(5)
            #SymboleSuivant(5)
            codeCible.append("\t\tpush offset msgEntrez")
            codeCible.append("\t\tcall dword ptr printf")
            codeCible.append("\t\tadd esp, 4")
            codeCible.append("\t\tpush offset varSaisie")
            codeCible.append("\t\tpush offset msgSaisie")
            codeCible.append("\t\tcall dword ptr scanf")
            codeCible.append("\t\tadd esp, 8")
            codeCible.append("\t\tpush varSaisie")
            codeCible.append("\t\tpop eax")
            SymboleSuivant(5)
            if var()==True:
                if varCible[0:1] == "i":
                    codeCible.append("\t\tmov " + varCible  + ", eax")
                elif varCible[0:1] == "s":
                    codeCible.append("\t\tmov " + varCible  + ", ax")
                elif varCible[0:1] == "b":
                    codeCible.append("\t\tmov " + varCible  + ", al")

    if var() == True :
         if SymboleCourant(1) == '=':
            global res
            res=varCible

            SymboleSuivant(1)
            OR()
            if res[0:1] == "i":
                codeCible.append("\t\tpop "+res)

            elif res[0:1] == "s":
                codeCible.append("\t\tpop eax")
                codeCible.append("\t\tmov " + res + ", ax")

            elif res[0:1] == "b":
                codeCible.append("\t\tpop eax")
                codeCible.append("\t\tmov " + res + ", al")


    else:
        OR()

# ----------------------------------------
def OR():
    AND()
    while SymboleCourant(1) in '|':
        if SymboleCourant(1) == '|':
            SymboleSuivant(1)
            AND()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tor eax, ebx")
            codeCible.append("\t\tpush eax")

# ----------------------------------------

def AND():
    ExprPM()
    while SymboleCourant(1) in '&':
        if SymboleCourant(1) == '&':
            SymboleSuivant(1)
            ExprPM()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tand eax, ebx")
            codeCible.append("\t\tpush eax")

#----------------------------------------------

def ExprPM():
    ExprFDM()
    while SymboleCourant(1) in "+-":
        if SymboleCourant(1) == '+':
            SymboleSuivant(1)
            ExprFDM()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tadd eax, ebx")
            codeCible.append("\t\tpush eax")
        elif SymboleCourant(1) == '-':
            SymboleSuivant(1)
            ExprFDM()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tsub eax, ebx")
            codeCible.append("\t\tpush eax")

# ----------------------------------------

def ExprFDM():
    Neg_Not()
    while SymboleCourant(1) in "*/%":
        if SymboleCourant(1) == '*':
            SymboleSuivant(1)
            Neg_Not()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\timul eax, ebx")
            codeCible.append("\t\tpush eax")
        elif SymboleCourant(1) == '/':
            SymboleSuivant(1)
            Neg_Not()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tcdq")
            codeCible.append("\t\tidiv ebx")
            codeCible.append("\t\tpush eax")
        elif SymboleCourant(1) == '%':
            SymboleSuivant(1)
            Neg_Not()
            codeCible.append("\t\tpop ebx")
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tcdq")
            codeCible.append("\t\tidiv ebx")
            codeCible.append("\t\tpush edx")# car dans le modulo le reste est stocke dans le registre edx

# ----------------------------------------

def Neg_Not():
    Facteur()
    while SymboleCourant(1) in "_~":
        if SymboleCourant(1) == '_':
            SymboleSuivant(1)
            Facteur()
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tneg eax")
            codeCible.append("\t\tpush eax")
        elif SymboleCourant(1) == '~':
            SymboleSuivant(1)
            Facteur()
            codeCible.append("\t\tpop eax")
            codeCible.append("\t\tnot eax")
            codeCible.append("\t\tpush eax")


# ----------------------------------------

def Facteur():

    #varCible = SymboleCourant(4)
    if SymboleCourant(1) == '(':
        SymboleSuivant(1)
        SuiteInstr()
        if SymboleCourant(1) == ')':
            SymboleSuivant(1)
    elif Reg32() == True:
        codeCible.append("\t\tpush " + SymboleCourant(3))
        SymboleSuivant(3)

    elif var() == True:

        if varCible[0] == 'i':
            codeCible.append("\t\tpush " + varCible)

        elif varCible[0] == 's':
            codeCible.append("\t\tmovsx eax, " + varCible)
            codeCible.append("\t\tpush eax")

        elif varCible[0] == 'b':
            codeCible.append("\t\tmovsx eax, " + varCible)
            codeCible.append("\t\tpush eax")

    else:
        Nombre_X()


#------------------------------------------
def Nombre_X():
    Nombre_Hexa()
    Nombre_Binaire()
    Nombre_Decimal()
# ----------------------------------------

def Nombre_Hexa():
    if SymboleCourant(2) == "0x":
        if chiffreHexa() == True:
            nb = SymboleCourant(1)
            SymboleSuivant(1)
            while chiffreHexa() == True:
                nb = nb + SymboleCourant(1)
                SymboleSuivant(1)
            nb = int(nb, 16)
            codeCible.append("\t\tpush dword ptr " + str(nb))


# ----------------------------------------------------------------------------
def Nombre_Binaire():
    if SymboleCourant(2) == "0b":
        if chiffreBinaire() == True:
            nb = SymboleCourant(1)
            SymboleSuivant(1)
            while chiffreBinaire() == True:
                nb = nb + SymboleCourant(1)
                SymboleSuivant(1)
            nb = int(nb, 2)
            codeCible.append("\t\tpush dword ptr " + str(nb))

#---------------------------------------------------------------------
def Nombre_Decimal():
    if ChiffreDecimal() == True:
        nb = ord(SymboleCourant(1)) - 0x30
        SymboleSuivant(1)
        while ChiffreDecimal() == True:
            nb = nb * 10 + ord(SymboleCourant(1)) - 0x30
            SymboleSuivant(1)
        codeCible.append("\t\tpush dword ptr " + str(nb))

#-----------------------------------------------------------------------------
def ChiffreDecimal():
    if SymboleCourant(1) in "0123456789":
        return True
    else:
        return False

# ----------------------------------------

def chiffreHexa():
    if SymboleCourant(1) in "0123456789abcdefx":
        return True
    else:
        return False

# ----------------------------------------


def chiffreBinaire():
    if SymboleCourant(1) in "01b":
        return True
    else:
        return False

# ----------------------------------------
def var():
    global varCible
    if SymboleCourant(1) in "isb":
        varCible = SymboleCourant(1)
        SymboleSuivant(1)
        mot()
        return True
    return False
# ----------------------------------------
def mot():
    global varList
    global varCible
    if lettre() == True:
        varCible = varCible + SymboleCourant(1)

        SymboleSuivant(1)
        while lettre() == True:
            varCible = varCible + SymboleCourant(1)
            SymboleSuivant(1)
        varList.append(varCible)
        varList=list(set(varList)) #set permetre conv  liste en  ensemble(supp les doublon) puis list conv en liste

# ----------------------------------------
def lettre():
    if SymboleCourant(1) in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTIVWXYZ":
        return True
    else:
        return False

# ----------------------------------------
def Print():
    if SymboleCourant(5) in ["print", "input"]:
        return True
    else:
        return False

# ----------------------------------------

def Reg32():
    if SymboleCourant(3) in ["eax", "ebx", "ecx", "edx", "esi", "edi"]:
        return True

    else:
        return False

# ----------------------------------------
def SymboleCourant(n):
    return programme[posCourante:posCourante + n]

# ----------------------------------------

def SymboleSuivant(n):
    global posCourante
    posCourante = posCourante + n
    while posCourante < len(programme) and programme[posCourante] == ' ':
        posCourante = posCourante + 1

# ----------------------------------------

programme = ("start>"
        
             #C CARRE
             #"512 * 17 % 3 + 7 "
             
             
             #C CARRE
             #"0b101 + 0xf0 * 3"
             
             
             #C CARRE
             #"512 * (144 + 0b11) | 0x12 - 541 & 0xff"
             
             #C CARRE
             #"iVar = _(_(144 + 0b11) + ~0xff)"
             
             
             #C CARRE
              #"sVal = 0b110010 | 9008 / (2 * 0xf)"
             
             
             #C CARRE
             #"sVar = (2 + 33) * 5;"
             #"bVal = 8 / 2 * 0xf0;"
             #"sVar = 0b110 + bVal"
             
             
             #C CARRE
             #"bVar = 3; "
             #"sVar = 2 + bVar;"
             #"iNb = 0b110 * sVar;"
             #"iNb = iNb + 1"
             
             
             #C CARRE
             #"sNombre = 45;"
             #"print sNombre + 2;"
             #"print _sNombre * 0b10"
             
             
             #c carre
             "input sNombre;" 
             "input bNb;"
             "print sNombre * _bNb"
             
             "<stop")
codeCible = []
posCourante = 0

if Prog() == True:
    for c in codeCible:
        print(c)
    print("\nCompilation terminée avec succès!")
else:
    print("Erreur de compilation : le caractere", SymboleCourant(1),
          "à la " + str(posCourante + 1) + "e position est invalide!")
