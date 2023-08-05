import json
from typing import Any
from typing import Dict


async def get_active_roll(hub, ctx, ocean_cluster_id) -> Dict[str, Any]:
    result = {}
    url = f"{hub.exec.spotinst.URL}/ocean/aws/k8s/cluster/{ocean_cluster_id}/roll?accountId={ctx.acct.account_id}"
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

    cluster_roll_list = ret.get("ret").get("response").get("items", {})
    for cluster_roll_item in cluster_roll_list:
        if (
            cluster_roll_item.get("scope") == "Cluster"
            and cluster_roll_item.get("status") == "IN_PROGRESS"
        ):
            result = cluster_roll_item

    return result


async def initiate_roll(hub, ctx, update_policy, ocean_cluster_id):
    roll_result = dict(comment=(), result=True, ret=None)
    if update_policy and update_policy["shouldRoll"]:
        active_roll = (
            await hub.tool.spotinst.ocean.aws.k8s_cluster_utils.get_active_roll(
                ctx, ocean_cluster_id
            )
        )

        if not active_roll:
            if ctx.get("test", False):
                roll_result["comment"] = (
                    f"Would initiate roll for ocean cluster {ocean_cluster_id}",
                )
                return roll_result

            roll_cofig = update_policy["roll"]
            ocean_custer_initial_roll_url = f"{hub.exec.spotinst.URL}/ocean/aws/k8s/cluster/{ocean_cluster_id}/roll?accountId={ctx.acct.account_id}"
            roll_data = {"roll": roll_cofig}

            ret = await hub.exec.request.json.post(
                ctx,
                success_codes=[200],
                headers={"Authorization": f"Bearer {ctx.acct.token}"},
                url=ocean_custer_initial_roll_url,
                data=json.dumps(roll_data),
            )
            if not ret["result"]:
                errors = json.loads(ret["ret"]).get("response").get("errors")
                if errors:
                    roll_result["comment"] = (
                        ret["comment"],
                        errors[0].get("message"),
                    )
                else:
                    roll_result["comment"] = (ret["comment"],)
                roll_result["result"] = False
                return roll_result

            roll_result["comment"] = (
                f"Initiated roll for ocean cluster {ocean_cluster_id}",
            )
        else:
            roll_result["comment"] = (
                f"Active roll exist for ocean cluster {ocean_cluster_id}",
            )

        return roll_result
