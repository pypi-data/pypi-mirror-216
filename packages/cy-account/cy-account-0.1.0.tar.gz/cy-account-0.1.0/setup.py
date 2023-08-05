import setuptools

setuptools.setup(
    name="cy-account",
    version="0.1.0",
    author="luyuan",
    author_email="136735431@qq.com",
    description="edited by myself",
    py_modules=["cy-account.account_api", "cy-account.cy_request", "cy-account.user_info", ],
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent"],
    # 自动找到项目中导入的模块
    packages=setuptools.find_packages(),
    # 依赖模块
    install_requires=['pydantic', 'fastapi', 'redis'],
    python_requires=">=3"
)
