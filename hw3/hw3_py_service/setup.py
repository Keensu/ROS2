from setuptools import find_packages, setup

package_name = 'hw3_py_service'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/test', ['test/test_service.py']),
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
            'server = hw3_py_service.server_node:main',
            'client = hw3_py_service.client_node:main',
        ],
    },
)
