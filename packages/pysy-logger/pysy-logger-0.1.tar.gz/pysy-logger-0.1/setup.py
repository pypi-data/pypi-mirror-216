from distutils.core import setup
setup(
  name = 'pysy-logger',         # How you named your package folder (MyLib)
  packages = ['pysy-logger'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = """
        This is (Py)thon Ea(sy) Logger
        This creates a simple to use python logger, Uses DictConfig for configuring logger.
        This Software is in initial stage and will be updated as I move on. Please contribute as you see fit
    """,   # Give a short description about your library
  author = 'Sabari',                   # Type in your name
  author_email = 'mailme@isbarirajan.com',      # Type in your E-Mail
  url = 'https://github.com/ISabariRajan',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ISabariRajan/Logger/archive/refs/tags/v-0.1.tar.gz',    # I explain this later on
  keywords = ['Logger', 'Easy', 'PySy'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
