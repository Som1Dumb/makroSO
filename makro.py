import pandas as pd

# Load the Excel file
file_path = 'Zeszyt1.xlsx'
df = pd.read_excel(file_path)

# Open the output YAML file for writing
with open('rules_output.yaml', 'w') as file:
    # Iterate over each row of the dataframe and print formatted YAML-like structure
    for index, row in df.iterrows():
        # Construct rule name
        name = f'rule-{index}'
        file.write(f'- name: {name}\n')
        file.write('  priority: 100\n')
        file.write('  action: Allow\n')
        file.write('  rules:\n')
        
        # Set default values first
        source_cidrs = ["0.0.0.0/0"]
        destination_cidrs = ["0.0.0.0/0"]
        protocols = ["Any"]
        ports = ["ALL"]

        # Overwrite default values with actual data from the row if present
        if pd.notna(row['Source CIDR']):
            source_cidrs = [cidr.strip() for cidr in row['Source CIDR'].split(',')]
        
        if pd.notna(row['Destination CIDR/FQDN']):
            destination_cidrs = [row['Destination CIDR/FQDN'].strip()]
        
        if pd.notna(row['Protocol']):
            protocols = row['Protocol'].split(' / ')
        
        if pd.notna(row['Port']):
            port_value = str(row['Port'])
            ports = port_value.split(', ') if ',' in port_value else [port_value]
            ports = ['ALL' if port == '*' else port for port in ports]
        
        # Manually write out the rule details in YAML format
        file.write(f'    - name: rule-source-{index}\n')
        file.write(f'      protocols: {protocols}\n')
        file.write(f'      source_addresses: {source_cidrs}\n')
        file.write(f'      destination_addresses: {destination_cidrs}\n')
        file.write(f'      destination_ports: {ports}\n')

# Inform the user that the YAML file is created
print("YAML file has been generated successfully.")
