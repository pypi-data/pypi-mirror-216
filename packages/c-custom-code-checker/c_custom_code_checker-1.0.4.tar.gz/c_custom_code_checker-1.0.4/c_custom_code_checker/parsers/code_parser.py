import os
import platform

import clang.cindex
from clang.cindex import Index,LinkageKind,CursorKind

from clang.cindex import TypeKind

import clang.enumerations
from c_custom_code_checker.constants.criterion_keys import CriterionKeys

from c_custom_code_checker.constants.target_keys import TargetKeys
from c_custom_code_checker.utlis.console_utils import print_process

class CodeParser():
   
  def __init__(self,rules,clang_path) -> None:
    #self.__OS_PLATFORM = platform.system()
    clang.cindex.Config.set_library_path(clang_path)
    
    self.__rules = rules


  def __check_rule_compliance(self,node,rule):
      criterion = rule.get_criterion()

      if(criterion[CriterionKeys.HANDLER] is not None):
        criterion[CriterionKeys.HANDLER](node,rule,criterion[CriterionKeys.VALUE_TO_CHECK])

  def __is_this_node_able_be_checked(self,node):
    if((node.kind == CursorKind.MACRO_DEFINITION) or (node.kind == CursorKind.MACRO_INSTANTIATION)):
      #only accept local macro definitions
      if(node.location.file != None):
        return True
      else:
        return False
    else:
      if(node.linkage != LinkageKind.INVALID):
        return True
      else:
        return False
      
  def __check_rule_requirements(self,requirements,node):

    rule_approved = False

    if((len(requirements[TargetKeys.REQUIREMENTS_OR]) > 0)):
      rule_approved = self.__rules_requirements_or(requirements[TargetKeys.REQUIREMENTS_AND],node)

  
    if((len(requirements[TargetKeys.REQUIREMENTS_AND]) > 0) and (rule_approved == False)):
      rule_approved = self.__rules_requirements_and(requirements[TargetKeys.REQUIREMENTS_AND],node)

    #no aditional requirement is needed to aprove rule
    if((len(requirements[TargetKeys.REQUIREMENTS_OR]) == 0) and (len(requirements[TargetKeys.REQUIREMENTS_AND]) == 0)):
      rule_approved = True

    return rule_approved

  def __rules_requirements_and(self,requirements,node):
    aproved = True

    for req in requirements:
      if(self.__check_single_requirement(req,node) == False):
        aproved = False
        break

    return aproved
  
  
  def __rules_requirements_or(self,requirements,node):
    aproved = False

    for req in requirements:
      if(self.__check_single_requirement(req,node) == True):
        aproved = True
        break

    return aproved

  def __check_single_requirement(self,requirement,node):
    approved = True

    if((TargetKeys.CLANG_LINKAGE_KIND in requirement) and not (node.linkage in requirement[TargetKeys.CLANG_LINKAGE_KIND] )):
      approved = False

    if((TargetKeys.CLANG_ACCESS_KIND in requirement ) and not (node.access_specifier in requirement[TargetKeys.CLANG_ACCESS_KIND])):
      approved = False

    if((TargetKeys.CLANG_PARENT_KIND in requirement ) and not(node.lexical_parent.kind in requirement[TargetKeys.CLANG_PARENT_KIND])):
      approved = False

    return approved

  def __parse_node_recursively(self,node):
      
      if(self.__is_this_node_able_be_checked(node)):
        #print(f'nome: {node.displayname} - - kind: {node.kind} tipo: {node.type.kind } -- acessibilidade: {node.access_specifier}')
        for rule in self.__rules:
          for rule_target in rule.get_target():
            if(node.kind in rule_target[TargetKeys.CLANG_KINDS]):
                
                if(self.__check_rule_requirements(rule_target[TargetKeys.REQUIREMENTS],node)):
                  self.__check_rule_compliance(node,rule)

      '''try:
        print(f'nome: {node.displayname} - - kind: {node.kind} tipo: {node.type.kind } -- acessibilidade: {node.access_specifier}')
      except:
        pass
      '''
      
      for c in node.get_children():
        self.__parse_node_recursively(c)


  def parse_code_file(self,file):
    index = Index.create()
    tu = index.parse(file,options=clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
    self.__parse_node_recursively(tu.cursor)