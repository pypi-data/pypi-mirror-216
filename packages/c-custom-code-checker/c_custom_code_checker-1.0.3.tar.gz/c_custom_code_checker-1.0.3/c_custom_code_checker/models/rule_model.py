
from c_custom_code_checker.enums.criterion_enum import CriterionEnum
from c_custom_code_checker.enums.target_enum import TargetEnum


class RuleModel:

    def __init__(self,name,file_name, description, target: list, criterion: CriterionEnum) -> None:
        self.__target = target
        self.__criterion = criterion
        self.__name = name
        self.__file_name = file_name
        self.__description = description

    def get_criterion(self) -> CriterionEnum:
        return self.__criterion
    
    def get_target(self) -> list:
        return self.__target
    
    def get_name(self):
        return self.__name
    
    def get_file_name(self):
        return self.__file_name
    
    def get_description(self):
        return self.__description

    def on_success():
        pass

    def on_failure():
        pass