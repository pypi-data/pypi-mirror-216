import os
import sys
import re
import shutil
import glob

argv = sys.argv
argc = len(sys.argv)


Help = '''
SortFile - File Sorting Utility

Description:
SortFile is a command-line utility that helps you organize and sort files based on a specific pattern.

Usage:
SortFile [Pattern] [FolderName]

Pattern: The pattern to match the files you want to sort. Enclose the pattern in double quotes.
FolderName: The name of the folder where the sorted files will be moved.

Examples:
$ SortFile "namefile.*" file
    - Sorts files with the pattern "namefile.*" and moves them to a folder named "file".

$ SortFile "name*.pdf" file
    - Sorts PDF files with names starting with "name" and moves them to a folder named "file".

Note:
- The folder name should not include any symbols, only English letters.
- If the specified folder already exists, you will be prompted to choose whether to move files to it or not.

Command-line Options:
-h, help    Display this help message.

'''

path = os.getcwd()


def main():
    
    chack_argc = Chack_argc()
    if chack_argc == False :
        return

    DataSort = argv[1]
    FileName = str(argv[2])

    chack_fileName = Chack_FileName(FileName)
    if chack_fileName == False:
        return
    
    folder_path = os.path.join(path,FileName)
    createfile = CreateFile(FileName,folder_path)
    
    if createfile == False:
        return 
    MoveFiles(DataSort,folder_path)
    return


def Chack_argc():
    if argc >= 1:
        if argv[1].lower() == "-h" or argv[1].lower() == "help" or argv[1].lower == "-help":
            print(Help)
            return False
        if argc > 3 :
            print("Invalid number of arguments. Only two arguments should be entered.")
            print(Help)
            return False
        if argc < 3 :
            print("Insufficient number of arguments. Two arguments are required.")
            print(Help)
            return False
    return True

def Chack_FileName(FileName) :
    pattern = r"[a-zA-Z]$"
    for i in FileName:
        if not re.match(pattern,i):
            print("The name of the folder should not include any symbols, only English letters")
            return False
    return True

def CreateFile(FileName,folder_path):
    try:
        os.mkdir(folder_path)
        print(f"A folder has been created with the name {FileName}")
        return True
    except:
        print("This folder already exists. Do you want to move files to it [y] or [n]")
        try:
            print("[y,n] : ", end=' ')
            inputUser = input()
            if inputUser.lower() == "y":
                return True
            if inputUser.lower() == "n":
                return False
        except:
            print("\n",end="")
            return False

def MoveFiles(DataSort, folder_path):
    try:
        for file_path in glob.glob(DataSort):
            shutil.move(file_path, os.path.join(folder_path, os.path.basename(file_path)))
        print("Success")
        return True
    except:
        print("An unexpected error occurred, try again")
        return False




if __name__ == "__main__":
    main()