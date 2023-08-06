# SortFile - File Sorting Utility

### Description:
SortFile is a command-line utility that helps you organize and sort files based on a specific pattern.

### Usage:
```
SortFile [Pattern] [FolderName]
```

> Pattern: The pattern to match the files you want to sort. Enclose the pattern in double quotes.
> FolderName: The name of the folder where the sorted files will be moved.

## Examples:
``` 
$ SortFile "namefile.*" file
```
- Sorts files with the pattern "namefile.*" and moves them to a folder named "file".

```
$ SortFile "name*.pdf" file
```
- Sorts PDF files with names starting with "name" and moves them to a folder named "file".

### Note:
- The folder name should not include any symbols, only English letters.
- If the specified folder already exists, you will be prompted to choose whether to move files to it or not.

Command-line Options:
-h, help    Display this help message.