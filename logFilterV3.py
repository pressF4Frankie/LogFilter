# DESCRIPTION
# This python program can read a Portal for ArcGIS, ArcGIS Server, ArcGIS Server service, or ArcGIS Data Store log, filter out duplicate messages, and total each unique log instance.
# This does not work for Postgres logs, WebGISDR logs, or any other logs that do not use message tags to state the log messages. EX: <Msg...> (text here) </Msg>.

# USAGE
# You must include the file extension and provide a name for the output file. 
# Example: 
# Input: "C:\Users\<username>\Downloads\inputLog.log"
# Output: "C:\Users\<username>\Downlaods\outputLog.log"

# Last Updated: 1/13/2024

# Import regex
import re

# Define a function to prompt the user to input the log level they wish to skip. This user input is converted to uppercase since log levels are written in UPPERCASE characters.
def get_log_levels_to_skip():
    log_levels = input("Enter the log levels you want to skip (e.g., DEBUG,INFO,WARNING), separated by commas: ").upper()
    if not log_levels.strip():
        return [] # Return an empty list if the input is left blank by the user.
    return [level.strip() for level in log_levels.split(",")] # Removes leading and trailing whitespaces and the comma(s) used in the user input.

# Define a function to remove double quotes from the user's input.
def remove_quotes(string):
    return string.strip().strip('"')

# Define a function to extract and grab the text between '>' and '</'
def extract_text(filename, output_filename):
    try:
        with open(filename, 'r') as file:
            match_counts = {} 
            log_levels_to_skip = get_log_levels_to_skip()
            for line in file:
                if not any(level in line for level in log_levels_to_skip): # Skip lines containing specified log levels.
                    matches = re.findall(r'>(.*?)<\/', line)
                    for match in matches:
                        if match in match_counts: # match_counts keeps track of the count of each unique match.
                            match_counts[match] += 1 # Adds a 1 to the count if the match is already present in the dictionary.
                        else:
                            match_counts[match] = 1 # If not in the dictionary, count starts at 1. 
        # Write the unique matches to the output file.
        with open(output_filename, 'w') as output_file:
            for match, count in match_counts.items():
                output_file.write(f"Log Message: {match} [Count: {count}]\n") # Writes the unique match and it's count.
                print(f"{match}: {count}") # Print match (key value) and count (value). 
    except Exception as e:
        print(f"An error occurred: {e}")

# Prompt the user for the input and output file path.
input_filename = remove_quotes(input("Enter the path to the input text file: "))
output_filename = remove_quotes(input("Enter the path to save the output text file, including the name of the file and extension: "))

# Call the function with the path to your text file.
extract_text(input_filename, output_filename)
