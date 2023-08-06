from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyneurosdk2',
    version='1.0.5',
    py_modules=[
        'neurosdk.scanner',
        'neurosdk.sensor',
        'neurosdk.cmn_types',
        'neurosdk.__cmn_types',
        'neurosdk.__utils',
        'neurosdk.amp_sensor',
        'neurosdk.electrode_sensor',
        'neurosdk.envelope_sensor',
        'neurosdk.fpg_sensor',
        'neurosdk.mems_sensor',
        'neurosdk.neuro_smart_sensor',
        'neurosdk.resist_sensor',
        'neurosdk.respiration_sensor',
        'neurosdk.callibri_sensor',
        'neurosdk.brainbit_sensor',
        'neurosdk.brainbit_black_sensor',
        
        
        
        
        'neurosdk.signal_sensor'],
    packages=['neurosdk'],
    url='https://gitlab.com/brainbit-inc/brainbit-sdk',
    license='MIT',
    author='Brainbit Inc.',
    author_email='support@brainbit.com',
    description='Python wrapper for NeuroSDK2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={"neurosdk": ['libs\\neurosdk2-x32.dll', 'libs\\neurosdk2-x64.dll']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.7',
)
