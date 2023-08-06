from pyparsing import Word, alphas, nums, Literal, Or, And, Group, Forward, QuotedString, infixNotation, opAssoc, ParseResults, ParseException

class Query:
    """
    A class that represents a query in the mongeasy query language using the following syntax:
    <variable> <operator> <value>
    where <variable> is a variable name, <operator> is one of the following operators: >=, <=, ==, !=, in, not in, <, >, and <value> is a value.

    The query can be composed of multiple conditions using the following syntax:
    <condition> and <condition> and <condition> ...
    where <condition> is a condition in the mongeasy query language.

    The query can also contain parentheses to define the order of evaluation of the conditions:
    (<condition> and <condition>) or <condition> and <condition> ...

    Examples:
    ```
    query = Query("age > 25")
    query = Query("age > 25 and friends.age == 32")
    query = Query("age > 25 and (friends.age == 32 or friends.age == 28)")
    query = Query("age > 25 and (friends.age == 32 or friends.age == 28) and name == 'John'")
    ````

    The query can be converted to a MongoDB query using the to_mongo_query() method.

    Examples:
    ``` 
    query = Query("age > 25")
    mongo_query = query.to_mongo_query()
    ```
    The result will be:
    ```
    {'age': {'$gt': 25}}
    ```
    """

    def __init__(self, query_str):
        self.query_str = query_str

    def to_mongo_query(self):
        # Define the basic components of the language
        variable = Word(alphas + '.')
        number = Word(nums).setParseAction(lambda t: int(t[0]))
        string = QuotedString('"')
        value = string | number

        # Define the operators
        operators = ['>=', '<=', '==', '!=', 'in', 'not in', '<', '>']
        condition = Group(variable + Or(map(Literal, operators)) + value)       
        
        # Define the operators
        expr = Forward()
        and_ = Literal('and')
        or_ = Literal('or')
        not_ = Literal('not')
        expr << infixNotation(condition, [(not_, 1, opAssoc.RIGHT, lambda t: {'$not': t[0][0]}), 
                                          (and_, 2, opAssoc.LEFT, lambda t: {'$and': [t[0][0], t[0][2]]}), 
                                          (or_, 2, opAssoc.LEFT, lambda t: {'$or': [t[0][0], t[0][2]]})])

        try:
            # Parse the query
            parsed_query = expr.parseString(self.query_str, parseAll=True)[0]
        except ParseException as e:
            raise ValueError(f"Invalid query string: {self.query_str}. Reason: {str(e)}")

        # Convert the parsed query into a MongoDB query
        try:
            mongo_query = self._to_mongo_query_rec(parsed_query)
        except Exception as e:
            raise ValueError(f"Failed to convert parsed query to MongoDB query. Reason: {str(e)}")

        return mongo_query   

    def _to_mongo_query_rec(self, parsed_query):
        if isinstance(parsed_query, str):
            return parsed_query
        elif isinstance(parsed_query, ParseResults) and len(parsed_query) == 3:
            operator = parsed_query[1]
            if operator == '==':
                return {parsed_query[0]: {'$eq': parsed_query[2]}}
            elif operator == '!=':
                return {parsed_query[0]: {'$ne': parsed_query[2]}}
            elif operator == '<':
                return {parsed_query[0]: {'$lt': parsed_query[2]}}
            elif operator == '>':
                return {parsed_query[0]: {'$gt': parsed_query[2]}}
            elif operator == '<=':
                return {parsed_query[0]: {'$lte': parsed_query[2]}}
            elif operator == '>=':
                return {parsed_query[0]: {'$gte': parsed_query[2]}}
            elif operator == 'in':
                return {parsed_query[0]: {'$in': parsed_query[2]}}
            elif operator == 'not in':
                return {parsed_query[0]: {'$nin': parsed_query[2]}}
            else:
                raise ValueError(f'Invalid operator: {operator}')
        elif isinstance(parsed_query, dict):
            for k, v in parsed_query.items():
                if isinstance(v, list):
                    parsed_query[k] = [self._to_mongo_query_rec(item) for item in v]
            return parsed_query
        else:
            raise ValueError(f'Invalid parsed query: {parsed_query}')
