import os
import setuptools

def requirements():
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), encoding='utf-8') as f:
        return f.read().splitlines()

setuptools.setup(
	name='rest-api-supporter',
	version='0.0.15',
	description='Rest api supporter',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	author='Sang Ki Kwon',
	url='https://github.com/automatethem/rest-api-supporter',
	install_requires=requirements(),
	author_email='automatethem@gmail.com',
	license='MIT',
	packages=setuptools.find_packages(),
	zip_safe=False
)
