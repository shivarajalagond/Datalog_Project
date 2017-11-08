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
					
					