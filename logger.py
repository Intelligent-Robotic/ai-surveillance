import csv
import datetime
import os


def log_data(file_path, data):
    # Check if the file already exists
    file_exists = os.path.isfile(file_path)
    
    # Open the file in append mode
    with open(file_path, 'a') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)
        
        # Write a header row if the file doesn't exist
        if not file_exists:
            csv_writer.writerow(['timestamp','type','info'])
        
        # Write the data to the CSV file
        csv_writer.writerow([datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), data['type'],data['info']])


