from setuptools import setup

if __name__ == "__main__":
    setup(
        name="klcreqs",
        version="2023.06.29",
        description="library for streamlining api requests",
        long_description="coming soon",
        readme="README.md",
        author='Thomas Nemechek',
        author_email='tnemechek@klcapital.com',
        classifiers=["Programming Language :: Python"],
        packages=['klcreqs'],
        include_package_data=True,
        install_requires=['numpy>=1.20.3',
        'pandas>=1.4.3',
        'requests>=2.26.0']
        )