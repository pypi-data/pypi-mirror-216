from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='PB_Sent',
    version='0.0.1',
    author='Bayode Ogunleye',
    author_email='batoog101@yahoo.com',
    description='A sentiment lexicon algorithm to classify pidgin English and English text into positive, negative or neutral',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/batoog101/SentiLEYE.git',
    packages=['sentileye'],
    include_package_data=True,
    package_data={
        'sentileye': ['neg.txt', 'neg1.txt','sentileye_list.csv', 'slang.csv', 'emotion_new.csv'],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=['pandas', 're', 'ast', 'csv'],
)

