from setuptools import setup, find_packages

setup(name='nodezator_plus',
      version='0.1.1',
      description='update for nodezator',
      packages=find_packages(),
      author_email='bagd.artur@gmail.com',
      zip_safe=False,
      include_package_data=True,
      package_data={'nodezator_plus': ['ru/dialogs_map.pyl', 'ru/status_messages_map.pyl', 'ru/translations_map.pyl', 'anim.mp4']})
