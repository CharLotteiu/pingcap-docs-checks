import re, sys, os

# Check manual line break within a paragraph.
def check_manual_break(filename):

    two_lines = []
    metadata = 0
    toggle = 0
    ctoggle = 0
    lineNum = 0
    mark = 0

    with open(filename,'r') as file:
        for line in file:

            lineNum += 1

            # Count the number of '---' to skip metadata.
            if metadata < 2 :
                if re.match(r'(\s|\t)*(-){3}', line):
                    metadata += 1
                continue
            else:
                # Skip tables and notes.
                if re.match(r'(\s|\t)*(\||>)\s*\w*',line):
                    continue

                # Skip html tags and markdownlint tags.
                if re.match(r'(\s|\t)*((<\/*(.*)>)|<!--|-->)\s*\w*',line):
                    if re.match(r'(\s|\t)*(<pre><code>|<table>)',line):
                        ctoggle = 1
                    elif re.match(r'(\s|\t)*(<\/code><\/pre>|<\/table>)',line):
                        ctoggle = 0
                    else:
                        continue

                # Skip image links.
                if re.match(r'(\s|\t)*!\[.+\](\(.+\)|: [a-zA-z]+://[^\s]*)',line):
                    continue

                # Set a toggle to skip code blocks.
                if re.match(r'(\s|\t)*`{3}', line):
                    toggle = abs(1-toggle)

                if toggle == 1 or ctoggle == 1:
                    continue
                else:
                    # Keep a record of the current line and the former line.
                    if len(two_lines)<1:
                        two_lines.append(line)
                        continue
                    elif len(two_lines) == 1:
                        two_lines.append(line)
                    else:
                        two_lines.append(line)
                        two_lines.pop(0)

                    # Compare if there is a manual line break between the two lines.
                    if re.match(r'(\s|\t)*\n', two_lines[0]) or re.match(r'(\s|\t)*\n', two_lines[1]):
                        continue
                    else:
                        if re.match(r'(\s|\t)*(-|\+|(\d+|\w{1})\.|\*)\s*\w*',two_lines[0]) and re.match(r'(\s|\t)*(-|\+|\d+|\w{1}\.|\*)\s*\w*',two_lines[1]):
                            continue

                        if mark == 0:
                            print("\n" + filename + ": this file has manual line breaks in the following lines:\n")
                            mark = 1

                        print("MANUAL LINE BREAKS: L" + str(lineNum))
    return mark


if __name__ == "__main__":

    count = 0

    for filename in sys.argv[1:]:
        if os.path.isfile(filename):
            mark = check_manual_break(filename)
            if mark :
                count+=1

    if count:
        print("\nThe above issues will cause website build failure. Please fix them.")
        exit(1)