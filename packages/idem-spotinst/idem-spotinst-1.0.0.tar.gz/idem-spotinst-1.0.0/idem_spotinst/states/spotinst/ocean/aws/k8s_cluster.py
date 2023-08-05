"""State module for managing Ocean AWS k8s cluster."""
import base64
import copy
import json
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    controller_cluster_id: str,
    region: str,
    compute: Dict = None,
    resource_id: str = None,
    capacity: Dict = None,
    logging: Dict = None,
    scheduling: Dict = None,
    security: Dict = None,
    strategy: Dict = None,
    auto_scaler=None,
    update_policy: Dict = None,
) -> Dict[str, Any]:
    """Create a Ocean k8s Cluster.

    Refer the `Spot Create Ocean Cluster documentation <https://docs.spot.io/api/#operation/OceanAWSClusterCreate>`_
    to get insight of functionality and input parameters

    Args:

        name(str): ocean cluster name.
        resource_id(str, Optional): The ocean cluster identifier.
        auto_scaler(dict, Optional): The automatic scaling mechanism used in Ocean for Kubernetes.
        capacity (dict, Optional):
            The overall capability of the Ocean cluster expressed as number of instances and specified with a minimum,
            a maximum, and a target number of running instances.
        compute (dict, Optional):
            Compute specifications for the Ocean cluster. This is required for greenfield and optional for brownfield.
        controller_cluster_id(str): Reporting identifier for the Ocean Controller.
        logging	(dict, Optional):  Logging configuration for ocean aws cluster.
        region(str): Region for the Ocean cluster to run in.
        scheduling(dict, Optional)	: An object used to define times for a task such as a shutdown to be activated.
        security(dict, Optional): Object for cluster security features.
        strategy(dict, Optional):
            An object defining the cluster strategy with regard to waiting periods
            and utilization of on-demand and reserved instances.
        update_policy(dict, Optional): Configures the cluster update policy.
            You can configure to start the roll on update and run it in defined batches.

    Request Syntax:
        .. code-block:: sls

            [spotinst.ocean.aws.k8s_cluster-state-id]:
               spotinst.ocean.aws.k8s_cluster.present:
                  - name: 'string'
                  - controller_cluster_id: 'string'
                  - region: 'string'
                  - update_policy:
                      shouldRoll: boolean
                      roll:
                         batchSizePercentage: Integer
                         comment: 'string'
                         batchMinHealthyPercentage: Integer
                  - compute:
                      launchSpecification:
                        keyPair: 'string'
                        imageId: 'string'
                        associatePublicIpAddress: boolean
                        rootVolumeSize: Integer
                        iamInstanceProfile:
                            arn: 'string'
                        userData: 'string'
                        tags:
                        - tagKey: 'string'
                          tagValue: 'string'
                        - tagKey: 'string'
                          tagValue: 'string'
                        securityGroupIds:
                            - 'string'
                      subnetIds:
                         - 'string'
                      instanceTypes:
                        whitelist:
                        - 'string'
                  - strategy:
                      fallbackToOd: boolean
                      spotPercentage: Integer
                      utilizeReservedInstances: boolean
                  - auto_scaler:
                      isEnabled: boolean
                      isAutoConfig: boolean
                      cooldown: Integer
                      headroom:
                        cpuPerUnit: Integer
                        memoryPerUnit: Integer
                        numOfUnits: Integer
                      down:
                        maxScaleDownPercentage: Integer
                  - resourceLimits:
                      maxMemoryGib: Integer
                      maxVCpu: Integer
                  - capacity:
                      maximum: Integer
                      minimum: Integer

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            ocean_cluster:
              spotinst.ocean.aws.k8s_cluster.present:
              - name: idem-test
              - controller_cluster_id: idem-test
              - region: ap-east-1
              - update_policy:
                  shouldRoll: false
                  roll:
                     batchSizePercentage: 30
                     comment: Idem cluster roll testing
                     batchMinHealthyPercentage: 100
              - compute:
                  launchSpecification:
                    keyPair: test-idem-key
                    imageId: ami-06c9598a8dcd87e79
                    associatePublicIpAddress: False
                    rootVolumeSize: 100
                    iamInstanceProfile:
                        arn: arn:aws:iam::111222333:instance-profile/idem-instance-profile-test
                    userData: |
                            #!/bin/bash -xe
                            /etc/eks/test-idem.sh
                    tags:
                    - tagKey: tag-ket-1
                      tagValue: tag-value-1
                    - tagKey: tag-ket-2
                      tagValue: tag-value-2
                    securityGroupIds:
                        - sg-qbc111122223333
                  subnetIds:
                     - subnet-0abc111222333
                  instanceTypes:
                    whitelist:
                    - c5.large
              - strategy:
                  fallbackToOd: true
                  spotPercentage: 100
                  utilizeReservedInstances: true
              - auto_scaler:
                  isEnabled: True
                  isAutoConfig: true
                  cooldown: 300
                  headroom:
                    cpuPerUnit: 1024
                    memoryPerUnit: 512
                    numOfUnits: 3
                  down:
                    maxScaleDownPercentage: 60
                  resourceLimits:
                    maxMemoryGib: 20000
                    maxVCpu: 100000
              - capacity:
                  maximum: 1000
                  minimum: 1

    """
    if auto_scaler is None:
        auto_scaler = {}
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # If userdata is set in compute, encode userData to base64
    if (
        compute
        and compute.get("launchSpecification")
        and compute.get("launchSpecification").get("userData")
    ):
        try:
            user_data_bytes = (
                compute.get("launchSpecification").get("userData").encode("utf-8")
            )
            base64_string = base64.b64encode(user_data_bytes).decode("utf-8")
            compute["launchSpecification"]["userData"] = base64_string
        except UnicodeError as e:
            hub.log.debug(f"base 64 encoding failed for user_data {e}")
            result["result"] = False
            result["comment"] = (f"{e.__class__.__name__}: {e}",)
            return result

    data = {
        "cluster": {
            "name": name,
            "capacity": capacity,
            "compute": compute,
            "controllerClusterId": controller_cluster_id,
            "logging": logging,
            "scheduling": scheduling,
            "security": security,
            "strategy": strategy,
        }
    }

    if auto_scaler:
        data["cluster"]["autoScaler"] = auto_scaler

    resource_parameters = {
        "capacity": capacity,
        "compute": compute,
        "controller_cluster_id": controller_cluster_id,
        "logging": logging,
        "region": region,
        "scheduling": scheduling,
        "security": security,
        "strategy": strategy,
        "auto_scaler": auto_scaler,
    }

    desire_state = {"name": name, "resource_id": resource_id}
    for parameter_key, parameter_value in resource_parameters.items():
        if parameter_value is not None:
            desire_state[parameter_key] = parameter_value

    before = None

    if resource_id:
        ocean_custer_resource_url = f"{hub.exec.spotinst.URL}/ocean/aws/k8s/cluster/{resource_id}?accountId={ctx.acct.account_id}"
        ret = await hub.exec.request.json.get(
            ctx,
            url=ocean_custer_resource_url,
            success_codes=[200],
            headers={"Authorization": f"Bearer {ctx.acct.token}"},
        )
        if not ret["result"]:
            if ret["status"] == 400:
                result["comment"] = (
                    f"spotinst.ocean.aws.k8s_cluster '{name}'(resource Id: '{resource_id}') not found",
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
        ] = hub.tool.spotinst.ocean.aws.conversion_utils.convert_raw_k8s_cluster_to_present(
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
            old_tags_list=result["old_state"]
            .get("compute")
            .get("launchSpecification")
            .get("tags"),
            new_tags_list=desire_state.get("compute")
            .get("launchSpecification")
            .get("tags"),
        )
        update_required = update_required or is_tags_updated

        if update_required:
            if ctx.get("test", False):
                result["new_state"] = desire_state
                result[
                    "comment"
                ] = hub.tool.spotinst.comment_utils.would_update_comment(
                    resource_type="spotinst.ocean.aws.k8s_cluster", name=resource_id
                )
                if update_policy and update_policy["shouldRoll"]:
                    roll_result = await hub.tool.spotinst.ocean.aws.k8s_cluster_utils.initiate_roll(
                        ctx, update_policy, resource_id
                    )
                    result["comment"] += roll_result["comment"]
                    result["new_state"]["update_policy"] = copy.deepcopy(update_policy)

                return result
            # update in real
            ret = await hub.exec.request.json.put(
                ctx,
                success_codes=[200],
                headers={"Authorization": f"Bearer {ctx.acct.token}"},
                url=ocean_custer_resource_url,
                data=json.dumps(data),
            )
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
            ] = hub.tool.spotinst.ocean.aws.conversion_utils.convert_raw_k8s_cluster_to_present(
                raw_resource=ret["ret"].get("response").get("items")[0],
                idem_resource_name=resource_id,
            )
            result["comment"] = hub.tool.spotinst.comment_utils.update_comment(
                resource_type="spotinst.ocean.aws.k8s_cluster", name=resource_id
            )

            # initiate roll only in real update (when update is successful)
            if update_policy and update_policy["shouldRoll"]:
                roll_result = (
                    await hub.tool.spotinst.ocean.aws.k8s_cluster_utils.initiate_roll(
                        ctx, update_policy, resource_id
                    )
                )

                result["comment"] += roll_result["comment"]
                if not roll_result["result"]:
                    result["result"] = False
                    return result

                result["new_state"]["update_policy"] = copy.deepcopy(update_policy)
        else:
            result["comment"] = hub.tool.spotinst.comment_utils.already_present_comment(
                resource_type="spotinst.ocean.aws.k8s_cluster",
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
                resource_type="spotinst.ocean.aws.k8s_cluster", name=name
            )
            return result
        # create in real
        try:
            data.get("cluster")["region"] = region
            ret = await hub.exec.request.json.post(
                ctx,
                success_codes=[200],
                headers={"Authorization": f"Bearer {ctx.acct.token}"},
                url=f"{hub.exec.spotinst.URL}/ocean/aws/k8s/cluster?accountId={ctx.acct.account_id}",
                data=json.dumps(data),
            )
        except Exception as e:
            hub.log.debug(f"Could not create spotinst.ocean.aws.k8s_cluster {e}")
            result["result"] = False
            result["comment"] = (f"{e.__class__.__name__}: {e}",)
            return result

        if not ret["result"]:
            result["result"] = False
            errors = json.loads(ret["ret"]).get("response").get("errors")
            if errors:
                result["comment"] = (
                    ret["comment"],
                    errors[0].get("message"),
                )
            else:
                result["comment"] = ret["comment"]
            return result

        resource_id = ret["ret"].get("response").get("items")[0].get("id")
        result[
            "new_state"
        ] = hub.tool.spotinst.ocean.aws.conversion_utils.convert_raw_k8s_cluster_to_present(
            raw_resource=ret["ret"].get("response").get("items")[0],
            idem_resource_name=resource_id,
        )
        result["comment"] = hub.tool.spotinst.comment_utils.create_comment(
            resource_type="spotinst.ocean.aws.k8s_cluster", name=name
        )

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes the specified Ocean cluster.

    When this call completes, the cluster is no longer available for use.

    Refer the `Spot Delete Ocean Cluster documentation <https://docs.spot.io/api/#operation/OceanAWSClusterDelete>`_
    to get insight of functionality and input parameters

    Args:
        name(str): An idem name of the ocean cluster.
        resource_id(str, Optional): The ID of the ocean cluster.

    Request Syntax:
        .. code-block:: sls

           [k8s_cluster-resource-id]:
             spotinst.ocean.aws.k8s_cluster.absent:
               - name: 'string'
               - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem-test-k8s_cluster:
              spotinst.ocean.aws.k8s_cluster.absent:
                - name: idem-test-k8s_cluster
                - resource_id:idem-test-k8s_cluster

    """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.spotinst.comment_utils.already_absent_comment(
            resource_type="spotinst.ocean.aws.k8s_cluster", name=name
        )
        return result

    url = f"{hub.exec.spotinst.URL}/ocean/aws/k8s/cluster/{resource_id}?accountId={ctx.acct.account_id}"
    try:
        before = await hub.exec.request.json.get(
            ctx,
            url=url,
            success_codes=[200],
            headers={"Authorization": f"Bearer {ctx.acct.token}"},
        )
    except Exception as e:
        hub.log.debug(f"Could not get K8s Cluster {e}")
        result["result"] = False
        result["comment"] = (f"{e.__class__.__name__}: {e}",)
        return result

    if before["status"] == 400:
        result["comment"] = hub.tool.spotinst.comment_utils.already_absent_comment(
            resource_type="spotinst.ocean.aws.k8s_cluster", name=name
        )
    elif before["result"]:
        result[
            "old_state"
        ] = hub.tool.spotinst.ocean.aws.conversion_utils.convert_raw_k8s_cluster_to_present(
            raw_resource=before["ret"].get("response").get("items")[0],
            idem_resource_name=resource_id,
        )

        if ctx.get("test", False):
            result["comment"] = hub.tool.spotinst.comment_utils.would_delete_comment(
                resource_type="spotinst.ocean.aws.k8s_cluster", name=name
            )
            return result
        try:
            after = await hub.exec.request.json.delete(
                ctx,
                url=url,
                success_codes=[200],
                headers={"Authorization": f"Bearer {ctx.acct.token}"},
            )
        except Exception as e:
            hub.log.debug(f"Could not delete spotinst.ocean.aws.k8s_cluster {e}")
            result["result"] = False
            result["comment"] = (f"{e.__class__.__name__}: {e}",)
            return result
        if not after["result"] or after["status"] == 400:
            hub.log.debug(
                f"Could not delete spotinst.ocean.aws.k8s_cluster {result['comment']} {result['ret']}"
            )
            result["comment"] = after["comment"]
            return result

        result["result"] = after["result"]
        result["comment"] = hub.tool.spotinst.comment_utils.delete_comment(
            resource_type="spotinst.ocean.aws.k8s_cluster", name=name
        )
    else:
        hub.log.debug(f"Could not get k8s Cluster {before['comment']} {before['ret']}")
        result["result"] = False
        result["comment"] = before["comment"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Gets information about the ocean clusters.

    Refer the `Spot Listing Ocean Cluster documentation <https://docs.spot.io/api/#operation/OceanAWSClusterList>`_
    to get insight of functionality and input parameters

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe spotinst.ocean.aws.k8s_cluster

    """
    result = {}
    url = (
        f"{hub.exec.spotinst.URL}/ocean/aws/k8s/cluster?accountId={ctx.acct.account_id}"
    )
    ret = await hub.exec.request.json.get(
        ctx,
        url=url,
        success_codes=[200],
        headers={"Authorization": f"Bearer {ctx.acct.token}"},
    )

    if not ret["result"]:
        raise ValueError(
            f"Error on requesting GET {url} with status code {ret['status']}:"
            f" {ret.get('comment', '')}"
        )
    cluster_list = ret.get("ret").get("response").get("items", None)
    for cluster_item in cluster_list:
        resource_id = cluster_item.get("id")
        translated_resource = hub.tool.spotinst.ocean.aws.conversion_utils.convert_raw_k8s_cluster_to_present(
            raw_resource=cluster_item, idem_resource_name=resource_id
        )

        result[resource_id] = {
            "spotinst.ocean.aws.k8s_cluster.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }
    return result
