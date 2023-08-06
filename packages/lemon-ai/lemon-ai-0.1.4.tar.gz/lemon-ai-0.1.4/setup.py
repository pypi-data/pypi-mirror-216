from setuptools import setup

setup(
    name='lemon-ai',
    version='0.1.4',    
    description='A Python client that enables Langchain agents to design and execute workflow automations targeting internal tooling',
    author='Felix Brockmeier',
    author_email='felix@citodata.com',
    url="https://github.com/feliciori/lemon-ai-client-python",
    license='MIT',
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