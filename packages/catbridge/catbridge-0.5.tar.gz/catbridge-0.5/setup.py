from setuptools import setup, find_packages

setup(
    name="catbridge",
    version="0.5",
    packages=find_packages(),

    # Metadata
    author="Bowen Yang",
    author_email="by172@georgetown.edu",
    description="CAT Bridge (Compounds And Transcripts Bridge) is a robust tool built with the goal of uncovering biosynthetic mechanisms in multi-omics data, such as identifying genes potentially involved in compound synthesis by incorporating metabolomics and transcriptomics data.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    url="https://github.com/Bowen999/catbridge",  # Optional
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ],

    install_requires=[
        # List your package's dependencies here
    ],
)
