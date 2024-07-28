# Py Test Framework Documentation
## Py test using cmd
Run all of test cases are present inside the package step by step
```commandline
py.test
```
Give more information about test case like cache dir, root dir, etc.
```commandline
py.test -v
```
Show the console log
```commandline
py.test -v -s
```
Run only specific file
```commandline
py.test [file_name] -v -s
```
Run the test case with the name matched with char
```commandline
py.test -k [matched_char]
```
run all test case in current package
```commandline
pytest -rA -v
```
Run all test case in package 1 and package 2
```commandline
pytest [package 1] [package 2] -rA -v
```
Run all test case in specific file testcases
```commandline
pytest [path_of_file] -rA -v
```
Run specific test case in the file testcases
```commandline
pytest [path_of_file]::[testcase] -rA -v
```
Run specific test case that match with keyword used in @pytest.mark.[keyword]
```commandline
pytest -m "[keyword]" -rA -v
```