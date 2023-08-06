from setuptools import setup, find_packages

if __name__ == '__main__':
    name = 'taichu-dataflow'

    requirements = ['boto==2.49.0', 'esdk-obs-python==3.22.2', 'click==8.1.3']

    long_description = ''
    # with open('README.md', 'r') as f:
    #     long_description = f.read()

    setup(
        name=name,
        version='1.1.2',
        description='taichu serve is a tool for serving dataflow',
        long_description=long_description,
        author='taichu platform team',
        python_requires=">=3.6.0",
        url='',
        keywords='taichu',
        packages=find_packages(),
        install_requires=requirements,
        include_package_data=True,
        package_data={
            '': ['*.sh'],
        },
        entry_points={
            'console_scripts': [
                'taichudataflow = taichu_dataflow.command:cli',
            ],
        }
    )
