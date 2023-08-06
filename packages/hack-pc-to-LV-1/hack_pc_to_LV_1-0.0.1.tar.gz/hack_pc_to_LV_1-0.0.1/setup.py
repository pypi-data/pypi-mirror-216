from setuptools import setup, find_packages

setup(
    name='hack_pc_to_LV_1',
    version='0.0.1',
    description='PYPI tutorial package creation written by TeddyNote',
    author='LV_1_HAEIL',
    author_email='cfku0172@gmail.com',
    url='https://github.com/jst7501',
    install_requires=['halo', 'time', 'tqdm',],
    packages=find_packages(exclude=[]),
    keywords=['HAEIL'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
