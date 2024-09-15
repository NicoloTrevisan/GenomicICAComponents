import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Load the CSV files
trait_data = pd.read_csv('/Users/nico/Desktop/Google_Drive/MAGMA/PCA_ICA_April2024/IC_loci_GWAS_Catalog/Summary_traits.csv')
gene_data = pd.read_csv('/Users/nico/Desktop/Google_Drive/MAGMA/PCA_ICA_April2024/IC_loci_GWAS_Catalog/all_genes_combined_MHC.txt', sep='\t')
magma_gene_data = pd.read_csv('/Users/nico/Desktop/Google_Drive/MAGMA/PCA_ICA_April2024/IC_loci_GWAS_Catalog/genes_MAGMA_all_components.csv')


# Clean up any leading/trailing spaces in the 'Component' column
magma_gene_data['Component'] = magma_gene_data['Component'].astype(str).str.strip()


# Optional: Filter out rows that don't match the 'IC<number>' pattern
magma_gene_data = magma_gene_data[magma_gene_data['Component'].str.match(r'IC\d+')]

# Ensure 'Component' columns are strings and extract only the "IC" part ("IC1", "IC2", etc.)
trait_data['Component'] = trait_data['Component'].astype(str).str.extract(r'(IC\d+)', expand=False).str.strip()
gene_data['Component'] = gene_data['Component'].astype(str).str.extract(r'(IC\d+)', expand=False).str.strip()

# Remove duplicates within each DataFrame
trait_data = trait_data.drop_duplicates(subset=['Component', 'Chromosome', 'Position', 'Trait'])
gene_data = gene_data.drop_duplicates(subset=['Component', 'ensg'])
magma_gene_data = magma_gene_data.drop_duplicates(subset=['Component', 'GENE'])

# Group the data separately for traits, genes, and MAGMA genes
grouped_trait_data = trait_data.groupby('Component')[['Chromosome', 'Position', 'Trait']].apply(lambda x: x.to_dict('records')).to_dict()
grouped_gene_data = gene_data.groupby('Component')[['ensg', 'symbol', 'chr', 'start', 'end', 'strand', 'type', 'entrezID', 'HUGO', 'pLI', 'ncRVIS']].apply(lambda x: x.to_dict('records')).to_dict()
grouped_magma_gene_data = magma_gene_data.groupby('Component')[['GENE', 'CHR', 'START', 'STOP', 'NSNPS', 'NPARAM', 'N', 'ZSTAT', 'P']].apply(lambda x: x.to_dict('records')).to_dict()


# Combine trait, gene, and MAGMA gene data into a single dictionary
components = {}
for component in set(grouped_trait_data.keys()).union(grouped_gene_data.keys()).union(grouped_magma_gene_data.keys()):
    components[component] = {
        'Traits': grouped_trait_data.get(component, []),
        'Genes': grouped_gene_data.get(component, []),
        'MagmaGenes': grouped_magma_gene_data.get(component, [])  # Add the MAGMA genes here
    }

# Sort components to ensure they are in numerical order
sorted_components = dict(sorted(components.items(), key=lambda item: int(item[0][2:])))

# Environment for Jinja2
env = Environment(loader=FileSystemLoader(searchpath=''))
template = env.get_template('template.html')

# Passing magma genes to the template html
html_content = template.render(components=sorted_components, magma_genes=grouped_magma_gene_data)

# Save the HTML content to a file
with open('index.html', 'w') as file:
    file.write(html_content)

print('HTML file created successfully!')