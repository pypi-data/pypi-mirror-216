"""State module for managing Ocean AWS LaunchSpec."""
import base64
import copy
import json
from typing import Any
from typing import Dict
from typing import List

import dict_tools.differ as differ

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    image_id: str,
    ocean_id: str,
    resource_id: str = None,
    iam_instance_profile: Dict = None,
    taints: List = None,
    tags: List = None,
    subnet_ids: List = None,
    user_data: str = None,
    security_group_ids: List = None,
    root_volume_size: int = None,
    strategy: Dict = None,
    restrict_scale_down: bool = None,
    resource_limits: Dict = None,
    labels: List = None,
    instance_types: List = None,
    preferred_spot_types: List = None,
    elastic_ip_pool: Dict = None,
    auto_scale: Dict = None,
    block_device_mappings: List = None,
    associate_public_ip_address: bool = None,
    scheduling: Dict = None,
    instance_metadata_options: Dict = None,
) -> Dict[str, Any]:
    """Create a Launch Spec(Virtual Node Group).

    Refer the `Spot Create Launch Spec(Virtual Node Group) documentation <https://docs.spot.io/api/#operation/OceanAWSLaunchSpecCreate>`_
    to get insight of functionality and input parameters

    Args:
         name(str): launch specification name.
         image_id(str): AWS image identifier.
         ocean_id(str): The Ocean cluster identifier. Required for Launch Spec creation
         resource_id(str, Optional): The virtual node group identifier.
         iam_instance_profile(dict, Optional): The instance profile iamRole object.
         taints(list, Optional): Add taints to Launch Spec.
         tags(list, Optional): List of kay-value pairs of tags.
         subnet_ids(list, Optional): Set subnets in launchSpec. Each element in the array is a subnet identifier.
         user_data(str, Optional): Set user data script.
         security_group_ids(list, Optional): Set security groups. Each element in the array is a security group identifier.
         root_volume_size(int, Optional): Set root volume size (in GB). This field and blockDeviceMappings cannot be used in the same specification.
         strategy(dict, Optional): Similar to a strategy for an Ocean cluster, but applying only to a virtual node group.
         restrict_scale_down(bool, Optional): When set to “True”, VNG nodes will be treated as if all pods running have the restrict-scale-down label. Therefore, Ocean will not scale nodes down unless empty.
         resource_limits(dict, Optional): Option to set a maximum/minimum number of instances per launch specification.
         labels(list, Optional): An array of labels to add to the VNG nodes. Only custom user labels are allowed, and not Kubernetes built-in labels or Spot internal labels.
         instance_types(list, Optional): A list of instance types allowed to be provisioned for pods pending for the launch specification.
         preferred_spot_types(list, Optional): When Ocean scales up instances, it takes your preferred types into consideration while maintaining a variety of machine types running for optimized distribution.
         elastic_ip_pool(dict, Optional): Assign an Elastic IP to the instances launched by the launch spec.
         auto_scale(dict, Optional): Object specifying the automatic scaling of an Ocean VNG.
         block_device_mappings(list, Optional):
            Block devices that are exposed to the instance. You can specify virtual devices and EBS volumes.
            This parameter and rootVolumeSize cannot be in the spec at the same time.
            This parameter can be null, but if not null, it must contain at least one block device.
         associate_public_ip_address(bool, Optional): Configure public IP address allocation.
         scheduling(dict, Optional): An object used to define scheduled tasks such as a manual headroom update.
         instance_metadata_options(dict, Optional): Ocean instance metadata options object for IMDSv2.

    Request Syntax:
        .. code-block:: sls

            [spotinst.ocean.aws.launch_spec-resource-id]:
                spotinst.ocean.aws.launch_spec.present:
                   - name: 'string'
                   - resource_id: 'string'
                   - taints:
                     - effect: 'string'
                       key: 'string'
                       value: 'string'
                   - tags:
                     - tagKey: 'string'
                       tagValue: 'string'
                     - tagKey: 'string'
                       tagValue: 'string'
                   - subnet_ids:
                     - 'string'
                   - user_data: 'string'
                   - security_group_ids:
                     - 'string'
                   - root_volume_size: Integer
                   - resource_limits:
                       maxInstanceCount: Integer
                   - ocean_id: 'string'
                   - labels:
                     - key: 'string'
                       value: 'string'
                     - key: 'string'
                       value: 'string'
                   - instance_types:
                     - 'string'
                   - image_id: 'string'
                   - iam_instance_profile:
                       arn: 'string'
                   - associate_public_ip_address: true/false
                   - preferred_spot_types:
                     - 'string'
                   - elastic_ip_pool:
                       tagSelector:
                         tagKey: 'string'
                         tagValue: 'string'
                   - auto_scale:
                       headrooms:
                        - cpuPerUnit: Integer
                          memoryPerUnit: Integer
                          numOfUnits: Integer
                   - block_device_mappings:
                    - deviceName: 'string'
                      ebs:
                        deleteOnTermination: true/false
                        encrypted: true/false
                        volumeSize: Integer
                        volumeType: 'string'
                    - scheduling:
                        tasks:
                          - isEnabled: true/false
                            cronExpression: 'string'
                            taskType: 'string'
                        shutdownHours:
                          timeWindows:
                            - 'string'
                        isEnabled: true/false
                    - instanceMetadataOptions:
                                httpTokens: 'string'
                                httpPutResponseHopLimit: Integer

    Returns:
         Dict[str, Any]

    Examples:
         .. code-block:: sls

             ols-77e27034:
               spotinst.ocean.aws.launch_spec.present:
               - name: cluster-arm
               - resource_id: ols-77e27034
               - taints:
                 - effect: NoSchedule
                   key: dedicated
                   value: idem-test-value
               - tags:
                 - tagKey: tag-key-1
                   tagValue: tag-value-1
                 - tagKey: tag-key-2
                   tagValue: tag-value-2
               - subnet_ids:
                 - subnet-111122223333abcd
                 - subnet-444455556666abcd
               - user_data: /etc/eks/idem-test.sh
               - security_group_ids:
                 - sg-111122223333abcd
                 - sg-444455556666abcd
               - root_volume_size: 8
               - resource_limits:
                   maxInstanceCount: 1
               - ocean_id: o-b78b1d69
               - labels:
                 - key: autoscale
                   value: 'false'
                 - key: dedicated
                   value: idem-test-value
               - instance_types:
                 - t2.micro
               - image_id: ami-111122223333abcd
               - iam_instance_profile:
                   arn: arn:aws:iam::111122223333:instance-profile/spotinst-eks-stack-NodeInstanceProfile
               - auto_scale:
                   headrooms:
                    - cpuPerUnit: 1024
                      memoryPerUnit: 512
                      numOfUnits: 3
               - block_device_mappings:
                - deviceName: /dev/xvda
                  ebs:
                    deleteOnTermination: true
                    encrypted: true
                    volumeSize: 30
                    volumeType: gp2
                - scheduling:
                    tasks:
                      - isEnabled: true
                        cronExpression: '0 1 * * *'
                        taskType: manualHeadroomUpdate
                    shutdownHours:
                      timeWindows:
                        - "Sat:08:00-Sun:08:00"
                    isEnabled: true
                - instanceMetadataOptions:
                            httpTokens: optional
                            httpPutResponseHopLimit: 12

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    user_data_base64 = None
    if user_data:
        try:
            user_data_base64 = base64.b64encode(user_data.encode("utf-8")).decode(
                "utf-8"
            )
        except UnicodeError as e:
            hub.log.debug(f"base 64 encoding failed for user_data {e}")
            result["result"] = False
            result["comment"] = (f"{e.__class__.__name__}: {e}",)
            return result

    data = {
        "launchSpec": {
            "name": name,
            "taints": taints,
            "tags": tags,
            "subnetIds": subnet_ids,
            "userData": user_data_base64,
            "securityGroupIds": security_group_ids,
            "strategy": strategy,
            "restrictScaleDown": restrict_scale_down,
            "resourceLimits": resource_limits,
            "labels": labels,
            "instanceTypes": instance_types,
            "imageId": image_id,
            "iamInstanceProfile": iam_instance_profile,
            "elasticIpPool": elastic_ip_pool,
            "preferredSpotTypes": preferred_spot_types,
            "autoScale": auto_scale,
            "associatePublicIpAddress": associate_public_ip_address,
            "scheduling": scheduling,
            "instanceMetadataOptions": instance_metadata_options,
        }
    }

    # blockDeviceMappings and rootVolumeSize cannot be in the spec at the same time
    if block_device_mappings:
        data["launchSpec"]["blockDeviceMappings"] = block_device_mappings
    else:
        data["launchSpec"]["rootVolumeSize"] = root_volume_size

    resource_parameters = {
        "taints": taints,
        "tags": tags,
        "subnet_ids": subnet_ids,
        "user_data": user_data_base64,
        "security_group_ids": security_group_ids,
        "root_volume_size": root_volume_size,
        "strategy": strategy,
        "restrict_scale_down": restrict_scale_down,
        "resource_limits": resource_limits,
        "ocean_id": ocean_id,
        "labels": labels,
        "instance_types": instance_types,
        "image_id": image_id,
        "iam_instance_profile": iam_instance_profile,
        "elastic_ip_pool": elastic_ip_pool,
        "preferred_spot_types": preferred_spot_types,
        "auto_scale": auto_scale,
        "block_device_mappings": block_device_mappings,
        "associate_public_ip_address": associate_public_ip_address,
        "scheduling": scheduling,
        "instance_metadata_options": instance_metadata_options,
    }

    desire_state = {"name": name, "resource_id": resource_id}
    for parameter_key, parameter_value in resource_parameters.items():
        if parameter_value is not None:
            desire_state[parameter_key] = parameter_value

    before = None
    if resource_id:
        get_url = f"{hub.exec.spotinst.URL}/ocean/aws/k8s/launchSpec/{resource_id}?accountId={ctx.acct.account_id}"
        ret = await hub.exec.request.json.get(
            ctx,
            url=get_url,
            success_codes=[200],
            headers={"Authorization": f"Bearer {ctx.acct.token}"},
        )
        if not ret["result"]:
            if ret["status"] == 400:
                result["comment"] = (
                    f"spotinst.ocean.aws.launch_spec '{name}'(resource Id: '{resource_id}') not found",
                )  # In case of non-existance resource id, comment returns ' Bad Request'
            else:
                result["comment"] = ret["comment"]
            result["result"] = ret["result"]
            return result

        if ret["ret"].get("response").get("items"):
            before = ret["ret"].get("response").get("items")[0]

    if before:
        result[
            "old_state"
        ] = hub.tool.spotinst.ocean.aws.conversion_utils.convert_raw_launch_spec_to_present(
            raw_resource=before,
            idem_resource_name=resource_id,
        )
        desire_state = hub.tool.spotinst.state_utils.handle_null(
            desire_state=desire_state, current_state=result["old_state"]
        )
        diff = hub.tool.spotinst.state_comparison_utils.deep_diff(
            result["old_state"].copy(), desire_state.copy(), ignore="tags"
        )
        update_required = False
        if diff and "desire_state" in diff:
            for item in diff["desire_state"]:
                if diff["desire_state"].get(item):  # if value is not None
                    update_required = True

        is_tags_updated = hub.tool.spotinst.ocean.aws.tag_utils.is_update_required(
            old_tags_list=result["old_state"].get("tags"),
            new_tags_list=desire_state.get("tags"),
        )
        update_required = update_required or is_tags_updated

        if update_required:
            if ctx.get("test", False):
                result["new_state"] = desire_state
                result[
                    "comment"
                ] = hub.tool.spotinst.comment_utils.would_update_comment(
                    resource_type="spotinst.ocean.aws.launch_spec", name=resource_id
                )
                return result
            # Update in real
            try:
                ret = await hub.exec.request.json.put(
                    ctx,
                    success_codes=[200],
                    headers={"Authorization": f"Bearer {ctx.acct.token}"},
                    url=f"{hub.exec.spotinst.URL}/ocean/aws/k8s/launchSpec/{resource_id}?accountId={ctx.acct.account_id}",
                    data=json.dumps(data),
                )
            except Exception as e:
                hub.log.debug(f"Could not update spotinst.ocean.aws.launch_spec {e}")
                result["result"] = False
                result["comment"] = (f"{e.__class__.__name__}: {e}",)
                return result

            if not ret["result"]:
                errors = json.loads(ret["ret"]).get("response").get("errors")
                if errors:
                    result["comment"] = (
                        ret["comment"],
                        errors[0].get("message"),
                    )
                else:
                    result["comment"] = ret["comment"]
                result["result"] = False
                return result

            result[
                "new_state"
            ] = hub.tool.spotinst.ocean.aws.conversion_utils.convert_raw_launch_spec_to_present(
                raw_resource=ret["ret"].get("response").get("items")[0],
                idem_resource_name=name,
            )
            result[
                "comment"
            ] = f"Updated spotinst.ocean.aws.launch_spec Id: '{resource_id}')"
        else:
            result["comment"] = hub.tool.spotinst.comment_utils.already_present_comment(
                resource_type="spotinst.ocean.aws.launch_spec",
                name=name,
                resource_id=resource_id,
            )
            result["new_state"] = copy.deepcopy(result["old_state"])
            return result
    else:  # create new resource
        if ctx.get("test", False):
            # For test we should add resource_id
            if desire_state.get("resource_id", None) is None:
                desire_state["resource_id"] = "resource_id_known_after_present"
            result["new_state"] = desire_state
            result["comment"] = hub.tool.spotinst.comment_utils.would_create_comment(
                resource_type="spotinst.ocean.aws.launch_spec", name=name
            )
            return result
        # create in real
        data.get("launchSpec")["oceanId"] = ocean_id
        try:
            ret = await hub.exec.request.json.post(
                ctx,
                success_codes=[200],
                headers={"Authorization": f"Bearer {ctx.acct.token}"},
                url=f"{hub.exec.spotinst.URL}/ocean/aws/k8s/launchSpec?accountId={ctx.acct.account_id}",
                data=json.dumps(data),
            )
        except Exception as e:
            hub.log.debug(f"Could not create spotinst.ocean.aws.launch_spec {e}")
            result["result"] = False
            result["comment"] = (f"{e.__class__.__name__}: {e}",)
            return result

        if not ret["result"]:
            errors = json.loads(ret["ret"]).get("response").get("errors")
            if errors:
                result["comment"] = (
                    ret["comment"],
                    errors[0].get("message"),
                )
            else:
                result["comment"] = ret["comment"]
            result["result"] = False
            return result

        result[
            "new_state"
        ] = hub.tool.spotinst.ocean.aws.conversion_utils.convert_raw_launch_spec_to_present(
            raw_resource=ret["ret"].get("response").get("items")[0],
            idem_resource_name=name,
        )

        result["comment"] = hub.tool.spotinst.comment_utils.create_comment(
            resource_type="spotinst.ocean.aws.launch_spec", name=name
        )

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified launch Spec.

    When this call completes, the launch configuration is no longer available for use.

    Refer the `Spot Delete Launch Spec(Virtual Node Group) documentation <https://docs.spot.io/api/#operation/OceanAWSLaunchSpecDelete>`_
    to get insight of functionality and input parameters


    Args:
        name(str): An idem name of the launch spec.
        resource_id(str, Optional): The AWS ID of the launch spec.

    Request Syntax:
         .. code-block:: sls

           [launch_spec-resource-id]:
                  spotinst.ocean.aws.launch_spec.absent:
                  - name: 'string'
                  - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-test-launch_spec:
              spotinst.ocean.aws.launch_spec.absent:
                - name: idem-test-launch_spec
                - resource_id: idem-test-launch_spec

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.spotinst.comment_utils.already_absent_comment(
            resource_type="spotinst.ocean.aws.launch_spec", name=name
        )
        return result

    url = f"{hub.exec.spotinst.URL}/ocean/aws/k8s/launchSpec/{resource_id}?accountId={ctx.acct.account_id}"
    before = None
    try:
        before = await hub.exec.request.json.get(
            ctx,
            url=url,
            success_codes=[200],
            headers={"Authorization": f"Bearer {ctx.acct.token}"},
        )
    except Exception as e:
        hub.log.debug(f"Could not get Launch Spec {e}")
        result["result"] = False
        result["comment"] = (f"{e.__class__.__name__}: {e}",)
        return result

    if before["status"] == 400:
        result["comment"] = hub.tool.spotinst.comment_utils.already_absent_comment(
            resource_type="spotinst.ocean.aws.launch_spec", name=name
        )
    elif before["result"]:
        result[
            "old_state"
        ] = hub.tool.spotinst.ocean.aws.conversion_utils.convert_raw_launch_spec_to_present(
            raw_resource=before["ret"].get("response").get("items")[0],
            idem_resource_name=name,
        )

        if ctx.get("test", False):
            result["comment"] = hub.tool.spotinst.comment_utils.would_delete_comment(
                resource_type="spotinst.ocean.aws.launch_spec", name=name
            )
            return result
        try:
            ret = await hub.exec.request.json.delete(
                ctx,
                url=url,
                success_codes=[200],
                headers={"Authorization": f"Bearer {ctx.acct.token}"},
            )
            result["result"] = ret["result"]
            if not result["result"]:
                hub.log.debug(
                    f"Could not delete spotinst.ocean.aws.launch_spec {result['comment']} {result['ret']}"
                )
                result["comment"] = ret["comment"]
                return result

            result["comment"] = hub.tool.spotinst.comment_utils.delete_comment(
                resource_type="spotinst.ocean.aws.launch_spec", name=name
            )
        except Exception as e:
            hub.log.debug(f"Could not delete spotinst.ocean.aws.launch_spec {e}")
            result["result"] = False
            result["comment"] = (f"{e.__class__.__name__}: {e}",)
            return result
    else:
        hub.log.debug(f"Could not get Launch Spec {before['comment']} {before['ret']}")
        result["result"] = False
        result["comment"] = before["comment"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Gets information about the virtual node groups for the cluster.

    Please refer the `Spot Listing Launch Spec(Virtual Node Group) documentation <https://docs.spot.io/api/#operation/OceanAWSLaunchSpecList>`_ to get insight of functionality and input parameters

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe spotinst.ocean.aws.launch_spec

    """
    result = {}

    url = f"{hub.exec.spotinst.URL}/ocean/aws/k8s/launchSpec?accountId={ctx.acct.account_id}"
    ret = await hub.exec.request.json.get(
        ctx,
        url=url,
        success_codes=[200],
        headers={"Authorization": f"Bearer {ctx.acct.token}"},
    )

    if not ret["result"]:
        hub.log.debug(f"Could not describe launch_spec {ret['comment']}")
        return {}

    for launch_spec_item in ret["ret"].get("response").get("items"):
        resource_id = launch_spec_item.get("id")
        resource_translated = hub.tool.spotinst.ocean.aws.conversion_utils.convert_raw_launch_spec_to_present(
            raw_resource=launch_spec_item, idem_resource_name=resource_id
        )
        result[resource_id] = {
            "spotinst.ocean.aws.launch_spec.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
