from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'autorace_jazzy'

# Collect standard data files
data_files = [
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    ('share/' + package_name + '/launch', glob('launch/*.py')),
    ('share/' + package_name + '/sdf', glob('sdf/*.sdf')),
    ('share/' + package_name + '/worlds', glob('worlds/*.world')),
    ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
    ('share/' + package_name + '/config', glob('config/*.yaml')),
]

# Recursively add files from the models directory
for root, dirs, files in os.walk('models'):
    if files:
        # Create the destination path in the share directory
        dest_dir = os.path.join('share', package_name, root)
        # Create a list of file paths for this directory
        file_list = [os.path.join(root, f) for f in files]
        data_files.append((dest_dir, file_list))

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
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
