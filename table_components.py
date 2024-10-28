import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Load the CSV files
trait_data = pd.read_csv('/Users/nico/Desktop/Google_Drive/MAGMA/PCA_ICA_April2024/IC_loci_GWAS_Catalog/Summary_traits.csv')
gene_data = pd.read_csv('/Users/nico/Desktop/Google_Drive/MAGMA/PCA_ICA_April2024/IC_loci_GWAS_Catalog/all_genes_combined_MHC.txt', sep='\t')
magma_gene_data = pd.read_csv(
    '/Users/nico/Desktop/Google_Drive/MAGMA/PCA_ICA_April2024/IC_loci_GWAS_Catalog/genes_MAGMA_with_symbols.csv', sep=';', decimal=',')
new_data = pd.read_csv('/Users/nico/Desktop/Google_Drive/MAGMA/PCA_ICA_April2024/IC_loci_GWAS_Catalog/combined_filtered_padj_below_0_1.txt', sep='\t')

# Load component descriptions from the tab-separated text file
descriptions_file_path = '/Users/nico/Desktop/Google_Drive/MAGMA/PCA_ICA_April2024/IC_loci_GWAS_Catalog/COMPONENTS_DESCRIPTIONS.txt'
descriptions_df = pd.read_csv(descriptions_file_path, sep='\t', encoding='latin-1')

# Create a dictionary for descriptions
component_descriptions = descriptions_df.set_index('Components')[['Title', 'Text']].to_dict('index')

# Clean up any leading/trailing spaces in the 'Component' column
magma_gene_data['Component'] = magma_gene_data['Component'].astype(str).str.strip()
new_data['Component'] = new_data['Component'].astype(str).str.strip()

# Optional: Filter out rows that don't match the 'IC<number>' pattern
magma_gene_data = magma_gene_data[magma_gene_data['Component'].str.match(r'IC\d+')]
new_data = new_data[new_data['Component'].str.match(r'IC\d+')]

# Ensure 'Component' columns are strings and extract only the "IC" part ("IC1", "IC2", etc.)
trait_data['Component'] = trait_data['Component'].astype(str).str.extract(r'(IC\d+)', expand=False).str.strip()
gene_data['Component'] = gene_data['Component'].astype(str).str.extract(r'(IC\d+)', expand=False).str.strip()

# Remove duplicates within each DataFrame
trait_data = trait_data.drop_duplicates(subset=['Component', 'Chromosome', 'Position', 'Trait'])
gene_data = gene_data.drop_duplicates(subset=['Component', 'ensg'])
magma_gene_data = magma_gene_data.drop_duplicates(subset=['Component', 'GENE'])
new_data = new_data.drop_duplicates()

# Clean numeric columns in new_data (Removed 'P' from the list)
numeric_cols = ['NGENES', 'BETA', 'BETA_STD', 'SE', 'P_FDR']
for col in numeric_cols:
    new_data[col] = new_data[col].astype(str).str.replace(',', '.')
    new_data[col] = pd.to_numeric(new_data[col], errors='coerce')

# Group the data separately for traits, genes, MAGMA genes, and the new data
grouped_trait_data = trait_data.groupby('Component')[['Chromosome', 'Position', 'Trait']].apply(lambda x: x.to_dict('records')).to_dict()
grouped_gene_data = gene_data.groupby('Component')[['ensg', 'symbol', 'chr', 'start', 'end', 'strand', 'type', 'entrezID', 'HUGO', 'pLI', 'ncRVIS']].apply(lambda x: x.to_dict('records')).to_dict()
grouped_magma_gene_data = magma_gene_data.groupby('Component')[['GENE', 'GENE SYMBOL', 'CHR', 'START', 'STOP', 'NSNPS', 'NPARAM', 'N', 'ZSTAT', 'P']].apply(lambda x: x.to_dict('records')).to_dict()
grouped_new_data = new_data.groupby('Component')[['FULL_NAME', 'NGENES', 'BETA', 'BETA_STD', 'SE', 'P_FDR']].apply(lambda x: x.to_dict('records')).to_dict()

# Combine all data into a single dictionary
components = {}
all_components = set().union(
    grouped_trait_data.keys(), grouped_gene_data.keys(), 
    grouped_magma_gene_data.keys(), grouped_new_data.keys(), 
    component_descriptions.keys()
)

for component in all_components:
    descriptions = component_descriptions.get(component, {})
    components[component] = {
        'Traits': grouped_trait_data.get(component, []),
        'Genes': grouped_gene_data.get(component, []),
        'MagmaGenes': grouped_magma_gene_data.get(component, []),
        'NewData': grouped_new_data.get(component, []),
        'Description': descriptions.get('Text', "Description not available."),
        'Title': descriptions.get('Title', component)  # Fallback to component name if Title is missing
    }


# Sort components to ensure they are in numerical order
sorted_components = dict(sorted(components.items(), key=lambda item: int(item[0][2:])))

# Environment for Jinja2
env = Environment(loader=FileSystemLoader(searchpath=''))
template = env.get_template('template.html')

# Render the template with the combined data
html_content = template.render(components=sorted_components)

# Save the HTML content to a file
with open('index.html', 'w') as file:
    file.write(html_content)

print('HTML file created successfully!')