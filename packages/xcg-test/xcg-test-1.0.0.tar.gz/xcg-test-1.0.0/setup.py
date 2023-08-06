from setuptools import setup, find_packages

setup(
    name='xcg-test',
    version='1.0.0',
    description='打包测试',
    author='chuck',
    author_email='chuck@email.com',
    packages=find_packages(),
    install_requires=[
        # 依赖的其他包
        "pandas",
        "numpy",
        "pymatgen",
    ],
)
