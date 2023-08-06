from setuptools import setup, find_packages

setup(
    name='aicoder',
    version='0.1.1',
    url='https://github.com/carlospolop/AICoder',
    author='Carlos Polop',
    author_email='carlospolop@gmail.com',
    description='This is a tool to generate code using OpenAI api.',
    packages=find_packages(),    
    install_requires=[
        'requests',
        'colorlog',
        'openai',
        'tqdm',
        'PyGithub'
    ],
    entry_points={
        'console_scripts': [
            'aicoder=aicoder:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
)