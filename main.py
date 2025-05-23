from src.parser import GrammarParser

# -------------------------------------------------------------------------------------------------

# Ask for input file
while True:
    file_path = input("Enter the path to the file to parse: ")
    try:
        with open(file_path, "r") as file:
            text = file.read()
        break
    except FileNotFoundError:
        print("Invalid path. Try again.")

parser = GrammarParser()
if parser.parse(text):
    print("Input accepted by FSA.")
else:
    print("Input rejected.")
