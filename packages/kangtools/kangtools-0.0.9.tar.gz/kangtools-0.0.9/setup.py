from setuptools import setup

setup(
    name='kangtools',  # 包的名字
    version='0.0.9',  # 包的版本
    author='xiaowen kang',  # 你的名字
    author_email='kangxiaowen@gmail.com',  # 你的邮箱
    packages=['kangtools'],  # 包含的包，这是一个列表，如果你的项目包含多个包，都需要列在这里
    license='LICENSE',  # 许可证文件
    description='A Python package for version control.',  # 包的简短描述
    long_description=open('README.md').read(),  # 包的详细描述，通常从 README.md 文件读取
    long_description_content_type="text/markdown",  # 描述的格式，使用markdown格式
    entry_points={
    'console_scripts': [
        'kangtools_version_control=kangtools.version_control:main',
        'kangtools_commit_version_to_git=kangtools.commit_version_to_git:main',],
    },

)
