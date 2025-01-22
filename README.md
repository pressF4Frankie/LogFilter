# LogFilter
Python log filter for ArcGIS Enterprise 10.9.1 and up. 

## Features
- Filter on log levels
- Removes duplicate log entries
- Counts each instance of a log message
- Record first and last timestamp of a log message

## Requirements
- Python 3.7 and above

## Usage
1. Run the script.
   ```sh
   python EnterpriseLogFilter.py
   ```
2. Enter the path to the directory containing the '.log' files or specify an individual '.log' file.
   ```sh
   Diretory EX: "C:\arcgisportal\logs\<machine>\portal"
   OR
   File Name EX: "C:\arcgisportal\logs\<machine>\portal\file.log"
   ```
3. Enter a path to save the output file to, including the name of the file and extension.
   ```sh
   Output EX: "C:\Users\<user>\Desktop\outputfile.log"
4. Enter the log levels you would like to skip.
   ```sh
   EX: DEBUG, VERBOSE, INFO
   If you wish to include all levels in the output file, then hit Enter.
   ```
5. Run. You should see an brief output of the logs analyzed, and a new output file where the output file path was entered. 
