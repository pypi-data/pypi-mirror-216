# In test_pytest_m1m2m3.py

import pandas as pd
from kangforecast.m1load import m1load
from kangforecast.m2process import m2process

def test_main_process():
    print("Starting the test process...\n")

    print("m1: Loading data from ./tests/testdata/test_pytest_m1m2m3_input.csv...")
    df = m1load("./testdata/test_pytest_m1m2m3_input.csv")
    print("m1: Test data loaded successfully.\n")
    
    print("m2: Processing test data...")
    processed_df = m2process(df)
    print("m2: Test data processing complete.\n")
    
    print("m3: Verifying the result...")
    print("    ", end="\n")

    # Load expected output
    expected_df = pd.read_csv("./testdata/test_pytest_m1m2m3_output.csv")
    expected_output = expected_df['value'].median()

    # Verify that the processed data matches the expected result

    assert processed_df == expected_output, \
        f'Expected {expected_output}, but got {processed_df}'

    
    print("m3: Verification successful.\n")

    print("Test process complete!\n")
