
from setuptools import setup, find_packages

VERSION = '0.1.3'
DESCRIPTION = 'K Anonymity for Text first Try'
LONG_DESCRIPTION = 'A package that takes a dataframe with a corpus and return an anonymized corpus'

# Setting up
setup(
    name="Kanon4txt",
    version=VERSION,
    author="Lior Trieman",
    author_email="<liortr30@gmail.com>",
    url='https://github.com/LiorTrieman/Kanon4txt/tree/maine',
    download_url='https://github.com/LiorTrieman/Kanon4txt/archive/refs/tags/0.1.3.tar.gz',  # I explain this later on

    license='MIT',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # NEED TO ADD HERE ALL REQUIREMENTS!!!!!

    install_requires=["ipython==8.10.0",
                      "joblib==1.2.0",
                      "matplotlib==3.7.0",
                      "numpy==1.23.5",
                      "pandas==1.5.3",
                      "scikit_learn==1.2.1",
                      "scipy==1.10.1",
                      "setuptools==65.5.0",
                      "tqdm==4.64.1"],
    keywords=['python', 'corpus', 'stopwords', 'DBSCAN', 'generalization', 'reduction'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",

    ]
)
