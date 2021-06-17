import re, sys, os, zhon.hanzi

# Check Chinese punctuation in English files.

def check_zh_punctuation(filename):

    lineNum = 0
    pos = []
    zh_punc = []
    flag = 0

    with open(filename, 'r') as file:
        for line in file:

            lineNum += 1

            for char in line:

                if char in zhon.hanzi.punctuation:
                    flag = 1
                    pos.append(lineNum)
                    zh_punc.append(char)
                    break

    if flag:
        print("\n" + filename + ": this file has Chinese punctuation in the following lines:\n")
        for punc in pos:
            print("Chinese punctuation: L" + str(punc) + "  " + char)
        print("\nPlease convert these marks into English punctuation.")

    return flag

if __name__ == "__main__":

    count = 0

    for filename in sys.argv[1:]:
        if os.path.isfile(filename):
            flag = check_zh_punctuation(filename)
            if flag:
                count+=1

    if count:
        print("\nThe above issues will ruin your article. Please fix them.")
        exit(1)