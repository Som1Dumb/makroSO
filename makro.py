import pandas as pd
import yaml

# Load the Excel file
file_path = 'Zeszyt1.xlsx'
df = pd.read_excel(file_path)

# Clean the data: forward fill missing values in the CIDR and Protocol columns
df[['Source CIDR', 'Destination CIDR/FQDN', 'Protocol']] = df[['Source CIDR', 'Destination CIDR/FQDN', 'Protocol']].ffill()

# Function to format each row into YAML-like structure
def row_to_rule(row, index):
    # Split source and destination addresses into lists and ensure they are formatted correctly
    source_cidrs = [cidr.strip() for cidr in row['Source CIDR'].split(',')]
    destination_cidrs = [row['Destination CIDR/FQDN'].strip()]
    
    # Handle protocols, defaulting to ["Any"] if empty
    protocols = row['Protocol'].split(' / ') if pd.notna(row['Protocol']) else ["Any"]
    
    # Convert port to string, handle potential NaN values and ensure it's a list
    port_value = str(row['Port']) if pd.notna(row['Port']) else '*'
    ports = port_value.split(', ') if ',' in port_value else [port_value]
    
    # Replace "*" with "ALL" in ports
    ports = ['ALL' if port == '*' else port for port in ports]
    
    # Ensure all fields are lists in the output
    return {
        'name': f'rule-{index}',
        'priority': 100,
        'action': 'Allow',
        'rules': [
            {
                'name': f'rule-source-{index}',
                'protocols': protocols,  # Always a list
                'source_addresses': source_cidrs,  # Always a list
                'destination_addresses': destination_cidrs,  # Always a list
                'destination_ports': ports  # Always a list
            }
        ]
    }

# Convert each row of the dataframe into a rule
rules = [row_to_rule(row, index) for index, row in df.iterrows()]

# Customizing YAML dumper to force inline lists
class InlineListDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(InlineListDumper, self).increase_indent(flow=True, indentless=False)

# Save the YAML output to a file with forced inline list formatting
with open('rules_output.yaml', 'w') as yaml_file:
    yaml.dump(rules, yaml_file, Dumper=InlineListDumper, default_flow_style=False)

# Displaying the output in inline list format
yaml_output = yaml.dump(rules, Dumper=InlineListDumper, default_flow_style=False)
print(yaml_output)
