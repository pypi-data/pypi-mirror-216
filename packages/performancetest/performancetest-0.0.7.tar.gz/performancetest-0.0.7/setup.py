# # _*_ coding: utf-8 _*_
from setuptools import setup, find_packages

setup(
       name='performancetest',
       version='0.0.7',
       url='https://github.com/1033866383/perf-orange-cat',
       author='bozhou.fan',
       author_email='15525730080@163.com',
       description='Android, IOS app_performance',
       packages=find_packages(),
       install_requires=[],
       include_package_data=True,  # 这里添加 include_package_data 参数
       package_data={
           'performancetest': ['web/test_result/*']
       },
       classifiers=[
           'Development Status :: 3 - Alpha',
           'Intended Audience :: Developers',
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 3',
           'Programming Language :: Python :: 3.9',
       ],
   )