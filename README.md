# GenomicICAComponents
 
1. Introduction to GENOMICA

Independent Component Analysis (ICA) is an advanced unsupervised decomposition method used to extract independent sources from complex data. In this study, ICA was applied to high-dimensional genomic data from GWAS summary statistics to identify hidden, interpretable genomic factors influencing brain structure and function. Unlike Principal Component Analysis (PCA), ICA is particularly suited for separating mixed signals into their independent components, providing deeper insights into genetic influences across multiple traits.

2. Data Preparation for ICA

	•	The analysis utilized GWAS summary statistics from the UK Biobank’s Oxford Brain Imaging Genetics (BIG-40) database.
	•	Two non-overlapping samples were used: a discovery set with 22,138 participants and a replication set with 11,086 participants.
	•	2240 imaging-derived phenotypes (IDPs) were included, focusing on heritable measures from various MRI modalities.

3. GENOMICA Methodology

3.1 Multivariate Decomposition with MELODIC

	•	Algorithm: Multivariate Exploratory Linear Optimized Decomposition into Independent Components (MELODIC), a probabilistic ICA algorithm, was used to decompose the data.
	•	Data Structure: The analysis used matrices of SNP effect sizes across all IDPs, creating a genome-wide matrix of imaging and genetic data.
	•	Component Extraction:
	•	MELODIC starts by applying PCA to identify principal components, which are then rotated to maximize independence, producing independent components (ICs).
	•	ICA decomposes the data by focusing on non-Gaussianity and maximizing independence between components, even allowing non-orthogonal relationships.

3.2 Dimensionality and Component Selection

	•	The decomposition was performed on raw and z-transformed SNP effect sizes.
	•	Dimension 16 was identified as optimal, providing the best trade-off between reproducibility, interpretability, and model complexity.
