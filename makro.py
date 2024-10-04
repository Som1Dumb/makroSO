import pandas as pd

# Load the Excel file
file_path = 'Zeszyt1.xlsx'
df = pd.read_excel(file_path)

# Clean the data: forward fill missing values in the CIDR and Protocol columns
df[['Source CIDR', 'Destination CIDR/FQDN', 'Protocol']] = df[['Source CIDR', 'Destination CIDR/FQDN', 'Protocol']].ffill()

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
        
        # Extract values from the row
        source_cidrs = [cidr.strip() for cidr in row['Source CIDR'].split(',')]
        destination_cidrs = [row['Destination CIDR/FQDN'].strip()]
        protocols = row['Protocol'].split(' / ') if pd.notna(row['Protocol']) else ["Any"]
        port_value = str(row['Port']) if pd.notna(row['Port']) else '*'
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
