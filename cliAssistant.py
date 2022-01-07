import datetime, os, sys
import subprocess


#### #### #### #### #### 
#### Functions #### 
#### #### #### #### #### 
def ExitHandler() -> None:
    print("Bye")
    input("Press any key to continue ...")
    sys.exit() ## NOTE: try-except will catch sys.exit() as it raises SystemExit


def CheckAndRaiseExiting(userInput:str) -> None:
    if userInput == "exit":
        raise SystemExit


def TipsBeforeInput() -> None:
    print("If you want to exit, Enter exit or press Ctrl-C")


def GetTargetDirectory() -> str:
    while True:
        TipsBeforeInput()
        targetDirectory = input(r"Enter the location of media files for renaming (e.g. C:\Users\eee\Pictures): ")
        CheckAndRaiseExiting(targetDirectory)
        if os.path.isdir(targetDirectory):
            return targetDirectory
        print("The location does not exist. Try again.")


def GetAlternativeDate() -> datetime.date:
    while True:
        alternativeDate = input("Date (YYYY-MM-DD) for files naming if date & time information cannot be found. Leave it empty if you do not care: ")
        CheckAndRaiseExiting(alternativeDate)
        if alternativeDate == "":
            print("You did not provide an alternative date. File names will be preceded by 00000000_000000 if date & time information cannot be found")
            return None
        try:
            alternativeDate = datetime.date.fromisoformat(alternativeDate)
            return alternativeDate
        except ValueError:
            print("Your input is not a valid date in YYYY-MM-DD format. Try again.")


def GetIsRecursiveSearch() -> bool:
    while True:
        isRecursiveSearch = input("Do you want the program to recursively search for files to rename in the target folder and all its sub-folders? (y/N)")
        CheckAndRaiseExiting(isRecursiveSearch)
        if isRecursiveSearch in ["y", "Y", "yes", "Yes", "YES"]:
            return True
        if isRecursiveSearch in ["", "n", "N", "no", "No", "NO"]:
            return False
        print("Please enter y or n")


#### #### #### #### #### 
#### Main #### 
#### #### #### #### #### 
try:
    ## Variables initialization
    targetDirectory = GetTargetDirectory()
    alternativeDate = GetAlternativeDate()
    isRecursiveSearch = GetIsRecursiveSearch()
    ## Main
    command = ["./main.exe", "--dir", targetDirectory]
    if isinstance(alternativeDate, datetime.date):
        command.extend( ["--date", alternativeDate.isoformat() ] )
    if isRecursiveSearch is True:
        command.append("-r")
    subprocess.call(command)
except KeyboardInterrupt:
    pass
finally:
    ExitHandler()
