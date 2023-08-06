from setuptools import setup, find_packages

setup(
    name='yahoo_fantasy_baseball',
    version='1.0.0',
    description='Yahoo Fantasy Baseball Scraper',
    author='Taylor Ward',
    author_email='tayorreeseward@gmail.com',
    url='https://github.com/hotlikesauce/yahoo-fantasy-baseball-analyzer',
    packages=find_packages(),
    install_requires=[
        'urllib3==1.24.2',
        'bs4==0.0.1'

        # List any dependencies required by your package
    ],
)
