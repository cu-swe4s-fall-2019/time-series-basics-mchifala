test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_overall python data_import.py /smallData functional_test cgm
assert_no_stderr
assert_exit_code 0

run test_overall python pandas_import.py cgm_small.csv smallData
assert_no_stderr
assert_exit_code 0