

# In main.py(发布前)--发布后，通过tests进行测试
from kangforecast.m1load import m1load
from kangforecast.m2process import m2process
from kangforecast.m3show import m3show

def main():
    print("Starting the process...\n")

    print("m1: Loading data from ../data/testdata.csv...")
    df = m1load("../data/testdata.csv")
    print("m1: Data loaded successfully.\n")
    
    print("m2: Processing data...")
    processed_df = m2process(df)
    print("m2: Data processing complete.\n")
    
    print("m3: Displaying processed data...")
    print("    ", end="\n")
    m3show(processed_df)
    print("    ", end="\n")
    print("m3: Data displayed successfully.\n")

    print("Process complete!")

if __name__ == "__main__":
    main()
