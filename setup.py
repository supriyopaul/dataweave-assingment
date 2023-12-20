from setuptools import setup, find_packages

setup(
    name='dataweave',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'python-multipart',
        'pika',
        
    ],
    entry_points={
        'console_scripts': [
            'dataweave=dataweave.cli:main',
        ],
    },
)
