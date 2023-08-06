from typing import Iterable, Tuple
import base64
from fetchfox import rest
from fetchfox.checks import check_str
from fetchfox.constants.cardano import ADA_HANDLE_POLICY_ID

BASE_URL = "https://cardano-mainnet.blockfrost.io/api"


def get(service: str, project_id: str, params: dict = None, version: int = 0) -> Tuple[dict, int]:
    check_str(project_id, "blockfrost.project_id")

    return rest.get(
        url=f"{BASE_URL}/v{version}/{service}",
        params=params or {},
        headers={
            "project_id": project_id,
        },
    )


def get_assets(policy_id: str, project_id: str) -> Iterable[str]:
    check_str(policy_id, "blockfrost.policy_id")
    policy_id = policy_id.strip().lower()

    page = 0

    while True:
        page += 1

        response, status_code = get(
            f"assets/policy/{policy_id}",
            params={
                "page": page,
                "count": 100,
                "order": "desc",
            },
            project_id=project_id,
        )

        if not response:
            break

        for item in response:
            if int(item["quantity"]) == 0:
                continue

            if item["asset"] == policy_id:
                continue

            yield item["asset"]


def get_asset_data(asset_id: str, project_id: str) -> dict:
    check_str(asset_id, "blockfrost.asset_id")

    asset_id = asset_id.strip().lower()

    response, status_code = get(
        f"assets/{asset_id}",
        project_id=project_id,
    )

    return response


def get_stake_address(address: str, project_id: str) -> str:
    check_str(address, "blockfrost.address")

    response, status_code = get(
        f"addresses/{address}",
        project_id=project_id,
    )

    return response.get("stake_address")


def get_holdings(stake_address: str, project_id: str) -> Iterable[dict]:
    check_str(stake_address, "blockfrost.stake_address")

    page = 0

    while True:
        page += 1

        response, status_code = get(
            f"accounts/{stake_address}/addresses/assets",
            params={
                "count": 100,
                "page": page,
            },
            project_id=project_id,
        )

        if not response:
            break

        yield from response


def get_owners(asset_id: str, project_id: str) -> dict:
    check_str(asset_id, "blockfrost.asset_id")

    response, status_code = get(
        f"assets/{asset_id}/addresses",
        project_id=project_id,
    )

    if isinstance(response, dict):
        if response.get("error"):
            return None

    for item in response:
        if item.get("quantity") == "1":
            address = item["address"]
            stake_address = get_stake_address(address, project_id)

            yield {
                "asset_id": asset_id,
                "address": address,
                "stake_address": stake_address,
                "amount": item["quantity"],
            }


def get_handle(stake_address: str, project_id: str) -> str:
    handles = []

    for holding in get_holdings(stake_address, project_id=project_id):
        if holding["quantity"] != "1":
            continue

        asset_id = holding["unit"]

        if not asset_id.startswith(ADA_HANDLE_POLICY_ID):
            continue

        asset_name = bytes.fromhex(asset_id[56:]).decode()
        handles.append(asset_name)

    if not handles:
        return None

    return sorted(handles, key=len)[0]


def resolve_handle(handle: str, project_id: str) -> str:
    check_str(handle, "blockfrost.handle")

    if handle.startswith("$"):
        if handle.startswith("$"):
            handle = handle[1:]

    handle = handle.lower()
    encoded_name = base64.b16encode(handle.encode()).decode("utf-8")

    asset_id = f"{ADA_HANDLE_POLICY_ID}{encoded_name}".lower()
    owners = list(get_owners(asset_id, project_id))

    if not owners:
        return None

    return owners[0]
