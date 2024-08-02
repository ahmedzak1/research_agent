import json
import csv

def convert_raw_json_to_csv(raw_input, output_file='research_tools.csv'):
    """
    Converts raw JSON input to a CSV file.
    
    Parameters:
    raw_input (str): The raw JSON string input.
    output_file (str): The name of the output CSV file (default is 'research_tools.csv').
    """
    try:
        # Remove backticks and leading/trailing whitespace
        raw_json = raw_input.strip().strip('`')
        
        # Remove leading '\n' if present
        if raw_json.startswith('\n'):
            raw_json = raw_json[1:]
        
        # Parse the JSON string
        data = json.loads(raw_json)
        
        # Prepare CSV output
        fieldnames = ['name', 'description', 'functionality']
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data rows
            for item in data:
                writer.writerow(item)
        
        print(f"CSV file '{output_file}' has been created successfully.")
    
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")
        print("First 100 characters of input:")
        print(raw_input[:100])
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("First 100 characters of input:")
        print(raw_input[:100])

