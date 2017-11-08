import pyparsing as pp

class Parser:

    def __init__(self, text):
        self.text = text
        self.factList = []
        self.ruleList = []
        self.errorList = []
        self.warningList = []

    def checkSafety(self,tokens):
        #self.warningList.append(tokens['head']['arguments'])
        return None

    def parse(self):
        colonDash = pp.Literal(":-")

        integer = pp.Word(pp.nums)
        decimal = pp.Combine(pp.Word(pp.nums) + "." + pp.Word(pp.nums))
        number = decimal | integer

        # To-Do: special characters should be tested
        string = "\'" + pp.Word(pp.printables + ' ', excludeChars='\'') + "\'"

        # Identifier is a word started with a lower case letter
        identifier = pp.Word(pp.alphas.lower(), pp.alphanums + '_')

        constant = string | number | identifier
        constantList = pp.delimitedList(constant)

        variable = pp.Word(pp.alphas.upper(), pp.alphanums + '_')
        variableList = pp.delimitedList(variable)

        argumentList = pp.ZeroOrMore( constant +pp.Literal(",").suppress())+ \
                       variableList+\
                       pp.Optional(pp.Literal(",").suppress()+pp.delimitedList(constant|variable))

        #Built-in predicate
        compOperator = pp.oneOf("< <= > >=")
        equalOperator = pp.oneOf("== !=")

        equalBuiltInPredicate = pp.Group("(" + (variable + equalOperator.setResultsName('equalOperators') + (variable|constant)) |\
                           ((variable|constant) + equalOperator + variable) + ")")
        compBuiltInPredicate = pp.Group("(" + (variable + compOperator.setResultsName('compOperators') + (variable|constant)) |\
                          ((variable|constant) + compOperator + variable) |\
                          (variable + compOperator + variable)+ ")")

        builtInPredicate = equalBuiltInPredicate | compBuiltInPredicate

        # predicate => argumentList has at least one variable inside
        predicate = pp.Group(identifier.setResultsName('identifier') + "(" + pp.Group(argumentList).setResultsName('arguments') + ")")

        '''predicateOrBuiltInList = pp.ZeroOrMore(builtInPredicate + pp.Literal(",").suppress()) + \
                                    predicateList + \
                                    pp.ZeroOrMore(pp.Literal(",").suppress() + \
                                                  pp.delimitedList(predicate | builtInPredicate))
        '''
        #predicateOrBuiltInList = pp.delimitedList(predicate|builtInPredicate)

        fact = pp.Group(identifier.setResultsName('identifier') + "(" + pp.Group(constantList).setResultsName('arguments') +\
                        ")" + pp.Literal(".").suppress()).setResultsName('fact')

        rule = pp.Group(predicate.setResultsName('head') + colonDash + \
                        pp.Group(pp.delimitedList(predicate|builtInPredicate|fact)) \
                        .setResultsName('body') + pp.Literal(".").suppress()).setResultsName('rule')

        #parse the text
        for line in self.text:
            safe = True;
            try:
                newFact = fact.parseString(line).asDict()
                print(newFact)
                self.factList.append(newFact)
            except pp.ParseException as factError:
                try:
                    newRule = rule.parseString(line).asDict()
                    print(newRule)
                    headVariables = []
                    for arg in newRule['rule']['head']['arguments']:
                        if (arg[0].isupper()):
                            headVariables.append(arg)

                    bodyVariables = []
                    for item in newRule['rule']['body']:
                        for arg in item['arguments']:
                            if (arg[0].isupper()):
                                bodyVariables.append(arg)

                    #Change bodyVariables and headVariables to a unique set to remove duplicate variables
                    bodyVariables = set(bodyVariables)
                    headVariables = set(headVariables)

                    #check safety type 1: head variables should be appeared on the body
                    for var in headVariables:
                        if (not(var in bodyVariables)):
                            self.warningList.append(var + " is not safe ")
                            safe = False;

                    #check safety type2: Variables in built-in predicates should be bounded

                    if (safe):
                        self.ruleList.append(newRule)

                except pp.ParseException as ruleError:
                    self.errorList.append(factError)
                    self.errorList.append(ruleError)

def main():
    tmpText = """\
            e(1,2).
                e(2,3).
                e(3,4).
                p(X,Q) :-  e(X,Y) , e (Y,Z), e(Z,Q).""".splitlines()
    datalogParser = Parser(tmpText)
    datalogParser.parse()
    print("facts")
    print(datalogParser.factList)
    print("Rules:")
    print(datalogParser.ruleList)
    print("Errors:")
    print(datalogParser.errorList)
    print("Warnings:")
    print(datalogParser.warningList)




if __name__ == '__main__':
    main()





