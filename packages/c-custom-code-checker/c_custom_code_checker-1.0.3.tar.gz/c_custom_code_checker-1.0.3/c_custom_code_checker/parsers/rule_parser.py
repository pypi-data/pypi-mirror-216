import copy
import json
from c_custom_code_checker.constants.criterion_keys import CriterionKeys
from c_custom_code_checker.constants.rules_reserved_keys import RulesReservedKeys
from c_custom_code_checker.constants.target_keys import TargetKeys
from c_custom_code_checker.enums.criterion_enum import CriterionEnum
from c_custom_code_checker.enums.target_enum import TargetEnum
from c_custom_code_checker.exceptions.criterion_value_missing_exception import CriterionValueMissingException
from c_custom_code_checker.exceptions.invalid_criterion_exception import InvalidCriterionException
from c_custom_code_checker.exceptions.invalid_target_exception import InvalidTargetException
from c_custom_code_checker.exceptions.rule_missing_criterion_exception import RuleMissingCriterionException

from c_custom_code_checker.models.rule_model import RuleModel
from c_custom_code_checker.exceptions.rule_missing_target_exception import RuleMissingTargetException


class RuleParser():

    def __parse_criterion(self,in_criterion):
        
        found_criterion = None

        for crit in CriterionEnum:
            if crit.value[CriterionKeys.VALUE_IN_RULE] == in_criterion[RulesReservedKeys.CRITERION_TARGET]:
                found_criterion = crit.value
                if(crit.value[CriterionKeys.REQUIRE_VALUE] == True):

                    if(in_criterion[RulesReservedKeys.CRITERION_VALUE] is None):
                        #raise exception
                        raise CriterionValueMissingException()
                    
                    found_criterion[CriterionKeys.VALUE_TO_CHECK] = in_criterion[RulesReservedKeys.CRITERION_VALUE]
                break

        if(found_criterion is None):
            raise InvalidCriterionException()
        
        return found_criterion
            

    def parse_file(self,path:str):
        with open(path, 'r') as raw_data:
            j_rule = json.load(raw_data)

            target = None
            criterion = None
            name = "unamed"
            file_name = path

            if(RulesReservedKeys.RULE_NAME in j_rule):
                name = j_rule[RulesReservedKeys.RULE_NAME]

            if(not (RulesReservedKeys.TARGET_NAME in j_rule)):
                raise RuleMissingTargetException()
            
            if(not (RulesReservedKeys.CRITERION_OBJ_KEY in j_rule)):
                raise RuleMissingCriterionException()
            
            found_target = []

            for target in TargetEnum:
                if (target.value[TargetKeys.VALUE_IN_RULE] in j_rule[RulesReservedKeys.TARGET_NAME]):
                    found_target.append(target.value)

            if(len(found_target) == 0):
                raise InvalidTargetException()
            
            criterion = copy.deepcopy(self.__parse_criterion(j_rule[RulesReservedKeys.CRITERION_OBJ_KEY]))
        
            ret_rule = RuleModel(name,file_name,j_rule[RulesReservedKeys.RULE_DESCRIPTION],found_target,criterion)

            return ret_rule
            


