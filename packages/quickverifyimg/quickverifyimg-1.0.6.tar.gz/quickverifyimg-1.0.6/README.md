# QuickVerifyImg

# 打包上传
python setup.py sdist bdist_wheel
twine upload dist/*

快速检验图片是否存在指定的用例集中

使用示例: tests/verify_test.py