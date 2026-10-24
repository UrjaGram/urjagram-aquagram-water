from setuptools import setup, find_packages

setup(
    name="urjagram-aquagram-water",
    version="1.0.0",
    description="AquaGramOS: Village Groundwater & Soil Intelligence Engine for UrjaGram Innovations",
    author="Kushagra Singh Kushwah (VNIT Nagpur)",
    author_email="kushagrasinghkushwah46@gmail.com",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pydantic>=2.0.0",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "aquagram-water=src.cli:main",
            "aquagram-dashboard=src.dashboard:run_server",
        ],
    },
)
