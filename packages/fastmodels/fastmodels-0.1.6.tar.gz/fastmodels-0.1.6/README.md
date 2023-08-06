# FastModels Command-line Interface

一个python library，方便用户进行数据预处理、和通过API访问FastModels服务。

### Development:
To test the lib locally, run `pip install -e .` in the fastmodels directory

### Uploading to PyPl:
1. 安装必要的包`pip install setuptools wheel twine`
2. 打包`python setup.py sdist bdist_wheel`
3. 测试上传（可选）`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
4. 实际上传`twine upload dist/*`


### Usages：
1. `pip install fastmodels`
2. `fastmodels '{"prompt": "Write a short story.", "completion": "Once upon a time..."}'`

