from Parser import Parser
from collections import defaultdict

class engine:
    tmpText = """\
                e(1,2).
                e(2,3).
                e(3,5).
                p(X,Q) :-  e(X,Y) , e (Y,Z), e(Z,Q).""".splitlines()

    numberOfSubgoals = 0
    nofactsMatch = True
    parser = Parser(tmpText)
    parser.parse()
    rule = {}
    rules = parser.ruleList
    lenght = len(rules)
    i = 0
    while (i < lenght):
        rule = rules[i]
        i += 1

    #Taking the subgoals from rules
    for body in rule:
        for facts in parser.factList:
            ruleBodyLength = len(rule["rule"]["body"])
            w = 0
            subGoals = []
    while (w < ruleBodyLength):
        subGoals.append(rule["rule"]["body"][w])
        numberOfSubgoals += 1;
        w += 1

     #All the subgoals
    # for items in subGoals:
    #     print(items["identifier"])

    substitutied = {}
    factArguements = {}
    ruleArugements = {}
    for subgoal in subGoals:
        if (nofactsMatch):
            for facts in parser.factList:
                if (subgoal["identifier"] == facts["fact"]["identifier"]):
                    #print("The identifiers are equal")
                    factArguements = facts["fact"]["arguments"]
                    ruleArugements = subgoal["arguments"]
                    #print("factarguemets")
                    #print(factArguements)
                    #print(ruleArugements)
					
					
					if (len(factArguements) != len(ruleArugements)):
                        print("Invalid argument length")
                    else:
                        p = 0
                        k = 0
                        while (p < len(factArguements)):

                            if (substitutied.get(ruleArugements[k]) is None):
                                substitutied[ruleArugements[k]] = factArguements[p]
                                p = p + 1
                                k = k + 1

                            else:
                                key = ruleArugements[k]
                                variableValue = substitutied.get(key)
                                #print("Present variableValue is")
                                #print(variableValue)
                                if (variableValue != factArguements[p]):
                                    #print("Not a valid rule")
                                    p = p + 1
                                    k = k + 1
                                    break

                                else:
                                    #print("Valid rule")
                                    trueSubgoals = +1
                                p = p + 1
                                k = k + 1
                        # print(substitutied)
                        # print(substitutied.keys())
                        newFact = []
                        headArguements = rule["rule"]["head"]["arguments"]
                        for each in headArguements:
                            newFact.append(substitutied.get(each))
                            headPredicate = rule["rule"]["head"]["identifier"]
                        # print(headPredicate)
                        # print(newFact)
                        # print(type(newFact))

                else:
                    nofactsMatch=False
                    #print("The identifiers are not equal")
                    substitutied.clear()

    #Formatting the new inferred fact
    val = ','.join([str(item) for item in newFact])
    inferred = str(headPredicate) +"("  + val + ")" + "."
    #print('{}{}'.format("New Facts to EDB ", parser.factList))
    #print('{}{}'.format("Number of subgoals are  ", numberOfSubgoals))
    print("Predicates after unification ")
    print(substitutied)

    #Adding the new facts to the FactList of the parser
    toadd={}
    facttoadd={}
    toadd['identifier']=str(headPredicate)
    toadd['arguments'] = newFact
    facttoadd['fact'] = toadd
    parser.factList.append(facttoadd)
    print("The new factlist of the parser")
    print(parser.factList)