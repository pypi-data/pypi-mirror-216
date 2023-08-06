from setuptools import (
    setup,
    find_packages,
)

deps = {
    'bubble-env': [
        'dacite>=1.6.0',
        'fabric>=2.6.0',
        'loguru>=0.5.3',
        'paramiko>=2.8.0',
        'ruamel.base>=1.0.0',
        'rwlock>=0.0.7',
    ]
}

with open('./README.md', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='bubble-env',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='0.1.3',
    description="""Common library to deployment bubble chain""",
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    author='shing',
    author_email='shinnng@outlook.com',
    url='https://github.com/shinnng/bubble-env',
    include_package_data=True,
    install_requires=[
        'dacite>=1.6.0',
        'fabric>=2.6.0',
        'loguru>=0.5.3',
        'paramiko>=2.8.0',
        'ruamel.base>=1.0.0',
        'rwlock>=0.0.7',
    ],
    py_modules=['bubble_env'],
    extras_require=deps,
    license="MIT",
    zip_safe=False,
    package_data={'bubble-env': ['py.typed']},
    keywords='bubble',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
