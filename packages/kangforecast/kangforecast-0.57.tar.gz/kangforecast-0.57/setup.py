from setuptools import setup, find_packages

setup(
    name='kangforecast',
    version='0.57',
    description='A simple forecast package.',
    author='Xiaowen Kang',
    author_email='kangxiaowen@gmail.com',
    url='https://www.linkedin.com/in/xiaowenkang/',  # replace with the url of your GitHub repo
    packages=find_packages(),
    package_data={'kangforecast': ['data/*.csv']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # choose a license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'kanglib',
        'pandas',
        # other libraries...
    ],
    entry_points={
        'console_scripts': [
            'kangforecast_command=kangforecast.main:main',
        ],
    },
)
