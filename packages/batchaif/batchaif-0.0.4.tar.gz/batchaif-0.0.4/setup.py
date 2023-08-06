from setuptools import setup, find_packages

setup(
    name='batchaif',
    version='0.0.4',
    url='https://gitlab-research.centralesupelec.fr/mics_biomathematics/biomaths/batchaif',
    license='',
    author='Lily Monnier',
    author_email='lily.monnier@student.ecp.fr',
    description='Package to correct batch effects in scRNA-seq data using Adversarial Information Factorization',
    project_urls={
        "Bug Tracker": 'https://gitlab-research.centralesupelec.fr/mics_biomathematics/biomaths/batchaif/issues',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "batchaif"},
    packages=find_packages(where="batchaif"),
    python_requires=">=3.9",
    install_requires=[
        'anndata>=0.7.6',
        'h5py>=3.6.0',
        'matplotlib>=3.5.1',
        'numba>=0.55.1',
        'numpy>=1.21.5',
        'pandas>=1.4.1',
        'scanpy>=1.8.2',
        'scikit-learn>=1.0.2',
        'scikit-network==0.23.0',
        'scipy>=1.6.3',
        'seaborn>=0.11.1',
        'torch>=1.10.2',
        'torchaudio>=0.10.2',
        'torchvision>=0.11.3',
        'umap-learn>=0.5.1',
        'harmonypy>=0.0.5'
    ]
)
