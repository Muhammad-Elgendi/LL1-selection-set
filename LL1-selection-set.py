grammerFile = open("Grammer.txt","r")
grammer =grammerFile.read().splitlines()
print("Here is your grammer : ",grammer)
nullableForSure = [rule[0] for rule in grammer if rule.endswith("→ϵ")]

# print(nullableForSure)
# tempGrammerFile = open("tempGrammer.txt","w+")
# tempGrammerFile.write('\n'.join(grammer))

# for nonTerminal in nullableForSure:
#     fileStr = tempGrammerFile.read()
#     tempGrammerFile.write(fileStr.replace(nonTerminal,"ϵ"))
#     tempGrammerFile.flush()

print("-"*40)
# --------------------------------------------------
# step 1 Nullable non terminal & Rule number
# --------------------------------------------------
for index , rule in enumerate(grammer):
    # rightHandSide = rule.split("→")[1]
    # print(rightHandSide)

    # step 1 Nullable non terminal & Rule number
    string = ""
  
    for char in rule.split("→")[1]:
        if char in nullableForSure or char == "ϵ":
            string+= char

    if rule.split("→")[1] == string:
        print("Step 1:","Nullable non terminal",rule.split("→")[0],"Rule",index+1)
print("-"*40)

# -----------------------------
# step 2 Begins directly with
# -----------------------------
BDW = []
for index ,rule in enumerate(grammer):
     
    indexOfRHS = rule.index(rule.split("→")[1][0])
    if rule[indexOfRHS] != "ϵ":
        print("Step 2:",rule.split("→")[0],"Begins directly with",rule[indexOfRHS])
        BDW.append([rule.split("→")[0],rule[indexOfRHS]])
        indexOfNonNullable = rule.index(rule.split("→")[1][0])
        for char in rule.split("→")[1]:
            if char in nullableForSure or char == "ϵ":
                indexOfNonNullable+=1
            else :
                break        

        if indexOfRHS != indexOfNonNullable:
            for i in range(indexOfRHS,indexOfNonNullable,1):
                print("Step 2:",rule.split("→")[0],"Begins directly with",rule[i+1])
                BDW.append([rule.split("→")[0],rule[i+1]])

# print(BDW)
print("-"*40)

# --------------------
# step 3 Begins with
# --------------------
BW =[]
# (from BDW)
BW.extend(BDW)
# (transitive)
for i in BDW:
    for j in BDW:
        if i[1] == j[0]:
            BW.append([i[0],j[1]])
# reflexive
symbols = set(j for i in BDW for j in i)
BW.extend([[symbol,symbol] for symbol in symbols ])
for relation in BW:
    print("Step 3:",relation[0],"Begins with",relation[1])
print("-"*40)

# --------------------
# step 4 First(x)
# --------------------
first = {}
for index , symbol in enumerate(symbols):
    first[symbol]= set()
    if symbol.isupper():
        for relation in BW:
            if relation[0] == symbol and relation[1].islower():
                first[symbol].add(relation[1])
    elif symbol.islower():
        first[symbol].add(symbol)

for symbol , setOfSymbols in first.items():
    print("Step 4:","First(",symbol,"):",setOfSymbols)
print("-"*40)

# ----------------------------------------
# step 5 First of right side of each rule
# ----------------------------------------
firstOfRHS = {}
for index ,rule in enumerate(grammer):    
    firstOfRHS[rule.split("→")[1]] = set()
    indexOfRHS = rule.index(rule.split("→")[1][0])
    if rule[indexOfRHS] != "ϵ":
        indexOfNonNullable = rule.index(rule.split("→")[1][0])
        for char in rule.split("→")[1]:
            if char in nullableForSure or char == "ϵ":
                indexOfNonNullable+=1
            else :
                break 
        if indexOfRHS != indexOfNonNullable:
            firstOfRHS[rule.split("→")[1]] = firstOfRHS[rule.split("→")[1]].union(first[rule[indexOfRHS]])
            for i in range(indexOfRHS,indexOfNonNullable,1):
                firstOfRHS[rule.split("→")[1]] = firstOfRHS[rule.split("→")[1]].union(first[rule[i+1]])
        else:
            firstOfRHS[rule.split("→")[1]] = firstOfRHS[rule.split("→")[1]].union(first[rule[indexOfRHS]])

for symbol , setOfSymbols in firstOfRHS.items():
    print("Step 5:","First(",symbol,"):",setOfSymbols)
print("-"*40)

# ----------------------------------------------------
# step 6 Compute the relation Is Followed Directly By
# ----------------------------------------------------
FDB = []
for rule in grammer:
    RHS = rule.split("→")[1]
    for index , char in enumerate(RHS):
        if char.isupper() and index+1 <= len(RHS)-1:
            FDB.insert(index , [char , RHS[index+1]] )
            if RHS[index+1] in nullableForSure and index+2 <= len(RHS)-1:
                FDB.insert(index , [char , RHS[index+2]] )         

for relation in FDB:
    print("Step 6:",relation[0],"Is Followed Directly By",relation[1])
print("-"*40)

# ----------------------------------------------
# step 7  Compute the relation Is Direct End Of
# ----------------------------------------------
DEO = []
for index , rule in enumerate(grammer):   
    RHS = rule.split("→")[1][::-1]
    if RHS[0] != "ϵ":       
        DEO.insert(index,[ RHS[0] , rule.split("→")[0] ])
        if RHS[0] in nullableForSure:
            DEO.insert(index, [ RHS[1] , rule.split("→")[0] ])

for relation in DEO:
    print("Step 7:",relation[0],"Is Direct End Of",relation[1])

print("-"*40)

# ---------------------------------------
# step 8  Compute the relation Is End Of
# ---------------------------------------

EO =[]
# (from DEO)
EO.extend(DEO)
# (transitive)
for i in DEO:
    for j in DEO:
        if i[1] == j[0]:
            EO.append([i[0],j[1]])
# reflexive
symbols = set(j for i in BDW for j in i)
EO.extend([[symbol,symbol] for symbol in symbols ])
EO =  [list(x) for x in set(tuple(x) for x in EO)]
for relation in EO:
    print("Step 8:",relation[0],"Is End Of",relation[1])

print("-"*40)

# -------------------------------------------
# Step 9 Compute the relation Is Followed By
# -------------------------------------------
# EO | FDB | BW
FB =[]
for E in EO:
    for F in FDB:
        for B in BW:
            if E[1] == F[0] and F[1] == B[0]:
                FB.append([E[0],B[1]])
for relation in FB:
    print("Step 9:",relation[0],"Is Followed By",relation[1])

print("-"*40)

# ----------------------------------------------------
# Step 10 Extend the FB relation to include endmarker 
# ----------------------------------------------------

EFB = [] # Extended Followed By
EFB.extend(FB)
for relation in EO:
    if relation[0].isupper() and relation[1] == "S":
        EFB.append([relation[0] , "←"])

for relation in EFB:
    print("Step 10:",relation[0],"Is Followed By",relation[1])
print("-"*40)