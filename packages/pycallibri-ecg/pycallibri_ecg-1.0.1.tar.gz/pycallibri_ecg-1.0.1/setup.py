from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pycallibri_ecg',
    version='1.0.1',
    py_modules=['callibri_ecg.callibri_ecg_lib'],
    packages=['callibri_ecg'],
    url='https://gitlab.com/neurosdk2/neurosamples/-/tree/main/python',
    license='MIT',
    author='Brainbit Inc.',
    author_email='support@brainbit.com',
    description='Python wrapper for CallibriECG library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={"callibri_ecg": ['libs\\x64\\callibri_utils-x64.dll',
                               'libs\\x64\\filters.dll', 
                               'libs\\x86\\callibri_utils-x86.dll',
                               'libs\\x86\\filters.dll']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.7',
)