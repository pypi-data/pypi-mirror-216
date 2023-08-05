from collections import OrderedDict
from typing import Any
from typing import Dict


def convert_raw_k8s_cluster_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """
    Util function to convert raw resource state from AWS K8s Cluster to present input format.
    """

    resource_id = raw_resource.get("id")
    resource_parameters = OrderedDict(
        {
            "name": "name",
            "controllerClusterId": "controller_cluster_id",
            "region": "region",
            "capacity": "capacity",
            "compute": "compute",
            "logging": "logging",
            "scheduling": "scheduling",
            "security": "security",
            "strategy": "strategy",
            "autoScaler": "auto_scaler",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    return resource_translated


def convert_raw_launch_spec_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """
    Util function to convert raw resource state from AWS Launch Spec to present input format.
    """

    resource_id = raw_resource.get("id")
    resource_parameters = OrderedDict(
        {
            "name": "name",
            "taints": "taints",
            "tags": "tags",
            "subnetIds": "subnet_ids",
            "userData": "user_data",
            "securityGroupIds": "security_group_ids",
            "rootVolumeSize": "root_volume_size",
            "strategy": "strategy",
            "restrictScaleDown": "restrict_scale_down",
            "resourceLimits": "resource_limits",
            "oceanId": "ocean_id",
            "labels": "labels",
            "instanceTypes": "instance_types",
            "imageId": "image_id",
            "iamInstanceProfile": "iam_instance_profile",
            "blockDeviceMappings": "block_device_mappings",
            "elasticIpPool": "elastic_ip_pool",
            "preferredSpotTypes": "preferred_spot_types",
            "autoScale": "auto_scale",
            "associatePublicIpAddress": "associateP_public_ip_address",
            "scheduling": "scheduling",
            "instanceMetadataOptions": "instance_metadata_options",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated
