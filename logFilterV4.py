# DESCRIPTION
# This python program can read a Portal for ArcGIS, ArcGIS Server, ArcGIS Server service, or ArcGIS Data Store log, filter out duplicate messages, and total each unique log instance.
# This only works for .log files or directories that contain .log files that use the XML Elements: Time and Type

# USAGE
# Individual log file: You must include the .file extension and provide a name for the output file. 
# Example: 
# Input: "C:\arcgisportal\logs\<machine>\portal\file.log"
# Output: "C:\Users\<user>\Desktop\outputfile.log"

# Folder directory: You must provide the path to the directory and a name for the output file.
# Example:
# Input: "C:\arcgisportal\logs\<machine>\portal"
# Output: "C:\Users\<user>\Desktop\outputfile.log"

# Last Updated: 1/15/2025

import os
import xml.etree.ElementTree as ET

# Define a function to prompt the user to input the log level they wish to skip. This user input is converted to uppercase since log levels are written in UPPERCASE characters.
def get_log_levels_to_skip():
    log_levels = input("Enter the log levels you want to skip (e.g., DEBUG,INFO,WARNING), separated by commas (leave blank to skip none): ")
    if not log_levels.strip():
        return []  # Return an empty list if input is blank.
    return [level.strip().upper() for level in log_levels.split(",")] # Removes whitespace and commas in user input. 

# Define a function to remove double quotes from the user's input.
def remove_quotes(string):
    return string.strip().strip('"')

# Define a function to extract log message and timestamps from the matching XML elements.
def extract_text_from_file(filename, match_counts, log_levels_to_skip):
    try:
        if not filename.endswith(".log"):
            print(f"Skipping file {filename} as it does not end with .log")
            return
        with open(filename, 'r') as file:
            for line in file:
                try:
                    element = ET.fromstring(line)
                    timestamp = element.get('time')
                    if any(level in element.get('type').upper() for level in log_levels_to_skip): # Check log level.
                        continue
                    # Extract the log message content.
                    log_message = element.text.strip()
                    if log_message in match_counts:
                        count, first_timestamp, _ = match_counts[log_message] # Underscore used as a temporary placeholder for the last occurence timestamp.
                        match_counts[log_message] = (count + 1, first_timestamp, timestamp) # Update count and last occurrence timestamp.
                    else:
                        match_counts[log_message] = (1, timestamp, timestamp) # If not in dictionary, then initialize count and timestamps.
                except ET.ParseError:
                    continue
    except Exception as e:
        print(f"An error occurred while processing {filename}: {e}") # Skip lines that are not valid XML.

def extract_text(input_path, output_path):
    try:
        match_counts = {} # Dictionary to keep track of unique matches, counts, and timestamps.
        log_levels_to_skip = get_log_levels_to_skip()
        if os.path.isdir(input_path):
            for filename in os.listdir(input_path): # Check if the input_path is a directory. 
                if filename.endswith(".log"):
                    extract_text_from_file(os.path.join(input_path, filename), match_counts, log_levels_to_skip)
        else:
            if input_path.endswith(".log"): # Check if the input_path ends with .log.
                extract_text_from_file(input_path, match_counts, log_levels_to_skip)
            else:
                print(f"Skipping file {input_path} as it does not end with .log")
        # Write the unique matches, their counts, and timestamps to the output file. 
        if match_counts:
            with open(output_path, 'w') as output_file:
                for log_message, (count, first_timestamp, last_timestamp) in match_counts.items():
                    output_file.write(f"Log Message: {log_message} [Count: {count}]\nFirst Occurrence: {first_timestamp} Last Occurrence: {last_timestamp}\n\n")
                    print(f"{log_message}: {count}")
        else:
            print("No log files were processed or no matching log messages were found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Prompt the user for the directory and output file path, removing any double quotes
input_path = remove_quotes(input("Enter the path to the directory containing the log files or an individual log file: "))
output_path = remove_quotes(input("Enter the path to save the output file, including the name of the file and extension: "))

# Call the function with the directory and output file path
extract_text(input_path, output_path)
