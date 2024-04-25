# REMINDER: Before running this script, activate the virtual environment with:
# source /Users/nico/Desktop/Google_Drive/MAGMA/PCA_ICA_April2024/IC_loci_GWAS_Catalog/HTML_table/venv/bin/activate


import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Load the CSV file into a DataFrame
data = pd.read_csv('/Users/nico/Desktop/Google_Drive/MAGMA/PCA_ICA_April2024/IC_loci_GWAS_Catalog/all_combined_traits.csv')

# Process the 'Component' column to keep only the "IC" part (e.g., "IC1", "IC2", etc.)
data['Component'] = data['Component'].str.extract('(IC\\d+)')

# Group the data by 'Component' and create a dictionary of traits, chromosomes, and positions
grouped_data = data.groupby('Component').apply(lambda x: x[['Chromosome', 'Position', 'Trait']].to_dict('records')).to_dict()

# Set up the environment for Jinja2
env = Environment(loader=FileSystemLoader(searchpath=''))
template = env.get_template('index.html')  # You need to create a template.html file

# Render the template with grouped data
html_content = template.render(components=grouped_data)

# Save the HTML content to a file
with open('components_traits.html', 'w') as file:
    file.write(html_content)

print('HTML file created successfully!')
