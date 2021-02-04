# pingcap-docs-checks

Some CI check scripts for [PingCAP documentation](https://github.com/pingcap/docs).

## How to download scripts in the CI environment

1. View the script file you want to download and click the `raw` button on the upper right.

2. Copy the link. For example: https://raw.githubusercontent.com/CharLotteiu/pingcap-docs-checks/main/check-conflicts.py

3. Use the `wget` command to download the script. For example: 

  ```
  wget https://raw.githubusercontent.com/CharLotteiu/pingcap-docs-checks/main/check-conflicts.py
  ```

4. Use the `python3` command to run the file. For example:

  ```
  python3 check-conflicts.py $(git diff-tree --name-only --no-commit-id -r upstream/master..HEAD -- '*.md' ':(exclude).github/*')
  ```
