from enum import Enum

from clang.cindex import CursorKind,LinkageKind,AccessSpecifier
from c_custom_code_checker.constants.rules_reserved_keys import RulesReservedKeys

from c_custom_code_checker.constants.target_keys import TargetKeys

class TargetEnum(Enum):
    TARGET_NONE = {TargetKeys.VALUE_IN_RULE: RulesReservedKeys.TARGET_TYPE_NONE,TargetKeys.CLANG_KINDS:[],TargetKeys.CLANG_LINKAGE_KIND:None,TargetKeys.CLANG_ACCESS_KIND:None}
    TARGET_FUNCTION = {TargetKeys.VALUE_IN_RULE: RulesReservedKeys.TARGET_TYPE_METHODS, TargetKeys.CLANG_KINDS:[CursorKind.FUNCTION_DECL,CursorKind.FUNCTION_TEMPLATE], TargetKeys.REQUIREMENTS:{TargetKeys.REQUIREMENTS_AND:[{TargetKeys.CLANG_LINKAGE_KIND:[LinkageKind.INTERNAL]}],TargetKeys.REQUIREMENTS_OR:[]}}
    TARGET_GLOBAL_VARIABLE = {TargetKeys.VALUE_IN_RULE:RulesReservedKeys.TARGET_TYPE_GLOBALS, TargetKeys.CLANG_KINDS:[CursorKind.VAR_DECL],TargetKeys.REQUIREMENTS:{TargetKeys.REQUIREMENTS_AND:[{TargetKeys.CLANG_LINKAGE_KIND:[LinkageKind.INTERNAL]},{TargetKeys.CLANG_PARENT_KIND:[CursorKind.TRANSLATION_UNIT]}],TargetKeys.REQUIREMENTS_OR:[{TargetKeys.CLANG_ACCESS_KIND:AccessSpecifier.PUBLIC},{TargetKeys.CLANG_PARENT_KIND:None}]}}
    TARGET_LOCAL_VARIABLE = {TargetKeys.VALUE_IN_RULE: RulesReservedKeys.TARGET_TYPE_VARIABLES,TargetKeys.CLANG_KINDS:[CursorKind.VAR_DECL],TargetKeys.REQUIREMENTS:{TargetKeys.REQUIREMENTS_AND:[{TargetKeys.CLANG_LINKAGE_KIND:[LinkageKind.INTERNAL]}],TargetKeys.REQUIREMENTS_OR:[]}}
    TARGET_DEFINE = {TargetKeys.VALUE_IN_RULE:RulesReservedKeys.TARGET_TYPE_DEFINES,TargetKeys.CLANG_KINDS:[CursorKind.MACRO_DEFINITION,CursorKind.MACRO_INSTANTIATION],TargetKeys.REQUIREMENTS:{TargetKeys.REQUIREMENTS_AND:[],TargetKeys.REQUIREMENTS_OR:[]}}
    TARGET_TYPE_ENUMS = {TargetKeys.VALUE_IN_RULE:RulesReservedKeys.TARGET_TYPE_ENUMS,TargetKeys.CLANG_KINDS:[CursorKind.ENUM_DECL],TargetKeys.REQUIREMENTS:{TargetKeys.REQUIREMENTS_AND:[],TargetKeys.REQUIREMENTS_OR:[]}}