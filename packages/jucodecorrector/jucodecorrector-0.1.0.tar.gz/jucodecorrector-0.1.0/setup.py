from setuptools import setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='jucodecorrector',
    version='0.1.0',
    author='Isaac Duong',
    author_email='isaaacduong@gmail.com',
    license='MIT',    
    url='https://github.com/isaacduong/jucodecorrector.git',
    description=("Python script to rivise error code " 
                 "based on the error messages " 
                 "using ChatGPT."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['jucodecorrector'],
    install_requires=[   
            'ipywidgets==8.0.6',
            'black==23.3.0',
            'colored==2.2.2',
            'ipython==8.14.0',
            'openai==0.27.8',
            'PyAutoGUI==0.9.54',
            'Pygments==2.15.1',
            'pyperclip==1.8.2',
            'jupyter_ai_magics==0.8.0',
      ],
   
)
