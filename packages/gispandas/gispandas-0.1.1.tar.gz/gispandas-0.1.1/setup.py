from setuptools import setup, find_packages
import os

VERSION = '0.1.1'

setup(
    name='gispandas',  # package name
    version=VERSION,  # package version
    author="HMX",
    author_email="kzdhb8023@163.com",
    description='gispandas',  # package description
    packages=find_packages(),
    url="https://github.com/mxhou/gispandas/",
    zip_safe=False,
    # What packages are required for this module to be executed?
    REQUIRED = ['geopandas', 'numpy', 'geopandas','json','rasterio','rasterstats'],
    license='MIT',
    python_requires=">=3.6",
    keywords=['gis','geo','tif','json']
)