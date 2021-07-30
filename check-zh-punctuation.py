import sys, os, zhon.hanzi

# Check Chinese punctuation in English files.

def check_zh_punctuation(filename):

    lineNum = 0
    pos = []
    zh_punc = []
    acceptable_punc = ['–','—'] # em dash and en dash
    flag = 0

    with open(filename, 'r') as file:
        for line in file:

            count = 0
            lineNum += 1
            punc_inline = ""

            for char in line:

                if char in zhon.hanzi.punctuation and char not in acceptable_punc :
                    flag = 1
                    if count != 1:
                        pos.append(lineNum)
                    punc_inline += char
                    count = 1

            if punc_inline != "":
                zh_punc.append(punc_inline)

    if flag:
        print("\n" + filename + ": this file has Chinese punctuation in the following lines:\n")

        count = 0
        for lineNum in pos:
            print("Chinese punctuation: L" + str(lineNum) + " has " + zh_punc[count])
            count += 1

    return flag

if __name__ == "__main__":

    count = 0

    for filename in sys.argv[1:]:
        if os.path.isfile(filename):
            flag = check_zh_punctuation(filename)
            if flag:
                count+=1

    if count:
        print("\nThe above issues will ruin your article. Please convert these marks into English punctuation.")
        exit(1)