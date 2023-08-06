from setuptools import setup
def readme():
    with open('README.md','r') as f:
        return f.read()
setup(
    name='sourceshot',
    version='2.0.1',
    description='Takes pictures of code!',
    long_description=readme(),
    packages=['sshot'],
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts':[
            'sshot=sshot:_cli'
        ]
    },
    python_requires='>=3.6',
    install_requires=['pygments>=0.7','pillow<10','numpy','opencv-python','colorama'],
    keywords=['code','picture'],url='https://github.com/none-None1/sourceshot'
)
