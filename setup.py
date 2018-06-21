from setuptools import setup

setup(name='Deep habitat name',
      version='0.1',
      description='Generates name of the place town or city.',
      url='https://github.com/bigr/deep_habitat_name',
      author='Pavel Klinger',
      author_email='ja@bigr.cz',
      license='MIT',
      packages=['deep_habitat_name'],
      install_requires=[
            'keras',
            'h5py',
            'numpy',
      ],
      zip_safe=False,
      scripts=['bin/deep-habitat-name-train', 'bin/deep-habitat-name-generate', 'bin/deep-habitat-name-get-names']
      #test_suite='test'
)
