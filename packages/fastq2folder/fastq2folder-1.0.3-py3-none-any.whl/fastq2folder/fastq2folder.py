#!/usr/bin/env python
# coding: utf-8

# In[8]:


import os
import gzip
import shutil
import pandas as pd
from Bio import SeqIO
from scipy import stats
import numpy as np

#Create a new folder for the unzipped and binned files to go
#base_dir = r"C:\Users\egar1\OneDrive\Desktop"
base_dir = input('Enter path to source directory: ')
if os.path.isdir(base_dir):
    print('The directory exists')
else:
    print('The directory does not exist.  Make sure you select the parent directory, and omit outer quotes and the final forward slash.')
file_dir = 'fastq_pass'
source_dir = os.path.join(base_dir, file_dir)
new_dir = 'fastq_bins'

if os.path.isdir(source_dir):
    print('Found the fastq_pass folder')
else:
    print('The fastq_pass folder does not exist in the source directory.') 

destination_dir = os.path.join(base_dir, new_dir)
if not os.path.isdir(destination_dir):
    os.mkdir(destination_dir)
    print('folder created')
    
for foldername, subfolders, filenames in os.walk(source_dir):
    #print('foldername', foldername)
    #print('subfolders', subfolders)
    #print('filenames', filenames)
    for filename in filenames:
        shutil.copy(os.path.join(foldername, filename), destination_dir)

# Create a dictionary to store the barcode folders
barcode_folders = {}

def decompress_gz_files_in_dir(directory):
    for item in os.listdir(directory):
        if item.endswith('.gz'):
            print('decompressing ', item)
            file_name = os.path.join(directory, item)
            with gzip.open(file_name, 'rb') as f_in:
                with open(file_name[:-3], 'wb') as f_out:  # Remove the '.gz' from the output file name
                    shutil.copyfileobj(f_in, f_out)
    print('decompression complete')

# Call the function and provide the directory you want to decompress .gz files in
decompress_gz_files_in_dir(destination_dir)


# In[9]:


print('calculating read lengths')
def get_stats(fastq_file):
    cutoff_value = 1000 #do not include values below 1000
    lengths = []
    filtered = []
    for record in SeqIO.parse(fastq_file, "fastq"):
        lengths.append(len(record.seq))
    for n in lengths:
        if n > cutoff_value:
            filtered.append(n)
    if len(filtered)>1:
        return filtered, np.mean(filtered), np.median(filtered), stats.mode(filtered)[0][0]
    else:
        print('File ', fastq_file, 'does not have enough long reads for statistical analysis')
        return None
        
results = []

# define the bins and their labels
bins = [0, 3000, 6000, 9000, 12000, 15000, 18000, np.inf]
labels = ['bin2000', 'bin5000', 'bin8000', 'bin11000', 'bin14000', 'bin17000', 'bin20000']

#INPUT is a folder of fastq files
for file in os.listdir(destination_dir):
    if not file.endswith(".fastq"):
        continue
    print('filename', file)
    fastq_file = os.path.join(destination_dir, file)
    
    stats_result = get_stats(fastq_file)
    if stats_result is not None:
        filtered, mean, median, mode = get_stats(fastq_file)

        bin_labels = pd.cut(filtered, bins=bins, labels=labels)

        # Identify the most frequent bin for this file
        common_bin = pd.DataFrame(bin_labels).mode().values[0][0]

        results.append({
            "Barcode": file,
            "Mode": mode,
            "Bin": common_bin
        })

        new_dir = os.path.join(destination_dir, common_bin)
        os.makedirs(new_dir, exist_ok=True)

        shutil.copy2(fastq_file, os.path.join(new_dir, file))

df = pd.DataFrame(results)
print('Binning complete')
#df = df.sort_values("Mode", ascending=False)
#df.to_csv("output.csv", index=False)
print(df)


# In[33]:


import matplotlib.backends.backend_pdf
import matplotlib.gridspec as gridspec
from matplotlib import pyplot as plt

def plot_histograms(directory):
    # Create a new PDF file
    output_file = destination_dir+"\\read_length_histograms.pdf"
    print(output_file)
    pdf = matplotlib.backends.backend_pdf.PdfPages(output_file)

    file_list = [file for file in os.listdir(directory) if file.endswith(".fastq")]
    num_pages = len(file_list) // 8 + (len(file_list) % 8 > 0)

    for page in range(num_pages):
        # Create a new figure for each page
        fig = plt.figure(figsize=(20, 28))

        gs = gridspec.GridSpec(4, 2)
        
        # Adjust vertical spacing
        gs.update(hspace=0.5) # Change the value as needed for more or less spacing

        for i in range(min(8, len(file_list) - page * 8)):
            file = file_list[page * 8 + i]
            fastq_file = os.path.join(directory, file)
            
            # Extract lengths of the sequences in the FASTQ file
            lengths = [len(record.seq) for record in SeqIO.parse(fastq_file, "fastq")]

            # Calculate the mode
            mode = stats.mode(lengths)[0][0]

            # Count the number of reads
            reads = len(lengths)

            ax = fig.add_subplot(gs[i // 2, i % 2])

            # Plot histogram
            sns.histplot(lengths, bins=100, kde=False, color='skyblue', ax=ax)

            # Add a vertical line for the mode
            ax.axvline(mode, color='black', linestyle='dashed', linewidth=2, alpha=0.5)
            
            # Annotate the mode
            ax.text(0.97, 0.94, f'Estimated plasmid size: {mode}bp', fontsize=14, horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, color='black')

            # Annotate the number of reads
            ax.text(0.97, 0.87, f'Reads: {reads}', fontsize=14, horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, color='black')

            # Get the barcode from the file name
            barcode = file.split('pass_')[-1]
            barcode = barcode[:-26]

            # Set the title to the barcode
            ax.set_title(barcode, fontsize=16)
            
            # Label the axes
            ax.set_xlabel('Sequence Length', fontsize=14)
            ax.set_ylabel('Count', fontsize=14)
        
        # Add the figure to the PDF file
        pdf.savefig(fig)

    # Close the PDF file
    pdf.close()
plot_histograms(destination_dir)

