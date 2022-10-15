# Setup Instructions
## Requirements
- Python 3.9.12
- Tensorflow 2.9.1
- Pandas 1.4.3
- Numpy 1.23.1
- Astor 0.8.1

## Step 1
Navigate to ADDB_automation
Put one deep learning program for comparison into df-testing/v1.
Put the other program for comparison into df-testing/v2.

## Step 2
Terminal change directory to `/ADDB_automation`
Run `ADDB_automation.py`

## Step 3
Enter `df-testing` as the directory in terminal when it prompts.

## Step 4
ADDB_automation would produce a folder named `df-testing_modified`

## Step 5
Run the deep learning programs in `df-testing_modified/v1` and `df-testing_modified/v2`

## Step 6
Move the generated csv files into `ADDB_testing/csvs` directory

## Step 7
Terminal change directory to `/ADDB_testing`
Run `ADDB_testing.py`

## Step 8 (Optional)
When running ADDB_testing.py, you can set a different threshold to overwrite the default.
specify the difference for accuracy(x%) and loss(y) for overfitting. 
run `python3 ADD_testing.py --acc_thres x --loss_thres y`


