from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='lemon-ai',
    version='0.1.6',    
    description='A Python client that enables Langchain agents to design and execute workflow automations targeting internal tooling',
    author='Felix Brockmeier',
    author_email='felix@citodata.com',
    url="https://github.com/feliciori/lemonai-py-client",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    packages=['lemon_ai'],
    python_requires='>=3.8.1',
    install_requires=[
        'langchain',
        'loguru'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)