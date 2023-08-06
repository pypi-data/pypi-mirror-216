'''
## cdk-aws-sagemaker-role-manager

## Usage

### Create Role from ML Activity with VPC and KMS conditions

```python
import { Stack } from 'aws-cdk-lib';
import { Activity } from '@cdklabs/cdk-aws-sagemaker-role-manager';

const stack = new Stack(app, 'CdkRoleManagerDemo');

const activity = Activity.manageJobs(stack, 'id1', {
    rolesToPass: [iam.Role.fromRoleName('Enter Name')],
    subnets: [ec2.Subnet.fromSubnetId('Enter Id')],
    securityGroups: [ec2.SecurityGroup.fromSecurityGroupId('Enter Id')],
    dataKeys: [kms.Key.fromKeyArn('Enter Key Arn')],
    volumeKeys: [kms.Key.fromKeyArn('Enter Key Arn')],
});

activity.createRole(stack, 'role id', 'Enter Name');
```

### Create Role from ML Activity without VPC and KMS conditions

```python
import { Stack } from 'aws-cdk-lib';
import { Activity } from '@cdklabs/cdk-aws-sagemaker-role-manager';

const stack = new Stack(app, 'CdkRoleManagerDemo');

const activity = Activity.manageJobs(this, 'id1', {
    rolesToPass: [iam.Role.fromRoleName('Enter Name')],
});

activity.createRole(this, 'role id', 'Enter Name', 'Enter Description');
```

### Create Role from Data Scientist ML Persona

```python
import { Stack } from 'aws-cdk-lib';
import { Activity, Persona } from '@cdklabs/cdk-aws-sagemaker-role-manager';

const stack = new Stack(app, 'CdkRoleManagerDemo');

let persona = new Persona(this, 'persona id', {
    activities: [
        Activity.useStudioApps(),
        Activity.manageJobs(this, 'id1', {rolesToPass: [iam.Role.fromRoleName('Enter Name')]}),
        Activity.manageModels(this, 'id2', {rolesToPass: [iam.Role.fromRoleName('Enter Name')]}),
        Activity.manageExperiments(this, 'id3', {}),
        Activity.searchExperiments(this, 'id4', {}),
        Activity.accessBuckets(this, 'id5', {buckets: [s3.S3Bucket.fromBucketName('Enter Name')]})
    ],
    subnets: [ec2.Subnet.fromSubnetId('Enter Id')],
    securityGroups: [ec2.SecurityGroup.fromSecurityGroupId('Enter Id')],
    dataKeys: [kms.Key.fromKeyArn('Enter Key Arn')],
    volumeKeys: [kms.Key.fromKeyArn('Enter Key Arn')],
});

persona.createRole(this, 'role id', 'Enter Name', 'Enter Description');
```

### Create Role from Data Scientist ML Persona without vpc and kms global conditions

```python
import { Stack } from 'aws-cdk-lib';
import { Activity, Persona } from '@cdklabs/cdk-aws-sagemaker-role-manager';

const stack = new Stack(app, 'CdkRoleManagerDemo');

// Please see below how to create the Data Scientist ML Persona using its ML Activities.
// You can update the following list with changes matching your usecase.
let persona = new Persona(this, 'persona id', {
    activities: [
        Activity.useStudioApps(),
        Activity.manageJobs(this, 'id1', {rolesToPass: [iam.Role.fromRoleName('Enter Name')]}),
        Activity.manageModels(this, 'id2', {rolesToPass: [iam.Role.fromRoleName('Enter Name')]}),
        Activity.manageExperiments(this, 'id3', {}),
        Activity.searchExperiments(this, 'id4', {}),
        Activity.accessBuckets(this, 'id5', {buckets: [s3.S3Bucket.fromBucketName('Enter Name')]})
    ],
});

// We can create a role with Data Scientist persona permissions
const role = persona.createRole(this, 'role id', 'Enter Name', 'Enter Description');
```

### Create Role MLOps ML Persona

```python
import { Stack } from 'aws-cdk-lib';
import { Activity, Persona } from '@cdklabs/cdk-aws-sagemaker-role-manager';

const stack = new Stack(app, 'CdkRoleManagerDemo');

let persona = new Persona(this, 'persona id', {
    activities: [
        Activity.useStudioApps(this, 'id1', {}),
        Activity.manageModels(this, 'id2', {rolesToPass: [iam.Role.fromRoleName('Enter Name')]}),
        Activity.manageEndpoints(this, 'id3',{rolesToPass: [iam.Role.fromRoleName('Enter Name')]}),
        Activity.managePipelines(this, 'id4', {rolesToPass: [iam.Role.fromRoleName('Enter Name')]}),
        Activity.searchExperiments(this, 'id5', {})
    ],
    subnets: [ec2.Subnet.fromSubnetId('Enter Id')],
    securityGroups: [ec2.SecurityGroup.fromSecurityGroupId('Enter Id')],
    dataKeys: [kms.Key.fromKeyArn('Enter Key Arn')],
    volumeKeys: [kms.Key.fromKeyArn('Enter Key Arn')],
});

const role = persona.createRole(this, 'role id', 'Enter Name', 'Enter Description');
```

### Create Role from MLOps ML Persona without vpc and kms global conditions

```python
import { Stack } from 'aws-cdk-lib';
import { Activity, Persona } from '@cdklabs/cdk-aws-sagemaker-role-manager';

const stack = new Stack(app, 'CdkRoleManagerDemo');

let persona = new Persona(this, 'persona id', {
    activities: [
        Activity.useStudioApps(this, 'id1', {}),
        Activity.manageModels(this, 'id2', {rolesToPass: [iam.Role.fromRoleName('Enter Name')]}),
        Activity.manageEndpoints(this, 'id3',{rolesToPass: [iam.Role.fromRoleName('Enter Name')]}),
        Activity.managePipelines(this, 'id4', {rolesToPass: [iam.Role.fromRoleName('Enter Name')]}),
        Activity.searchExperiments(this, 'id5', {})
    ],
});

const role = persona.createRole(this, 'role id', 'Enter Name', 'Enter Description');
```

## Available ML Activities

| ML Activity Name | ML Activity Interface           | ML Activity Description                                                                                   | ML Activity Required Parameters |
|------------------|---------------------------------|-----------------------------------------------------------------------------------------------------------|---------------------------------|
| Access Required AWS Services          | Activity.accessAwsServices()    | Permissions to access S3, ECR, Cloudwatch and EC2. Required for execution roles for jobs and endpoints.   | ecrRepositories, s3Buckets      |
| Run Studio Applications         | Activity.runStudioApps()        | Permissions to operate within a Studio environment. Required for domain and user-profile execution roles. | rolesToPass                     |
| Manage ML Jobs          | Activity.manageJobs()           | Permissions to manage SageMaker jobs across their lifecycles.                                             | rolesToPass                     |
| Manage Models          | Activity.manageModels()         | 	Permissions to manage SageMaker models and Model Registry.                                               | rolesToPass                     |
| Manage Endpoints        | Activity.manageEndpoints()      | Permissions to manage SageMaker Endpoint deployments and updates.                                         | No required parameters          |
| Manage Pipelines         | Activity.managePipelines()      | Permissions to manage SageMaker Pipelines and pipeline executions.                                        | rolesToPass                     |
| Manage Experiments         | Activity.manageExperiments()    | 	Permissions to manage experiments and trials.                                                            | No required parameters          |
| Search and visualize experiments         | Activity.visualizeExperiments() | Permissions to audit, query lineage and visualize experiments.                                            | No required parameters          |
| 	Manage Model Monitoring         | Activity.monitorModels()        | Permissions to manage monitoring schedules for SageMaker Model Monitor.                                   | rolesToPass                     |
| S3 Full Access        | Activity.accessS3AllResources() | 	Permissions to perform all S3 operations                                                                 | No required parameters          |
| S3 Bucket Access         | Activity.accessS3Buckets()      | Permissions to perform operations on specified buckets.                                                   | s3Buckets                       |
| 	Query Athena Workgroups        | Activity.queryAthenaGroups()    | Permissions to execute and manage Amazon Athena queries.                                                  | athenaWorkgroupNames            |
| 	Manage Glue Tables       | Activity.manageGlueTables()     | 	Permissions to create and manage Glue tables for SageMaker Feature Store and Data Wrangler.                                                                                                          | s3Buckets, glueDatabaseNames                     |

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecr as _aws_cdk_aws_ecr_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class Activity(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.Activity",
):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="accessAwsServices")
    @builtins.classmethod
    def access_aws_services(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ecr_repositories: typing.Sequence[_aws_cdk_aws_ecr_ceddda9d.IRepository],
        s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param ecr_repositories: 
        :param s3_buckets: 
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5211c3777ff232336aa3201329facc2a3b849d0ff050e74c891cb97170a57e03)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = AccessAwsServicesOptions(
            ecr_repositories=ecr_repositories,
            s3_buckets=s3_buckets,
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "accessAwsServices", [scope, id, options]))

    @jsii.member(jsii_name="accessS3AllResources")
    @builtins.classmethod
    def access_s3_all_resources(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3cf760fce634375ae1e69d657af8b0eac69356533d6075aa1585bb02c1b6b7b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = AccessS3AllResourcesOptions(
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "accessS3AllResources", [scope, id, options]))

    @jsii.member(jsii_name="accessS3AllResourcesV2")
    @builtins.classmethod
    def access_s3_all_resources_v2(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5237dc8d2a91e9185d52af32f0836b1f7cc405b2e72a542a1d53a1473f9f475)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = AccessS3AllResourcesV2Options(
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "accessS3AllResourcesV2", [scope, id, options]))

    @jsii.member(jsii_name="accessS3Buckets")
    @builtins.classmethod
    def access_s3_buckets(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param s3_buckets: 
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a9501f4b7c33148fbdca2c97d99ccbfb392b8dbef140a6492672491626f6ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = AccessS3BucketsOptions(
            s3_buckets=s3_buckets,
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "accessS3Buckets", [scope, id, options]))

    @jsii.member(jsii_name="manageEndpoints")
    @builtins.classmethod
    def manage_endpoints(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6daccbba48fb46e0449deee6661617129440a963c6e957addb3c68d1143ae7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ManageEndpointsOptions(
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "manageEndpoints", [scope, id, options]))

    @jsii.member(jsii_name="manageExperiments")
    @builtins.classmethod
    def manage_experiments(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ea1b48782474ec58c0488797eba73195eb32c68d57978e100e7830a8f944e1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ManageExperimentsOptions(
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "manageExperiments", [scope, id, options]))

    @jsii.member(jsii_name="manageGlueTables")
    @builtins.classmethod
    def manage_glue_tables(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        glue_database_names: typing.Sequence[builtins.str],
        s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param glue_database_names: 
        :param s3_buckets: 
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10c97ca33fc3bd2a34e89fabcafcdfc9601fa8fb0128b34a06e8a9420432486)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ManageGlueTablesOptions(
            glue_database_names=glue_database_names,
            s3_buckets=s3_buckets,
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "manageGlueTables", [scope, id, options]))

    @jsii.member(jsii_name="manageJobs")
    @builtins.classmethod
    def manage_jobs(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param roles_to_pass: 
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b91203598d016304f5699d33488383a6dd29c82c4f7ef130845926284c643a3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ManageJobsOptions(
            roles_to_pass=roles_to_pass,
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "manageJobs", [scope, id, options]))

    @jsii.member(jsii_name="manageModels")
    @builtins.classmethod
    def manage_models(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param roles_to_pass: 
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27a4e33293089ba1b2021b356d5b22ed51d0bd58e8869e2fb15878972fa8db2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ManageModelsOptions(
            roles_to_pass=roles_to_pass,
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "manageModels", [scope, id, options]))

    @jsii.member(jsii_name="managePipelines")
    @builtins.classmethod
    def manage_pipelines(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param roles_to_pass: 
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90fabed52bcc484d301e66a5d93a6b9e15af716296c80fd5d8d556e86479cc1d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ManagePipelinesOptions(
            roles_to_pass=roles_to_pass,
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "managePipelines", [scope, id, options]))

    @jsii.member(jsii_name="monitorModels")
    @builtins.classmethod
    def monitor_models(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param roles_to_pass: 
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045936b4c21feb245b8204a6d1c83e9bf20371db9c88d643f1015494f1d954bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = MonitorModelsOptions(
            roles_to_pass=roles_to_pass,
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "monitorModels", [scope, id, options]))

    @jsii.member(jsii_name="queryAthenaGroups")
    @builtins.classmethod
    def query_athena_groups(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        athena_workgroup_names: typing.Sequence[builtins.str],
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param athena_workgroup_names: 
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8909c9ce5ca8f3f519082beb7c5a052c211296ea88a7cbbd7f9c80e0e7ad7e84)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = QueryAthenaGroupsOptions(
            athena_workgroup_names=athena_workgroup_names,
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "queryAthenaGroups", [scope, id, options]))

    @jsii.member(jsii_name="runStudioApps")
    @builtins.classmethod
    def run_studio_apps(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param roles_to_pass: 
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d862f363484ff7073d10e0e9a5f8cec6ad1454460d029899eb4ea5f235697d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = RunStudioAppsOptions(
            roles_to_pass=roles_to_pass,
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "runStudioApps", [scope, id, options]))

    @jsii.member(jsii_name="runStudioAppsV2")
    @builtins.classmethod
    def run_studio_apps_v2(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f2dfbdf2733d397e7dcd517bd59e8ee11cc1e7c5fb92534c862f5925760876)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = RunStudioAppsV2Options(
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "runStudioAppsV2", [scope, id, options]))

    @jsii.member(jsii_name="visualizeExperiments")
    @builtins.classmethod
    def visualize_experiments(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> "Activity":
        '''
        :param scope: -
        :param id: -
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c536c4a818214b050cf817c4c9fb45b30e07940d9415c38cbadcabdccee18014)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = VisualizeExperimentsOptions(
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        return typing.cast("Activity", jsii.sinvoke(cls, "visualizeExperiments", [scope, id, options]))

    @jsii.member(jsii_name="createPolicy")
    def create_policy(
        self,
        scope: _constructs_77d1e7e8.Construct,
    ) -> _aws_cdk_aws_iam_ceddda9d.Policy:
        '''(experimental) Creates policy with permissions of activity.

        :param scope: the Construct scope.

        :return: - The policy that is created with the permissions of the activity

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284bcc1d8ec0fe9e5bde8dfe53d4ce78c8daa3a25e5dba069c16b17f43e82bf4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Policy, jsii.invoke(self, "createPolicy", [scope]))

    @jsii.member(jsii_name="createPrincipal")
    def create_principal(self) -> _aws_cdk_aws_iam_ceddda9d.ServicePrincipal:
        '''(experimental) Creates ML Activity service principal using ML Activity trust template.

        :return: - The service principal of the ML Activity

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.ServicePrincipal, jsii.invoke(self, "createPrincipal", []))

    @jsii.member(jsii_name="createRole")
    def create_role(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        role_name_suffix: builtins.str,
        role_description: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) Creates role with permissions of activity.

        :param scope: the Construct scope.
        :param id: the resource id.
        :param role_name_suffix: the name suffix of the role that will be created, if empty the role will have the name of the activity.
        :param role_description: the description of the role that will be created.

        :return: - The role that is created with the permissions of the activity

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3e83adeb6d741da0bba05fe17f3f8a1f095ee6a64ceee44d490bbf4a52eeeb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument role_name_suffix", value=role_name_suffix, expected_type=type_hints["role_name_suffix"])
            check_type(argname="argument role_description", value=role_description, expected_type=type_hints["role_description"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createRole", [scope, id, role_name_suffix, role_description]))

    @jsii.member(jsii_name="customizeKMS")
    def customize_kms(
        self,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> None:
        '''
        :param data_keys: -
        :param volume_keys: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23b8e8f6d6e6b6c8680a7a7b6f7defe7f945d01806d254a610257b9350d2cf0)
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
        return typing.cast(None, jsii.invoke(self, "customizeKMS", [data_keys, volume_keys]))

    @jsii.member(jsii_name="customizeVPC")
    def customize_vpc(
        self,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    ) -> None:
        '''
        :param subnets: -
        :param security_groups: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f395831c3296b503838d66d38e49582877c8f7e4a54aa922337c28d444357ba9)
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
        return typing.cast(None, jsii.invoke(self, "customizeVPC", [subnets, security_groups]))

    @jsii.member(jsii_name="grantPermissionsTo")
    def grant_permissions_to(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant permissions of activity to identity.

        :param identity: identity to be granted permissions.

        :return: - The grant with the permissions granted to the identity

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc551077478590cb370f7525ab06a3a96d7d813a2c57801d24e252253bd0bce)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantPermissionsTo", [identity]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ACCESS_AWS_SERVICES")
    def ACCESS_AWS_SERVICES(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ACCESS_AWS_SERVICES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ACCESS_S3_ALL_RESOURCES")
    def ACCESS_S3_ALL_RESOURCES(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ACCESS_S3_ALL_RESOURCES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ACCESS_S3_BUCKETS")
    def ACCESS_S3_BUCKETS(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ACCESS_S3_BUCKETS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATHENA_WORKGROUP_NAMES_DEFAULT_VALUE")
    def ATHENA_WORKGROUP_NAMES_DEFAULT_VALUE(cls) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "ATHENA_WORKGROUP_NAMES_DEFAULT_VALUE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MANAGE_ENDPOINTS_ACTIVITY_NAME")
    def MANAGE_ENDPOINTS_ACTIVITY_NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MANAGE_ENDPOINTS_ACTIVITY_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MANAGE_EXPERIMENTS_ACTIVITY_NAME")
    def MANAGE_EXPERIMENTS_ACTIVITY_NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MANAGE_EXPERIMENTS_ACTIVITY_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MANAGE_GLUE_TABLES_ACTIVITY_NAME")
    def MANAGE_GLUE_TABLES_ACTIVITY_NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MANAGE_GLUE_TABLES_ACTIVITY_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MANAGE_JOBS_ACTIVITY_NAME")
    def MANAGE_JOBS_ACTIVITY_NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MANAGE_JOBS_ACTIVITY_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MANAGE_MODELS_ACTIVITY_NAME")
    def MANAGE_MODELS_ACTIVITY_NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MANAGE_MODELS_ACTIVITY_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MANAGE_PIPELINES_ACTIVITY_NAME")
    def MANAGE_PIPELINES_ACTIVITY_NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MANAGE_PIPELINES_ACTIVITY_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MONITOR_MODELS_ACTIVITY_NAME")
    def MONITOR_MODELS_ACTIVITY_NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "MONITOR_MODELS_ACTIVITY_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="QUERY_ATHENA_WORKGROUPS")
    def QUERY_ATHENA_WORKGROUPS(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "QUERY_ATHENA_WORKGROUPS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RUN_STUDIO_APPS")
    def RUN_STUDIO_APPS(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "RUN_STUDIO_APPS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VISUALIZE_EXPERIMENTS")
    def VISUALIZE_EXPERIMENTS(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "VISUALIZE_EXPERIMENTS"))

    @builtins.property
    @jsii.member(jsii_name="activityName")
    def activity_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "activityName"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="isKMSCustomized")
    def is_kms_customized(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isKMSCustomized"))

    @is_kms_customized.setter
    def is_kms_customized(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028da7f2b1be36f4ca5c52ce78c4fd2a8a65a020a81d7e32ca8876022cce5922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isKMSCustomized", value)

    @builtins.property
    @jsii.member(jsii_name="isVPCCustomized")
    def is_vpc_customized(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isVPCCustomized"))

    @is_vpc_customized.setter
    def is_vpc_customized(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e762a9ced1e9eb46fe8d86693ca7418397f36a25cf79ff80424f929fac5ec03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isVPCCustomized", value)


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.ActivityProps",
    jsii_struct_bases=[],
    name_mapping={
        "activity_name": "activityName",
        "is_customization_available_for_kms": "isCustomizationAvailableForKMS",
        "is_customization_available_for_vpc": "isCustomizationAvailableForVPC",
        "athena_workgroup_names": "athenaWorkgroupNames",
        "ecr_repositories": "ecrRepositories",
        "glue_database_names": "glueDatabaseNames",
        "roles_to_pass": "rolesToPass",
        "s3_buckets": "s3Buckets",
        "version": "version",
    },
)
class ActivityProps:
    def __init__(
        self,
        *,
        activity_name: builtins.str,
        is_customization_available_for_kms: builtins.bool,
        is_customization_available_for_vpc: builtins.bool,
        athena_workgroup_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ecr_repositories: typing.Optional[typing.Sequence[_aws_cdk_aws_ecr_ceddda9d.IRepository]] = None,
        glue_database_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles_to_pass: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole]] = None,
        s3_buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param activity_name: (experimental) Name of the SageMaker Activity. This name will be used to name the IAM policy that is created from this Activity.
        :param is_customization_available_for_kms: (experimental) Whether the activity supports customization for kms data keys and volume keys. Default: - false
        :param is_customization_available_for_vpc: (experimental) Whether the activity supports customization for vpc subnets and vpc security groups. Default: - false
        :param athena_workgroup_names: (experimental) Names of the Athena workgroups to give query permissions. Default: - none
        :param ecr_repositories: (experimental) ECR Repositories to give image pull permissions. Default: - none
        :param glue_database_names: (experimental) Names of the Glue Databases to give permissions to search tables. Default: - none
        :param roles_to_pass: (experimental) Roles to allow passing as passed roles to actions. Default: - none
        :param s3_buckets: (experimental) S3 Buckets to give read and write permissions. Default: - none
        :param version: (experimental) Version of the SageMaker Activity. This version will be used to fetch the policy template that corresponds to the Activity. Default: - 1

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1751080a8c864f38dc30d70c8a8d7063c00eec1a7130a9b1ba7ef351eaf71c4)
            check_type(argname="argument activity_name", value=activity_name, expected_type=type_hints["activity_name"])
            check_type(argname="argument is_customization_available_for_kms", value=is_customization_available_for_kms, expected_type=type_hints["is_customization_available_for_kms"])
            check_type(argname="argument is_customization_available_for_vpc", value=is_customization_available_for_vpc, expected_type=type_hints["is_customization_available_for_vpc"])
            check_type(argname="argument athena_workgroup_names", value=athena_workgroup_names, expected_type=type_hints["athena_workgroup_names"])
            check_type(argname="argument ecr_repositories", value=ecr_repositories, expected_type=type_hints["ecr_repositories"])
            check_type(argname="argument glue_database_names", value=glue_database_names, expected_type=type_hints["glue_database_names"])
            check_type(argname="argument roles_to_pass", value=roles_to_pass, expected_type=type_hints["roles_to_pass"])
            check_type(argname="argument s3_buckets", value=s3_buckets, expected_type=type_hints["s3_buckets"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "activity_name": activity_name,
            "is_customization_available_for_kms": is_customization_available_for_kms,
            "is_customization_available_for_vpc": is_customization_available_for_vpc,
        }
        if athena_workgroup_names is not None:
            self._values["athena_workgroup_names"] = athena_workgroup_names
        if ecr_repositories is not None:
            self._values["ecr_repositories"] = ecr_repositories
        if glue_database_names is not None:
            self._values["glue_database_names"] = glue_database_names
        if roles_to_pass is not None:
            self._values["roles_to_pass"] = roles_to_pass
        if s3_buckets is not None:
            self._values["s3_buckets"] = s3_buckets
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def activity_name(self) -> builtins.str:
        '''(experimental) Name of the SageMaker Activity.

        This name will be used to name the IAM policy that is created from this Activity.

        :stability: experimental
        '''
        result = self._values.get("activity_name")
        assert result is not None, "Required property 'activity_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_customization_available_for_kms(self) -> builtins.bool:
        '''(experimental) Whether the activity supports customization for kms data keys and volume keys.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("is_customization_available_for_kms")
        assert result is not None, "Required property 'is_customization_available_for_kms' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def is_customization_available_for_vpc(self) -> builtins.bool:
        '''(experimental) Whether the activity supports customization for vpc subnets and vpc security groups.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("is_customization_available_for_vpc")
        assert result is not None, "Required property 'is_customization_available_for_vpc' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def athena_workgroup_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Names of the Athena workgroups to give query permissions.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("athena_workgroup_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ecr_repositories(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecr_ceddda9d.IRepository]]:
        '''(experimental) ECR Repositories to give image pull permissions.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("ecr_repositories")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecr_ceddda9d.IRepository]], result)

    @builtins.property
    def glue_database_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Names of the Glue Databases to give permissions to search tables.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("glue_database_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles_to_pass(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IRole]]:
        '''(experimental) Roles to allow passing as passed roles to actions.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("roles_to_pass")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IRole]], result)

    @builtins.property
    def s3_buckets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket]]:
        '''(experimental) S3 Buckets to give read and write permissions.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("s3_buckets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket]], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Version of the SageMaker Activity.

        This version will be used to fetch the policy template that corresponds to the
        Activity.

        :default: - 1

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActivityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.KMSOptions",
    jsii_struct_bases=[],
    name_mapping={"data_keys": "dataKeys", "volume_keys": "volumeKeys"},
)
class KMSOptions:
    def __init__(
        self,
        *,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> None:
        '''
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402dd097ff5f8e27bac3d1b283e9d9a52a4d1e199c6980361fed3755f45bb6a0)
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KMSOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Persona(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.Persona",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        activities: typing.Sequence[Activity],
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param activities: 
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff7b6fb2e211fca9261f1cfdfa75f56002565704e0b62084d0e5661fe2058ff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PersonaProps(
            activities=activities,
            security_groups=security_groups,
            subnets=subnets,
            data_keys=data_keys,
            volume_keys=volume_keys,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createRole")
    def create_role(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        role_name_suffix: builtins.str,
        role_description: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) Creates role with permissions of persona.

        :param scope: the Construct scope.
        :param id: the resource id.
        :param role_name_suffix: the name suffix of the role that will be created, if empty the role will have the name of the activity.
        :param role_description: the description of the role that will be created.

        :return: - The role that is created with the permissions of the persona

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75b54702baf5603be739b4cf84ce061372a50988d4631fbbf891efb5ef4ee88)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument role_name_suffix", value=role_name_suffix, expected_type=type_hints["role_name_suffix"])
            check_type(argname="argument role_description", value=role_description, expected_type=type_hints["role_description"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createRole", [scope, id, role_name_suffix, role_description]))

    @jsii.member(jsii_name="customizeKMS")
    def customize_kms(
        self,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> None:
        '''
        :param data_keys: -
        :param volume_keys: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0053dccc128493e6c665e83a782b1db2fa49c9bab217acab79ef12040a1cb8f6)
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
        return typing.cast(None, jsii.invoke(self, "customizeKMS", [data_keys, volume_keys]))

    @jsii.member(jsii_name="customizeVPC")
    def customize_vpc(
        self,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    ) -> None:
        '''
        :param subnets: -
        :param security_groups: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89758def47973a48baacaa68477c559285a9ee4d9c9bf035fb1a933ea868ef8e)
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
        return typing.cast(None, jsii.invoke(self, "customizeVPC", [subnets, security_groups]))

    @jsii.member(jsii_name="grantPermissionsTo")
    def grant_permissions_to(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant permissions of activity to identity.

        :param identity: identity to be granted permissions.

        :return: - The grant with the permissions granted to the identity

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c313b48c638a1b5e8089730df67afd311e07dac96ffce016719a34d8a4df9e7)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantPermissionsTo", [identity]))

    @builtins.property
    @jsii.member(jsii_name="activities")
    def activities(self) -> typing.List[Activity]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[Activity], jsii.get(self, "activities"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.VPCOptions",
    jsii_struct_bases=[],
    name_mapping={"security_groups": "securityGroups", "subnets": "subnets"},
)
class VPCOptions:
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    ) -> None:
        '''(experimental) Global Condition Customization Options.

        :param security_groups: 
        :param subnets: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f6463d37755f4be1ba2f10fb2ad904c0b170b29b6f75d173647eeeacf7e6fb)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VPCOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.VisualizeExperimentsOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
    },
)
class VisualizeExperimentsOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c432f076353a82979ed16d0a2b487d982da72ca21cdd627dea83c7efcba8b3e0)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VisualizeExperimentsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.AccessAwsServicesOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
        "ecr_repositories": "ecrRepositories",
        "s3_buckets": "s3Buckets",
    },
)
class AccessAwsServicesOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        ecr_repositories: typing.Sequence[_aws_cdk_aws_ecr_ceddda9d.IRepository],
        s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
    ) -> None:
        '''(experimental) SageMaker Activity Static Function Options.

        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 
        :param ecr_repositories: 
        :param s3_buckets: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a3eb9d54e32d3dd4b8427ee7742ac8ec40e38793ccba21fc1ecbc3a84b51a5)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
            check_type(argname="argument ecr_repositories", value=ecr_repositories, expected_type=type_hints["ecr_repositories"])
            check_type(argname="argument s3_buckets", value=s3_buckets, expected_type=type_hints["s3_buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ecr_repositories": ecr_repositories,
            "s3_buckets": s3_buckets,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def ecr_repositories(self) -> typing.List[_aws_cdk_aws_ecr_ceddda9d.IRepository]:
        '''
        :stability: experimental
        '''
        result = self._values.get("ecr_repositories")
        assert result is not None, "Required property 'ecr_repositories' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_ecr_ceddda9d.IRepository], result)

    @builtins.property
    def s3_buckets(self) -> typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''
        :stability: experimental
        '''
        result = self._values.get("s3_buckets")
        assert result is not None, "Required property 's3_buckets' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessAwsServicesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.AccessS3AllResourcesOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
    },
)
class AccessS3AllResourcesOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4fd646172839ba20a1cc1ae766ac7cba561a3e242ed365a9d5602e4d3a8b05)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessS3AllResourcesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.AccessS3AllResourcesV2Options",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
    },
)
class AccessS3AllResourcesV2Options(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc10e6e17a946a42fbd6145935fd2a17782a0c0508a9561d381342af2da6fd2)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessS3AllResourcesV2Options(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.AccessS3BucketsOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
        "s3_buckets": "s3Buckets",
    },
)
class AccessS3BucketsOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 
        :param s3_buckets: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddaf9da5e18e6422ea8ac1de0df423474bfd9c8352247b769cc1dc025cd50dea)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
            check_type(argname="argument s3_buckets", value=s3_buckets, expected_type=type_hints["s3_buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_buckets": s3_buckets,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def s3_buckets(self) -> typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''
        :stability: experimental
        '''
        result = self._values.get("s3_buckets")
        assert result is not None, "Required property 's3_buckets' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessS3BucketsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.ManageEndpointsOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
    },
)
class ManageEndpointsOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f32d55d81af02925d79d73d397039be38e89796a6ec301b31ab7bc7bfa178a6)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManageEndpointsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.ManageExperimentsOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
    },
)
class ManageExperimentsOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c5425aa8721dee1ff36b66a498d8d7be556fd569bb578d27fc906fbae6138e)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManageExperimentsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.ManageGlueTablesOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
        "glue_database_names": "glueDatabaseNames",
        "s3_buckets": "s3Buckets",
    },
)
class ManageGlueTablesOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        glue_database_names: typing.Sequence[builtins.str],
        s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 
        :param glue_database_names: 
        :param s3_buckets: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc820b3ad5f1bd550482bd6d9c326f836cb961deae9fdc66810892e2938540b9)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
            check_type(argname="argument glue_database_names", value=glue_database_names, expected_type=type_hints["glue_database_names"])
            check_type(argname="argument s3_buckets", value=s3_buckets, expected_type=type_hints["s3_buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "glue_database_names": glue_database_names,
            "s3_buckets": s3_buckets,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def glue_database_names(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("glue_database_names")
        assert result is not None, "Required property 'glue_database_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def s3_buckets(self) -> typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''
        :stability: experimental
        '''
        result = self._values.get("s3_buckets")
        assert result is not None, "Required property 's3_buckets' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManageGlueTablesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.ManageJobsOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
        "roles_to_pass": "rolesToPass",
    },
)
class ManageJobsOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 
        :param roles_to_pass: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e28a29e72c3604a9bdfe78402def358f07d48a8ad436f0f426ca7a4c0327f8)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
            check_type(argname="argument roles_to_pass", value=roles_to_pass, expected_type=type_hints["roles_to_pass"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "roles_to_pass": roles_to_pass,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def roles_to_pass(self) -> typing.List[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''
        :stability: experimental
        '''
        result = self._values.get("roles_to_pass")
        assert result is not None, "Required property 'roles_to_pass' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManageJobsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.ManageModelsOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
        "roles_to_pass": "rolesToPass",
    },
)
class ManageModelsOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 
        :param roles_to_pass: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__792f2d21ec2cad93908786a19854968d62166b9fa74c212a32e2843f8f262343)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
            check_type(argname="argument roles_to_pass", value=roles_to_pass, expected_type=type_hints["roles_to_pass"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "roles_to_pass": roles_to_pass,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def roles_to_pass(self) -> typing.List[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''
        :stability: experimental
        '''
        result = self._values.get("roles_to_pass")
        assert result is not None, "Required property 'roles_to_pass' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManageModelsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.ManagePipelinesOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
        "roles_to_pass": "rolesToPass",
    },
)
class ManagePipelinesOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 
        :param roles_to_pass: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631c159b01f847741dab15f600287e4a5e57dcd51168ce763832b397dd665b37)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
            check_type(argname="argument roles_to_pass", value=roles_to_pass, expected_type=type_hints["roles_to_pass"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "roles_to_pass": roles_to_pass,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def roles_to_pass(self) -> typing.List[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''
        :stability: experimental
        '''
        result = self._values.get("roles_to_pass")
        assert result is not None, "Required property 'roles_to_pass' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagePipelinesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.MonitorModelsOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
        "roles_to_pass": "rolesToPass",
    },
)
class MonitorModelsOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 
        :param roles_to_pass: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85e85e877f6db74c18bdf4a8f17331a199afc2afdf9343f68dc535ce88cfd7a)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
            check_type(argname="argument roles_to_pass", value=roles_to_pass, expected_type=type_hints["roles_to_pass"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "roles_to_pass": roles_to_pass,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def roles_to_pass(self) -> typing.List[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''
        :stability: experimental
        '''
        result = self._values.get("roles_to_pass")
        assert result is not None, "Required property 'roles_to_pass' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorModelsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.PersonaProps",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
        "activities": "activities",
    },
)
class PersonaProps(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        activities: typing.Sequence[Activity],
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 
        :param activities: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db2e578a2eafcd312959deaf78bb58bbba7eca3b956ad2540e3220ac122e8427)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
            check_type(argname="argument activities", value=activities, expected_type=type_hints["activities"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "activities": activities,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def activities(self) -> typing.List[Activity]:
        '''
        :stability: experimental
        '''
        result = self._values.get("activities")
        assert result is not None, "Required property 'activities' is missing"
        return typing.cast(typing.List[Activity], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PersonaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.QueryAthenaGroupsOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
        "athena_workgroup_names": "athenaWorkgroupNames",
    },
)
class QueryAthenaGroupsOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        athena_workgroup_names: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 
        :param athena_workgroup_names: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f81aab019e9ebef1640fdc4ae237a8ba7d58652911fd0e06922f11b48348b9)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
            check_type(argname="argument athena_workgroup_names", value=athena_workgroup_names, expected_type=type_hints["athena_workgroup_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "athena_workgroup_names": athena_workgroup_names,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def athena_workgroup_names(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("athena_workgroup_names")
        assert result is not None, "Required property 'athena_workgroup_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueryAthenaGroupsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.RunStudioAppsOptions",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
        "roles_to_pass": "rolesToPass",
    },
)
class RunStudioAppsOptions(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 
        :param roles_to_pass: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a76f07fabed4a579ec71b0dcd7ca0615552c47a5546c4df01b7e2fc4fb2cb0a7)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
            check_type(argname="argument roles_to_pass", value=roles_to_pass, expected_type=type_hints["roles_to_pass"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "roles_to_pass": roles_to_pass,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def roles_to_pass(self) -> typing.List[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''
        :stability: experimental
        '''
        result = self._values.get("roles_to_pass")
        assert result is not None, "Required property 'roles_to_pass' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunStudioAppsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-aws-sagemaker-role-manager.RunStudioAppsV2Options",
    jsii_struct_bases=[VPCOptions, KMSOptions],
    name_mapping={
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "data_keys": "dataKeys",
        "volume_keys": "volumeKeys",
    },
)
class RunStudioAppsV2Options(VPCOptions, KMSOptions):
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
        data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ) -> None:
        '''
        :param security_groups: 
        :param subnets: 
        :param data_keys: 
        :param volume_keys: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89484abf6a51c6866662a6ad3e1b3868222adb6103666225dc855889128f217)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument data_keys", value=data_keys, expected_type=type_hints["data_keys"])
            check_type(argname="argument volume_keys", value=volume_keys, expected_type=type_hints["volume_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if data_keys is not None:
            self._values["data_keys"] = data_keys
        if volume_keys is not None:
            self._values["volume_keys"] = volume_keys

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]], result)

    @builtins.property
    def data_keys(self) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("data_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def volume_keys(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_keys")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunStudioAppsV2Options(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccessAwsServicesOptions",
    "AccessS3AllResourcesOptions",
    "AccessS3AllResourcesV2Options",
    "AccessS3BucketsOptions",
    "Activity",
    "ActivityProps",
    "KMSOptions",
    "ManageEndpointsOptions",
    "ManageExperimentsOptions",
    "ManageGlueTablesOptions",
    "ManageJobsOptions",
    "ManageModelsOptions",
    "ManagePipelinesOptions",
    "MonitorModelsOptions",
    "Persona",
    "PersonaProps",
    "QueryAthenaGroupsOptions",
    "RunStudioAppsOptions",
    "RunStudioAppsV2Options",
    "VPCOptions",
    "VisualizeExperimentsOptions",
]

publication.publish()

def _typecheckingstub__5211c3777ff232336aa3201329facc2a3b849d0ff050e74c891cb97170a57e03(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ecr_repositories: typing.Sequence[_aws_cdk_aws_ecr_ceddda9d.IRepository],
    s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3cf760fce634375ae1e69d657af8b0eac69356533d6075aa1585bb02c1b6b7b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5237dc8d2a91e9185d52af32f0836b1f7cc405b2e72a542a1d53a1473f9f475(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a9501f4b7c33148fbdca2c97d99ccbfb392b8dbef140a6492672491626f6ae(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6daccbba48fb46e0449deee6661617129440a963c6e957addb3c68d1143ae7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ea1b48782474ec58c0488797eba73195eb32c68d57978e100e7830a8f944e1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10c97ca33fc3bd2a34e89fabcafcdfc9601fa8fb0128b34a06e8a9420432486(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    glue_database_names: typing.Sequence[builtins.str],
    s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b91203598d016304f5699d33488383a6dd29c82c4f7ef130845926284c643a3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27a4e33293089ba1b2021b356d5b22ed51d0bd58e8869e2fb15878972fa8db2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fabed52bcc484d301e66a5d93a6b9e15af716296c80fd5d8d556e86479cc1d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045936b4c21feb245b8204a6d1c83e9bf20371db9c88d643f1015494f1d954bd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8909c9ce5ca8f3f519082beb7c5a052c211296ea88a7cbbd7f9c80e0e7ad7e84(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    athena_workgroup_names: typing.Sequence[builtins.str],
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d862f363484ff7073d10e0e9a5f8cec6ad1454460d029899eb4ea5f235697d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f2dfbdf2733d397e7dcd517bd59e8ee11cc1e7c5fb92534c862f5925760876(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c536c4a818214b050cf817c4c9fb45b30e07940d9415c38cbadcabdccee18014(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284bcc1d8ec0fe9e5bde8dfe53d4ce78c8daa3a25e5dba069c16b17f43e82bf4(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3e83adeb6d741da0bba05fe17f3f8a1f095ee6a64ceee44d490bbf4a52eeeb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    role_name_suffix: builtins.str,
    role_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23b8e8f6d6e6b6c8680a7a7b6f7defe7f945d01806d254a610257b9350d2cf0(
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f395831c3296b503838d66d38e49582877c8f7e4a54aa922337c28d444357ba9(
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc551077478590cb370f7525ab06a3a96d7d813a2c57801d24e252253bd0bce(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028da7f2b1be36f4ca5c52ce78c4fd2a8a65a020a81d7e32ca8876022cce5922(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e762a9ced1e9eb46fe8d86693ca7418397f36a25cf79ff80424f929fac5ec03a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1751080a8c864f38dc30d70c8a8d7063c00eec1a7130a9b1ba7ef351eaf71c4(
    *,
    activity_name: builtins.str,
    is_customization_available_for_kms: builtins.bool,
    is_customization_available_for_vpc: builtins.bool,
    athena_workgroup_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ecr_repositories: typing.Optional[typing.Sequence[_aws_cdk_aws_ecr_ceddda9d.IRepository]] = None,
    glue_database_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles_to_pass: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole]] = None,
    s3_buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402dd097ff5f8e27bac3d1b283e9d9a52a4d1e199c6980361fed3755f45bb6a0(
    *,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff7b6fb2e211fca9261f1cfdfa75f56002565704e0b62084d0e5661fe2058ff(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    activities: typing.Sequence[Activity],
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75b54702baf5603be739b4cf84ce061372a50988d4631fbbf891efb5ef4ee88(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    role_name_suffix: builtins.str,
    role_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0053dccc128493e6c665e83a782b1db2fa49c9bab217acab79ef12040a1cb8f6(
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89758def47973a48baacaa68477c559285a9ee4d9c9bf035fb1a933ea868ef8e(
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c313b48c638a1b5e8089730df67afd311e07dac96ffce016719a34d8a4df9e7(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f6463d37755f4be1ba2f10fb2ad904c0b170b29b6f75d173647eeeacf7e6fb(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c432f076353a82979ed16d0a2b487d982da72ca21cdd627dea83c7efcba8b3e0(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a3eb9d54e32d3dd4b8427ee7742ac8ec40e38793ccba21fc1ecbc3a84b51a5(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    ecr_repositories: typing.Sequence[_aws_cdk_aws_ecr_ceddda9d.IRepository],
    s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4fd646172839ba20a1cc1ae766ac7cba561a3e242ed365a9d5602e4d3a8b05(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc10e6e17a946a42fbd6145935fd2a17782a0c0508a9561d381342af2da6fd2(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddaf9da5e18e6422ea8ac1de0df423474bfd9c8352247b769cc1dc025cd50dea(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f32d55d81af02925d79d73d397039be38e89796a6ec301b31ab7bc7bfa178a6(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c5425aa8721dee1ff36b66a498d8d7be556fd569bb578d27fc906fbae6138e(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc820b3ad5f1bd550482bd6d9c326f836cb961deae9fdc66810892e2938540b9(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    glue_database_names: typing.Sequence[builtins.str],
    s3_buckets: typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e28a29e72c3604a9bdfe78402def358f07d48a8ad436f0f426ca7a4c0327f8(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792f2d21ec2cad93908786a19854968d62166b9fa74c212a32e2843f8f262343(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631c159b01f847741dab15f600287e4a5e57dcd51168ce763832b397dd665b37(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85e85e877f6db74c18bdf4a8f17331a199afc2afdf9343f68dc535ce88cfd7a(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2e578a2eafcd312959deaf78bb58bbba7eca3b956ad2540e3220ac122e8427(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    activities: typing.Sequence[Activity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f81aab019e9ebef1640fdc4ae237a8ba7d58652911fd0e06922f11b48348b9(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    athena_workgroup_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76f07fabed4a579ec71b0dcd7ca0615552c47a5546c4df01b7e2fc4fb2cb0a7(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    roles_to_pass: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89484abf6a51c6866662a6ad3e1b3868222adb6103666225dc855889128f217(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnets: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISubnet]] = None,
    data_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    volume_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
) -> None:
    """Type checking stubs"""
    pass
