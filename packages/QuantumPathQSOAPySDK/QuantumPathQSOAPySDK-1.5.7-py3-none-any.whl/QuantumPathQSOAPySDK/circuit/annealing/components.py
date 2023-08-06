from ...utils.checker import (checkInputTypes, checkListTypes, checkMathExpression)
import uuid


##################_____PRIVATE CLASSES_____##################

# EXPRESSION
class __Expression():

    # CONSTRUCTOR
    def __init__(self, expType: str, coefficient: str = '', offset: str = '', fromValue: str = '', toValue: str = '',
                    iterator: str = '', term1: dict = {}, term2: dict = {}, childs: list = []):
        self.__uiID = str(uuid.uuid4())
        self.__expType = expType
        self.__coefficient = coefficient
        self.__offset = offset
        self.__from = fromValue
        self.__to = toValue
        self.__iterator = iterator
        self.__term1 = term1
        self.__term2 = term2
        self.__childs = childs

    # GETTERS
    def getUiID(self):
        """
        Get Expression uiID.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__uiID
    
    def getExpType(self):
        """
        Get Expression type.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__expType

    def getCoefficient(self):
        """
        Get Expression coefficient.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__coefficient
    
    def getOffset(self):
        """
        Get Expression offset.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__offset

    def getFrom(self):
        """
        Get Expression from.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__from

    def getTo(self):
        """
        Get Expression to.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__to

    def getIterator(self):
        """
        Get Expression iterator.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        str
        """

        return self.__iterator

    def getTerm1(self):
        """
        Get Expression term1.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        dict
        """

        return self.__term1

    def getTerm2(self):
        """
        Get Expression term2.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        dict
        """

        return self.__term2

    def getChilds(self):
        """
        Get Expression childs.

        Prerequisites
        ----------
        - Created expression.

        Output
        ----------
        list
        """

        return self.__childs


##################_____PUBLIC CLASSES_____##################

# PARAMETER
class Parameter:

    # CONSTRUCTOR
    def __init__(self, name: str, value):
        """
        Create Circuit Parameter.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        name : str
            Circuit Parameter name.
        value : int | float | str
            Parameter value.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('value', value, (int, float, str))
        )
        if isinstance(value, str):
            checkMathExpression('value', value)
        
        self.__uiID = str(uuid.uuid4())
        self.__name = name
        self.__value = str(value)
    
    
    # MAGIC METHODS
    def __add__(self, other):
        if isinstance(other, (int, float, str)):
            return f'{self.__name} + {other}'

        elif isinstance(other, Parameter):
            return f'{self.__name} + {other.__name}'

    def __sub__(self, other):
        if isinstance(other, (int, float, str)):
            return f'{self.__name} - {other}'

        elif isinstance(other, Parameter):
            return f'{self.__name} - {other.__name}'

    def __mul__(self, other):
        if isinstance(other, (int, float, str)):
            return f'{self.__name} * {other}'

        elif isinstance(other, Parameter):
            return f'{self.__name} * {other.__name}'

    def __truediv__(self, other):
        if isinstance(other, (int, float, str)):
            return f'{self.__name} / {other}'

        elif isinstance(other, Parameter):
            return f'{self.__name} / {other.__name}'

    def __neg__(self):
        return f'-{self.__name}'


    # GETTERS
    def getUiID(self):
        """
        Get Circuit Parameter uiID.

        Prerequisites
        ----------
        - Created parameter.

        Output
        ----------
        str
        """
        return self.__uiID

    def getName(self):
        """
        Get Circuit Parameter name.

        Prerequisites
        ----------
        - Created parameter.

        Output
        ----------
        str
        """
        return self.__name
    
    def getValue(self):
        """
        Get Circuit Parameter value.

        Prerequisites
        ----------
        - Created parameter.

        Output
        ----------
        str
        """
        return self.__value


# AUXDATA
class AuxData:
    
    # CONSTRUCTOR
    def __init__(self, name: str, value):
        """
        Create Circuit Auxiliary Data.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        name : str
            Circuit Auxiliary Data name.
        value : int | float | list
            Auxiliary Data value or list of values.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('value', value, (int, float, list))
        )
        if isinstance(value, list):
            checkListTypes(('value', value, (int, float, list)))

        self.__uiID = str(uuid.uuid4())
        self.__name = name
        self.__value = str(value)
    

    # GETTERS
    def getUiID(self):
        """
        Get Circuit Auxiliary Data uiID.

        Prerequisites
        ----------
        - Created auxiliary data.

        Output
        ----------
        str
        """
        return self.__uiID

    def getName(self):
        """
        Get Circuit Auxiliary Data name.

        Prerequisites
        ----------
        - Created auxiliary data.

        Output
        ----------
        str
        """
        return self.__name
    
    def getValue(self):
        """
        Get Circuit Auxiliary Data value.

        Prerequisites
        ----------
        - Created auxiliary data.

        Output
        ----------
        str
        """
        return self.__value
    

# CLASS
class Class:

    # CONSTRUCTOR
    def __init__(self, name: str, numberOfVars, description: str = ''):
        """
        Create Circuit Class.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        name : str
            Circuit Class name.
        numberOfVars : int | Parameter obj
            Number of Class variables.
        description : str
            Optional argument. Class description.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('numberOfVars', numberOfVars, (int, Parameter)),
            ('description', description, (str,))
        )

        self.__properties = []
        self.__uiID = str(uuid.uuid4())
        self.__name = name
        self.__numberOfVars = str(numberOfVars) if isinstance(numberOfVars, int) else numberOfVars.getName()
        self.__intNumberOfVars = numberOfVars if isinstance(numberOfVars, int) else numberOfVars.getValue()
        self.__description = description


    # GETTERS
    def getProperties(self):
        """
        Get Circuit Class properties.

        Prerequisites
        ----------
        - Created class.

        Output
        ----------
        list
        """
        return self.__properties
    
    def getUiID(self):
        """
        Get Circuit Class uiID.

        Prerequisites
        ----------
        - Created class.

        Output
        ----------
        str
        """
        return self.__uiID

    def getName(self):
        """
        Get Circuit Class name.

        Prerequisites
        ----------
        - Created class.

        Output
        ----------
        str
        """
        return self.__name
    
    def getNumberOfVars(self):
        """
        Get Circuit Class number of variables.

        Prerequisites
        ----------
        - Created class.

        Output
        ----------
        str
        """
        return self.__numberOfVars
    
    def getDescription(self):
        """
        Get Circuit Class description.

        Prerequisites
        ----------
        - Created class.

        Output
        ----------
        str
        """
        return self.__description
    

    # METHODS
    def addProperty(self, name: str, value: list):
        """
        Add Class Property.

        Prerequisites
        ----------
        - Created class.

        Parameters
        ----------
        name : str
            Class Property name.
        value : list
            List of property values. It may be the same that Class number of variables.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('value', value, (list,))
        )
        checkListTypes(('value', value, (int,)))

        if len(value) != int(self.__intNumberOfVars): # number of values and number of vars are not the same
            raise ValueError('Quantity of property values and number of variables must be the same')
        
        self.__properties.append({
            'uiID': str(uuid.uuid4()),
            'Name': name,
            'Values': list(map(str, value))
        })

        return self


# VARIABLE
class Variable:

    # CONSTRUCTOR
    def __init__(self, name: str, classes, description: str = ''):
        """
        Create Circuit Variable.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        name : str
            Circuit Variable name.
        classes : Class obj | list
            Class object or list of Class objects.
        description : str
            Optional argument. Variable description.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('classes', classes, (Class, list)),
            ('description', description, (str,))
        )

        self.__classes = []
        
        if isinstance(classes, list):
            checkListTypes(('classes', classes, (Class,)))

            for c in classes:
                self.__classes.append(c.getUiID())
        
        else:
            self.__classes.append(classes.getUiID())

        self.__uiID = str(uuid.uuid4())
        self.__name = name
        self.__description = description

    # GETTERS
    def getClasses(self):
        """
        Get Circuit Variable Classes uiID.

        Prerequisites
        ----------
        - Created variable.

        Output
        ----------
        list
        """
        return self.__classes

    def getUiID(self):
        """
        Get Circuit Variable uiID.

        Prerequisites
        ----------
        - Created variable.

        Output
        ----------
        str
        """
        return self.__uiID
    
    def getName(self):
        """
        Get Circuit Variable name.

        Prerequisites
        ----------
        - Created variable.

        Output
        ----------
        str
        """
        return self.__name
    
    def getDescription(self):
        """
        Get Circuit Variable description.

        Prerequisites
        ----------
        - Created variable.

        Output
        ----------
        str
        """
        return self.__description


# RULE
class Rule:

    # CONSTRUCTOR
    def __init__(self, name: str, lambdaValue, description = '', disabled = False):
        """
        Create Circuit Rule.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        name : str
            Circuit Rule name.
        lambdaValue : int | float | str
            Parameter value.
        description : str
            Optional argument. Rule description.
        disabled : bool
            Optional argument. Enable / disable rule.
        """
        checkInputTypes(
            ('name', name, (str,)),
            ('lambdaValue', lambdaValue, (int, float, str)),
            ('description', description, (str,)),
            ('disabled', disabled, (bool,)),
        )
        if isinstance(lambdaValue, str):
            checkMathExpression('lambdaValue', lambdaValue)

        self.__expressions = []
        self.__uiID = str(uuid.uuid4())
        self.__name = name
        self.__lambda = str(lambdaValue)
        self.__description = description
        self.__disabled = str(disabled)


    # GETTERS
    def getExpressions(self):
        """
        Get Circuit Rule expressions.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        list
        """

        return self.__expressions

    def getUiID(self):
        """
        Get Circuit Rule uiID.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        str
        """

        return self.__uiID
    
    def getName(self):
        """
        Get Circuit Rule name.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        str
        """

        return self.__name
    
    def getLambda(self):
        """
        Get Circuit Rule lambda.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        str
        """

        return self.__lambda
    
    def getDescription(self):
        """
        Get Circuit Rule description.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        str
        """

        return self.__description
    
    def getDisabled(self):
        """
        Get Circuit Rule disable status.

        Prerequisites
        ----------
        - Created rule.

        Output
        ----------
        str
        """

        return self.__disabled

    # METHODS
    def addExpression(self, expression):
        """
        Add Rule Expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        expression : SummationExp obj | SquaredExp obj | LinearExp obj | QuadraticExp obj | OffsetExp obj | list
            Expression to add. It could be an object or a list of following objects: SummationExp, SquaredExp, LinearExp, QuadraticExp or OffsetExp.
        
        Output
        ----------
        Rule obj
        """
        def appendExpression(expression):
            self.__expressions.append({
                'uiID': expression.getUiID(),
                'Type': expression.getExpType(),
                'Coefficient': expression.getCoefficient(),
                'Offset': expression.getOffset(),
                'From': expression.getFrom(),
                'To': expression.getTo(),
                'Iterator': expression.getIterator(),
                'Term1': expression.getTerm1(),
                'Term2': expression.getTerm2(),
                'Childs': expression.getChilds()
            })

        checkInputTypes(
            ('expression', expression, (SummationExp, SquaredExp, LinearExp, QuadraticExp, OffsetExp, list))
        )
        if isinstance(expression, list):
            checkListTypes(('expression', expression, (SummationExp, SquaredExp, LinearExp, QuadraticExp, OffsetExp)))

            for e in expression:
                appendExpression(e)
        
        else:
            appendExpression(expression)

        return self


# OFFSET EXPRESSION
class OffsetExp(__Expression):
    
    # CONSTRUCTOR
    def __init__(self, offset): 
        """
        Create Offset expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        offset : int | float | str | Parameter
            Offset value.
        """
        checkInputTypes(
            ('offset', offset, (int, float, str, Parameter))
        )

        if isinstance(offset, Parameter):
            offset = offset.getName()

        super().__init__(expType='OFFSET', offset=str(offset))


# LINEAR EXPRESSION
class LinearExp(__Expression):
    
    # CONSTRUCTOR
    def __init__(self, variable: tuple, coefficient = ''):
        """
        Create Linear expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        variable: tuple
            Circuit variable and values. First element: Variable obj. Second element: value or list of values (One per class in variable).
        coefficient : int | float | str | Parameter
            Optional argument. Coefficient value.
        """
        def appendIndex(termIndexes: dict, variable: Variable, index: int):
            if isinstance(variable[1], list):
                value = variable[1][index].getName() if isinstance(variable[1][index], Parameter) else str(variable[1][index])
            else:
                value = variable[1].getName() if isinstance(variable[1], Parameter) else str(variable[1])

            termIndexes.append({
                'uiID': str(uuid.uuid4()),
                'Value': value,
                'ClassID': variable[0].getClasses()[index]
            })

        def checkVariablesAndClasses(variable):
            numberOfClasses = len(variable[0].getClasses())

            if isinstance(variable[1], list):
                if len(variable[1]) != numberOfClasses:
                    raise ValueError(f'Expected {numberOfClasses} variable values, not {len(variable[1])}')  
            else:
                if numberOfClasses != 1:
                    raise ValueError(f'Expected {numberOfClasses} variable values, not 1')
        
        if isinstance(variable, tuple):
            if len(variable) != 2: # number of variable elements are not 2
                raise ValueError('variable takes 2 positional arguments')
        
        checkInputTypes(
            ('variable', variable, (tuple,)),
            ('variable', variable[0], (Variable,)),
            ('variable', variable[1], (int, float, str, Parameter, list)),
            ('coefficient', coefficient, (int, float, str, Parameter))
        )
        if isinstance(variable[1], list):
            checkListTypes(('variable', variable[1], (int, float, str, Parameter)))
        
        checkVariablesAndClasses(variable) # check number of variable numbers are the same that variable classes

        term1 = {
            'Indexes': [],
            'uiID': str(uuid.uuid4()),
            'VariableID': variable[0].getUiID()
        }

        if isinstance(variable[1], list):
            for index in range(0, len(variable[1])):
                appendIndex(term1['Indexes'], variable, index)
        else:
            appendIndex(term1['Indexes'], variable, 0)
        
        if isinstance(coefficient, Parameter):
            coefficient = coefficient.getName()

        super().__init__(expType='LINEAR', coefficient=str(coefficient), term1=term1)


# QUADRATIC EXPRESSION
class QuadraticExp(__Expression):
    
    # CONSTRUCTOR
    def __init__(self, variable1: tuple, variable2: tuple, coefficient = ''): 

        """
        Add Quadratic expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        variable1: tuple
            Circuit variable and values. First element: Variable obj. Second element: value or list of values (One per class in variable).
        variable2: tuple
            Circuit variable and values. First element: Variable obj. Second element: value or list of values (One per class in variable).
        coefficient : int | float | str | Parameter
            Optional argument. Coefficient value.
        """
        def appendIndex(termIndexes: dict, variable: Variable, index: int):
            if isinstance(variable[1], list):
                value = variable[1][index].getName() if isinstance(variable[1][index], Parameter) else str(variable[1][index])
            else:
                value = variable[1].getName() if isinstance(variable[1], Parameter) else str(variable[1])

            termIndexes.append({
                'uiID': str(uuid.uuid4()),
                'Value': value,
                'ClassID': variable[0].getClasses()[index]
            })

        def checkVariablesAndClasses(variable):
            numberOfClasses = len(variable[0].getClasses())

            if isinstance(variable[1], list):
                if len(variable[1]) != numberOfClasses:
                    raise ValueError(f'Expected {numberOfClasses} variable values, not {len(variable[1])}')
                
            else:
                if numberOfClasses != 1:
                    raise ValueError(f'Expected {numberOfClasses} variable values, not 1')

        if isinstance(variable1, tuple):
            if len(variable1) != 2: # number of variable1 elements are not 2
                raise ValueError('variable1 takes 2 positional arguments')
        if isinstance(variable2, tuple):
            if len(variable2) != 2: # number of variable2 elements are not 2
                raise ValueError('variable2 takes 2 positional arguments')
        
        checkInputTypes(
            ('variable1', variable1, (tuple,)),
            ('variable1', variable1[0], (Variable,)),
            ('variable1', variable1[1], (int, float, str, Parameter, list)),
            ('variable2', variable2, (tuple,)),
            ('variable2', variable2[0], (Variable,)),
            ('variable2', variable2[1], (int, float, str, Parameter, list)),
            ('coefficient', coefficient, (int, float, str, Parameter))
        )
        if isinstance(variable1[1], list):
            checkListTypes(('variable1', variable1[1], (int, float, str, Parameter)))
        if isinstance(variable2[1], list):
            checkListTypes(('variable2', variable2[1], (int, float, str, Parameter)))

        checkVariablesAndClasses(variable1) # check number of variable numbers are the same that variable classes
        checkVariablesAndClasses(variable2)

        term1 = {
            'Indexes': [],
            'uiID': str(uuid.uuid4()),
            'VariableID': variable1[0].getUiID()
        }

        term2 = {
            'Indexes': [],
            'uiID': str(uuid.uuid4()),
            'VariableID': variable2[0].getUiID()
        }

        if isinstance(variable1[1], list):
            for index in range(0, len(variable1[1])):
                appendIndex(term1['Indexes'], variable1, index)
        else:
            appendIndex(term1['Indexes'], variable1, 0)
        
        if isinstance(variable2[1], list):
            for index in range(0, len(variable2[1])):
                appendIndex(term2['Indexes'], variable2, index)
        else:
            appendIndex(term2['Indexes'], variable2, 0)
        
        if isinstance(coefficient, Parameter):
            coefficient = coefficient.getName()

        super().__init__(expType='QUADRATIC', coefficient=str(coefficient), term1=term1, term2=term2)


# SQUARED EXPRESSION
class SquaredExp(__Expression):
    
    # CONSTRUCTOR
    def __init__(self, expression): 
        """
        Create Squared expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        expression: SummationExp obj | LinearExp obj | OffsetExp obj | list
            Expression or list of expressions to be squared. It could be a Summation, Linear, or Offset expression.
        """
        childs = []
        def appendChild(expression):
            childs.append({
                'uiID': expression.getUiID(),
                'Type': expression.getExpType(),
                'Coefficient': expression.getCoefficient(),
                'Offset': expression.getOffset(),
                'From': expression.getFrom(),
                'To': expression.getTo(),
                'Iterator': expression.getIterator(),
                'Term1': expression.getTerm1(),
                'Term2': expression.getTerm2(),
                'Childs': expression.getChilds()
            })

        checkInputTypes(
            ('expression', expression, (SummationExp, LinearExp, OffsetExp, list))
        )
        if isinstance(expression, list):
            checkListTypes(('expression', expression, (SummationExp, LinearExp, OffsetExp)))

            for exp in expression:
                appendChild(exp)
        
        else:
            appendChild(expression)

        super().__init__(expType='SQUARED', childs=childs)


# SUMMATION EXPRESSION
class SummationExp(__Expression):
    
    # CONSTRUCTOR
    def __init__(self, fromValue, toValue, expression, iterator: str = 'i'): 
        """
        Create Summation expression.

        Prerequisites
        ----------
        - Created rule.

        Parameters
        ----------
        fromValue: int | float | str | Parameter
            Start value of the summation iteration.
        toValue: int | float | str | Parameter
            End value of the summation iteration.
        expression: SummationExp obj | SquaredExp obj | LinearExp obj | QuadraticExp obj | OffsetExp obj | list
            Expression or list of expressions to be inside of the summation. It could be a Summation, Squared, Linear, Quadratic or Offset expression.
        iterator: str
            Iterator name.
        """
        childs = []
        def appendChild(expression):
            childs.append({
                'uiID': expression.getUiID(),
                'Type': expression.getExpType(),
                'Coefficient': expression.getCoefficient(),
                'Offset': expression.getOffset(),
                'From': expression.getFrom(),
                'To': expression.getTo(),
                'Iterator': expression.getIterator(),
                'Term1': expression.getTerm1(),
                'Term2': expression.getTerm2(),
                'Childs': expression.getChilds()
            })

        checkInputTypes(
            ('fromValue', fromValue, (int, float, str, Parameter)),
            ('toValue', toValue, (int, float, str, Parameter)),
            ('expression', expression, (SummationExp, SquaredExp, LinearExp, QuadraticExp, OffsetExp, list)),
            ('iterator', iterator, (str,)),
        )
        if isinstance(expression, list):
            checkListTypes(('expression', expression, (SummationExp, SquaredExp, LinearExp, QuadraticExp, OffsetExp)))

            for exp in expression:
                appendChild(exp)
        
        else:
            appendChild(expression)
        
        if isinstance(fromValue, Parameter):
            fromValue = fromValue.getName()
        if isinstance(toValue, Parameter):
            toValue = toValue.getName()

        super().__init__(expType='SUMMATORY', fromValue=str(fromValue), toValue=str(toValue), iterator=iterator, childs=childs)