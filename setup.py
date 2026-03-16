from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'autorace_jazzy'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        ('share/' + package_name + '/sdf', glob('sdf/*.sdf')),
        ('share/' + package_name + '/worlds', glob('worlds/*.world')),
        ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
        ('share/' + package_name + '/models', glob('models/**/*', recursive=True)),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jkchen525',
    maintainer_email='jkchen525@todo.todo',
    description='淡江大學 AI 系大三專題：TurtleBot3 自動駕駛模擬專案。',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'autorace_manager = autorace_jazzy.autorace_manager:main'
        ],
    },
)
