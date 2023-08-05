class RulesReservedKeys():

    '''
        Rule basic details
    '''
    RULE_NAME = "name"
    RULE_DESCRIPTION = "description"

    '''
        Target keys
    '''
    TARGET_NAME = "target"

    TARGET_TYPE_NONE = "none"
    TARGET_TYPE_METHODS = "functions"
    TARGET_TYPE_GLOBALS = "globals"
    TARGET_TYPE_VARIABLES = "variables"
    TARGET_TYPE_DEFINES = "macros"
    TARGET_TYPE_ENUMS = "enums"


    '''
        Criterions
    '''
    CRITERION_OBJ_KEY = "criterion"
    CRITERION_TARGET = "target"
    CRITERION_VALUE = "value"

    '''
        Criterion target values
    '''
    NONE = "none"
    LENGTH_LESS_THAN = "length_less_than"
    LENGTH_BIGGER_THAN = "length_bigger_than"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    REGEX = "regex"

