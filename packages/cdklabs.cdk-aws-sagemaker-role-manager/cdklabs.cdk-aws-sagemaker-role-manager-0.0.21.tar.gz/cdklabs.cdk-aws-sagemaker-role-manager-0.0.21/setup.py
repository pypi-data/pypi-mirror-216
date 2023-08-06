import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdklabs.cdk-aws-sagemaker-role-manager",
    "version": "0.0.21",
    "description": "Create roles and policies for ML Activities and ML Personas",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-aws-sagemaker-role-manager",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-dev@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-aws-sagemaker-role-manager"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdklabs.cdk_aws_sagemaker_role_manager",
        "cdklabs.cdk_aws_sagemaker_role_manager._jsii"
    ],
    "package_data": {
        "cdklabs.cdk_aws_sagemaker_role_manager._jsii": [
            "cdk-aws-sagemaker-role-manager@0.0.21.jsii.tgz"
        ],
        "cdklabs.cdk_aws_sagemaker_role_manager": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.83.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.84.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
