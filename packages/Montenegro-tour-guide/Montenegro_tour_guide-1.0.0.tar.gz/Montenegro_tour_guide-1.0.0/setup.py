from setuptools import setup, find_packages
requirements = ['']
setup(
    name='Montenegro_tour_guide',
    version='1.0.0',
    packages=find_packages(exclude=['tests*']),
    license='GNU General Public License v3.0',
    description='A python wrapper for the nft-storage',
    long_description=open('README.md').read(),
    keywords=['Montenegro', 'Montenegro health tour', 'nft_storage'],
    install_requires=requirements,
    url='https://github.com/kbm9696/Montenegro_tour_guide',
    author='Balamurugan',
    author_email='kbala007.1996@gmail.com',
    long_description_content_type='text/markdown'
)