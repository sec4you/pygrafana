from distutils.core import setup
setup(
  name = 'pygrafana',
  packages = ['pygrafana'],
  version = '0.1',
  description = "Library to consume Grafana's API",
  author = 'Angelo Moura',
  author_email = 'angelo.moura@sec4you.com.br',
  url = 'https://github.com/sec4you/pygrafana',
  download_url = 'https://github.com/sec4you/pygrafana/archive/0.1.tar.gz',
  keywords = ['grafana','api'],
  install_requires=['PyYAML>=3.12','requests>=2.18.4'],
  classifiers = [],
)
