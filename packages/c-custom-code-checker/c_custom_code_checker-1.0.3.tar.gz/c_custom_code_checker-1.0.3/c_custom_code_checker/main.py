import os
import argparse
import glob
import platform

from tqdm import tqdm

from c_custom_code_checker.constants.strings import StringsConstants
from c_custom_code_checker.exceptions.lib_clang_not_found_exception import LibClangNotFoundException

from c_custom_code_checker.parsers.code_parser import CodeParser
from c_custom_code_checker.parsers.rule_parser import RuleParser
from c_custom_code_checker.utlis.console_utils import  print_exception, print_failure, print_header, print_process, print_success
from c_custom_code_checker.utlis.files_utils import search_files_by_keyword


ruleParser = RuleParser()
lib_clang_path = None

def get_libclang_install_dir():
    path_env = os.getenv("PATH")
    platform_name = platform.system()

    if path_env:
        paths = path_env.split(os.pathsep)
        for path in paths:

            if(platform_name == "Windows"):
                libclang_path = os.path.join(path, "libclang.dll")  
                if os.path.isfile(libclang_path):
                    return path
            else:
                libclang_path = os.path.join(path, "libclang.so")  
                if os.path.isfile(libclang_path):
                    return path
    return None



def check_prerequisites():

    global lib_clang_path
    
    #check if there is libclang environment variable
    lib_clang_path = get_libclang_install_dir()
    if (lib_clang_path == None):
        raise LibClangNotFoundException()
    

def check_rules(files,rules_directory):
    rules = []
    ret_files = search_files_by_keyword(rules_directory,"rule","json")

    if(len(ret_files) == 0):
        print_failure(StringsConstants.NO_RULES_FOUND)
        return -1
    
    pbar = tqdm(ret_files)
    for file in pbar:
        pbar.set_description(f'Reading rule: {file}')
        rules.append(ruleParser.parse_file(file))

    return rules

def check_code(files,rules):

    global lib_clang_path

    print_process(StringsConstants.CODE_CHECKING_TITLE)

    code_parser = CodeParser(rules,lib_clang_path)
    pbar = tqdm(files)

    for code in pbar:
        pbar.set_description(f"{code}")
        code_parser.parse_code_file(code)


def startup(files,rules_directory):

    try:

        check_prerequisites()

        print_header()
        print_process(StringsConstants.PARSING_RULES_TITLE)

        rules = check_rules(files,rules_directory)

    except Exception as e:
        print_exception(e)
        print_failure(StringsConstants.RULE_PARSING_FAILED)
        return -1

    print_success(StringsConstants.RULE_PARSING_SUCCEDED)

    try:
        check_code(files,rules)
        print_success(StringsConstants.CODE_CHECKING_SUCCEDED)
        return 0
    except Exception as e:
        print_exception(e)
        return -1
    


def main():
    parser = argparse.ArgumentParser(description=StringsConstants.TITLE)
    parser.add_argument("--input","-i",nargs="+",help="List of C files to analyse",required=True)
    parser.add_argument("--rules_path","-r",help="Path to rules",required=True)

    args = parser.parse_args()

    in_files = []

    for input_record in args.input:

        # Check if the argument contains wildcard characters
        if '*' in input_record or '?' in input_record:
            # Use glob to get a list of matching file paths
            file_paths = glob.glob(input_record)
            for file_path in file_paths:
                in_files.append(file_path)

        else:
            in_files.append(input_record)

    rules_path = args.rules_path

    return startup(in_files,rules_path)


if __name__ == "__main__":
    main()