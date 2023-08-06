from distutils.core import setup
from setuptools import find_packages

setup(
  name = 'kyano',         
  packages = find_packages(),
  version = '0.7',      
  license='apache-2.0',        
  description = 'Python module providing anomaly detection datasets and tools for evaluating algorithms. Modification of yano, mostly by replacing the datasets, through a kaggle query',   
  author = 'Simon Klüttermann',                   
  author_email = 'Simon.Kluettermann@cs.tu-dortmund.de',      
  url = 'https://github.com/psorus/kano',   
  download_url = 'https://github.com/psorus/kano/archive/v_01.tar.gz',    
  keywords = ['DATA', 'ANOMALY DETECTION', 'OUTLIER DETECTION', 'ML'],   
  install_requires=[            
          'numpy',
          'sklearn',
          'tqdm',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Science/Research',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
