from setuptools import setup, find_packages

setup(
    name="task-management",
    version="0.1",
    packages=find_packages(include=["webapi", "webapi.*"]),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pytest",
        "httpx"
    ],
)