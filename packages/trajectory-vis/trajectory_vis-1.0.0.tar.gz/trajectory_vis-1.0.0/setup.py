from setuptools import setup, find_namespace_packages

setup(
    name="trajectory_vis",
    url="https://gitlab-ncsa.ubisoft.org/tboulet/trajectory-visualization", 
    author="tboulet",
    author_email="timothe.boulet0@gmail.com",
    
    packages=find_namespace_packages(),
    install_requires=[
        'pygame',
    ],
    version="1.0.0",
    license="MIT",
    description="Visualization of data and/or model trajectories on a 2D plane using pygame",
    long_description=open('README.md').read(),     
    long_description_content_type="text/markdown", 
)