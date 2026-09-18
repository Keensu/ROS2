from setuptools import find_packages, setup

package_name = 'hw2_py_pubsub'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/test', ['test/pubsub_test_launch.py']),
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
            'random_publisher = hw2_py_pubsub.publisher_node:main',
            'mode_subscriber = hw2_py_pubsub.subscriber_node:main',

        ],
    },
)
