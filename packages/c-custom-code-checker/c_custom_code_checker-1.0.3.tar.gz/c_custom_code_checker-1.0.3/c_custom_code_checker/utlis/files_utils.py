

import os


def search_files_by_keyword(dir, keyword,format=None):
    found = []

    for root, dirs, files in os.walk(dir):
        for file in files:
            if(format is not None):
                if file.endswith(f".{format}") and keyword in file:
                    found.append(os.path.join(root, file))
            else:
                if keyword in file:
                    found.append(os.path.join(root, file))

    return found