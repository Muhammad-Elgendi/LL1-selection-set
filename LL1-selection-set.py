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

# ----------------------------------------------------
# step 6 Compute the relation Is Followed Directly By
# ----------------------------------------------------
FDB = {}
for rule in grammer:
    RHS = rule.split("→")[1]
    for index , char in enumerate(RHS):
        if char.isupper() and index+1 <= len(RHS)-1:
            FDB[char] = [RHS[index+1]]
            if RHS[index+1] in nullableForSure and index+2 <= len(RHS)-1:
                FDB[char].append( RHS[index+2] )           

for symbol , setOfSymbols in FDB.items():
    for followed in setOfSymbols:
        print("Step 6:",symbol,"FDB",followed)

# ----------------------------------------------
# step 7  Compute the relation Is Direct End Of
# ----------------------------------------------

