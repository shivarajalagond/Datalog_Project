
					
					
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