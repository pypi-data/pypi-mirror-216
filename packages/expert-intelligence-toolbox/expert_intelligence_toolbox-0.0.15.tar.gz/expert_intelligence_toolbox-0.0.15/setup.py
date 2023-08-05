from setuptools import setup, find_packages

setup(
    name="expert_intelligence_toolbox",
    version='0.0.15',
    packages=find_packages(),
    install_requires=[
        'pandas==2.0.2',
        'pyarrow==10.0.1',
        'snowflake-connector-python==3.0.4',
        'snowflake-snowpark-python==1.5.0',
        'configparser==5.3.0',
        'geopandas==0.12.2',
        'geolib==1.0.7',
        'geopy==2.2.0',
        'OSMPythonTools==0.3.5',
        'shapely==2.0.1',
    ],
)
