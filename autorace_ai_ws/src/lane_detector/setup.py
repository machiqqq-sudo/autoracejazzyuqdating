from setuptools import find_packages, setup

package_name = 'lane_detector'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jkchen525',
    maintainer_email='machiqqq@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_projection = lane_detector.image_projection:main',
            'lane_detection = lane_detector.lane_detection:main'
        ],
    },
)
