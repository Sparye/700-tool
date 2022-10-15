# Import libraries
import glob
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import argparse

#Overfitting threshold percentage
acc_threshold_def = 0.05
loss_threshold_def = 0.1

parser = argparse.ArgumentParser()
parser.add_argument('--acc_thres', nargs='?', const=acc_threshold_def, type=float, default=acc_threshold_def)
parser.add_argument('--loss_thres', nargs='?', const=loss_threshold_def, type=float, default=loss_threshold_def)
args = parser.parse_args()

acc_threshold = args.acc_thres
loss_threshold = args.loss_thres

# Get CSV files list from a folder
path = os.getcwd()
csv_files = glob.glob(path + "/csvs/*.csv")

# Read each CSV file into DataFrame
# This creates a list of dataframes
df_list = (pd.read_csv(file) for file in csv_files)

# Concatenate all DataFrames
big_df   = pd.concat(df_list, ignore_index=True)

big_df = big_df.reset_index()

# plt.gca().ticklabel_format(axis='both', style='sci', useOffset=False)

# figure, axis = plt.subplots(2,4, figsize =(16, 9))
figure, axis = plt.subplot_mosaic(
    """
    ABC
    ADE
    """,
    constrained_layout=True, figsize =(16, 9))

big_df['acc_diff_avg'] = ''
big_df['loss_diff_avg'] = ''

table_data = {'Attribute \ Model name': ['Attribute \ Model name'],
        'Overfitting epoch by ACC': ['Overfitting epoch by ACC'],
        'Overfitting epoch by LOSS': ['Overfitting epoch by LOSS'],
        'Training time': ['Training time'],
        'Training time per param' : ['Training time per param']}
table_df = pd.DataFrame(table_data)

new_file_name = ''

for index, row in big_df.iterrows():
    if row['crash'] == '-':
        new_file_name = new_file_name + row['model_name'] + " vs "

        acc_diff = list()
        row['accuracy_history'] = list(np.float_(row['accuracy_history'][1:-1].split(', ')))
        row['validation_accuracy'] = list(np.float_(row['validation_accuracy'][1:-1].split(', ')))

        loss_diff = list()
        row['loss_history'] = list(np.float_(row['loss_history'][1:-1].split(', ')))
        row['val_loss_history'] = list(np.float_(row['val_loss_history'][1:-1].split(', ')))
        i = 0

        for train_acc, val_acc, train_loss, val_loss_history in zip(row['accuracy_history'], row['validation_accuracy'], row['loss_history'], row['val_loss_history']):
            i += 1
            acc_diff.append(abs(float(train_acc)-float(val_acc)))

            loss_diff.append(abs(float(train_loss)-float(val_loss_history)))
            
        acc_diff_avg = sum(acc_diff) / len(acc_diff)
        loss_diff_avg = sum(loss_diff) / len(loss_diff)

        acc_diff_rev = list(reversed(acc_diff))
        acc_diff_fill = list()
        loss_diff_rev = list(reversed(loss_diff))
        loss_diff_fill = list()

        acc_of_epoch = len(acc_diff)
        loss_of_epoch = len(loss_diff)
        acc_avg = max(acc_diff_rev)
        loss_avg = max(loss_diff_rev)

        of_flag = False
        for idx, acc in enumerate(acc_diff_rev):
            acc_diff_fill.append(acc)
            if (acc_avg >= sum(acc_diff_fill) / len(acc_diff_fill)) & (acc >= acc_threshold):
                acc_of_epoch = len(acc_diff) - idx
                of_flag = True
            acc_avg = sum(acc_diff_fill) / len(acc_diff_fill)

        if not of_flag:
            acc_of_epoch = '-'

        of_flag = False
        for idx, loss in enumerate(loss_diff_rev):
            loss_diff_fill.append(loss)
            if (loss_avg >= sum(loss_diff_fill) / len(loss_diff_fill)) & (loss >= loss_threshold):
                loss_of_epoch = len(loss_diff) - idx
                of_flag = True
            loss_avg = sum(loss_diff_fill) / len(loss_diff_fill)

        if not of_flag:
            loss_of_epoch = '-'

        time_per_param = np.float_(row['train_time'])/np.float_(row['num_model_params'])
        new_table_data = {'Attribute \ Model name': row['model_name'],
            'Overfitting epoch by ACC': acc_of_epoch,
            'Overfitting epoch by LOSS': loss_of_epoch,
            'Training time': row['train_time'],
            'Training time per param' : time_per_param}
        table_df = table_df.append(new_table_data, ignore_index=True)
        
        big_df.at[index, 'acc_diff_avg'] = acc_diff_avg
        big_df.at[index, 'loss_diff_avg'] = loss_diff_avg

        epoch_list = list(range(1, len(acc_diff)+1))
        axis['B'].set_title('Accuracy difference')
        axis['B'].plot(epoch_list, list(map(abs, acc_diff)), label = row['model_name'])
        axis['B'].legend()
        axis['C'].set_title('Loss difference')
        axis['C'].plot(epoch_list, list(map(abs, loss_diff)), label = row['model_name'])
        axis['C'].legend()
        axis['D'].set_title('Accuracy history')
        axis['D'].plot(epoch_list, row['accuracy_history'], label = row['model_name'])
        axis['D'].legend()
        axis['E'].set_title('Loss history')
        axis['E'].plot(epoch_list, row['loss_history'], label = row['model_name'])
        axis['E'].legend()

    else:
        new_table_data = {'Attribute \ Model name': row['model_name'],
            'Overfitting epoch by ACC': 'N/A',
            'Overfitting epoch by LOSS': 'N/A',
            'Training time': 'N/A',
            'Training time per param' : 'N/A'}
        table_df = table_df.append(new_table_data, ignore_index=True)

new_file_name = new_file_name[:len(new_file_name) - 4]

table_df = table_df.T

table = axis['A'].table(cellText=table_df.values, loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.5, 5)
axis['A'].axis('off')


big_df['time_per_param'] = time_per_param

output_df = big_df[['model_name', 'accuracy_history', 'validation_accuracy', 'acc_diff_avg', 'loss_diff_avg', 'train_time', 'num_model_params', 'time_per_param', 'eval_time', 'crash']].copy()

output_df.to_csv(new_file_name+'.csv', index=False)
  
# function to show the plot
plt.show()