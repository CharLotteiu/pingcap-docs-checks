import re, sys, os

# Check control characters.
def check_control_char(filename):

    lineNum = 0
    pos = []
    flag = 0

    with open(filename,'r') as file:
        for line in file:

            lineNum += 1

            if re.search(r'[\b]', line):
                pos.append(lineNum)
                flag = 1

    if flag:
        print("\n" + filename + ": this file has control characters in the following lines:\n")
        for cc in pos:
            print("CONTROL CHARACTERS: L" + str(cc))
        print("\nPlease delete these control characters.")

    return flag

if __name__ == "__main__":

    count = 0

    for filename in sys.argv[1:]:
        if os.path.isfile(filename):
            flag = check_control_char(filename)
            if flag:
                count+=1

    if count:
        print("\nThe above issues will cause website build failure. Please fix them.")
        exit(1)