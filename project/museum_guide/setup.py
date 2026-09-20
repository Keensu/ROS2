from setuptools import find_packages, setup

package_name = 'museum_guide'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/museum_launch.py']),
        ('share/' + package_name + '/test',
         ['test/test_exhibits.py',
          'test/test_guide_action.py',
          'test/test_distance.py']),
        ('.', ['.flake8']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yar10',
    maintainer_email='yar10@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'exhibit_server = museum_guide.exhibit_server:main',
            'guide_node = museum_guide.guide_node:main',
            'visitor_spawner = museum_guide.visitor_spawner:main',
            'distance_monitor = museum_guide.distance_monitor:main',
            'route_client = museum_guide.route_client:main',
            'exhibit_markers = museum_guide.exhibit_markers:main',
        ],
    },
)
