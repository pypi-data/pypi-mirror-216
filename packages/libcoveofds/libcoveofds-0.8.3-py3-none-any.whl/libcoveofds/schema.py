import json
import os

from libcove2.common import schema_dict_fields_generator

_schema_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


class OFDSSchema:
    """Represents and provides information about the schema."""

    package_schema_url: str = os.path.join(_schema_folder, "schema-0-3-0.json")
    network_schema_url: str = os.path.join(
        _schema_folder, "schema-0-3-0-network-only.json"
    )

    def get_package_schema(self):
        with open(self.package_schema_url) as fp:
            return json.load(fp)

    def get_link_rels_for_external_nodes(self) -> list:
        return [
            "tag:opentelecomdata.net,2022:nodesAPI",
            "tag:opentelecomdata.net,2022:nodesFile",
        ]

    def get_link_rels_for_external_spans(self) -> list:
        return [
            "tag:opentelecomdata.net,2022:spansAPI",
            "tag:opentelecomdata.net,2022:spansFile",
        ]

    def get_package_schema_fields(self) -> set:
        return set(schema_dict_fields_generator(self.get_package_schema()))

    def extract_data_ids_from_data_and_path(self, data: dict, path: list) -> dict:
        out: dict = {}
        # network_id
        if len(path) >= 2 and path[0] == "networks":
            network_id = data["networks"][path[1]].get("id")
            if network_id:
                out["network_id"] = network_id
        # other ids
        for field in ["node", "span"]:
            if len(path) >= 4 and path[0] == "networks" and path[2] == field + "s":
                id = data["networks"][path[1]][field + "s"][path[3]].get("id")
                if id:
                    out[field + "_id"] = id
        # return
        return out
