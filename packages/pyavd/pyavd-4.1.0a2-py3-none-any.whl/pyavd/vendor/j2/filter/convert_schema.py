from __future__ import annotations


from pyavd.vendor.errors import AristaAvdError
from pyavd.vendor.utils.display import Display

from pyavd.vendor.errors import AristaAvdError
from pyavd.vendor.schema.avdschema import AvdSchema
from pyavd.avd_schema_tools import AvdSchemaTools
from pyavd.vendor.schema.avdtodocumentationschemaconverter import AvdToDocumentationSchemaConverter
from pyavd.vendor.schema.avdtojsonschemaconverter import AvdToJsonSchemaConverter


def convert_schema(schema_id: str, type: str):
    """
    The `arista.avd.convert_schema` filter will convert AVD Schema to a chosen output format.

    TODO: Split into separate filters or lookups for each type.

    Parameters
    ----------
    schema_id : str, ["eos_cli_config_gen" , "eos_designs"]
        ID of AVD Schema
    type : str, ["documentation_tables", "jsonschema"]
        Type of schema to convert to

    Returns
    -------
    dict | list
        Schema of the requested type

    Raises
    ------
    AvdSchemaError, AvdValidationError
        If the input schema is not valid, exceptions will be raised accordingly.
    """
    avdschema = AvdSchema(schema_id=schema_id)

    # Validate that the loaded schema follows the meta schema
    avdschematools = AvdSchemaTools(
        hostname="schema converter", ansible_display=Display(), schema_id=schema_id, conversion_mode="disabled", validation_mode="error"
    )
    validation_results = avdschematools.validate_schema()
    if validation_results:
        raise AristaAvdError("Invalid schema!")

    if type == "documentation_tables":
        return AvdToDocumentationSchemaConverter(avdschema).convert_schema_to_tables()

    elif type == "jsonschema":
        return AvdToJsonSchemaConverter(avdschema).convert_schema()

    else:
        raise AristaAvdError(f"Filter arista.avd.convert_schema requires type 'documentation_tables' or 'jsonschema'. Got {type}")


class FilterModule(object):
    def filters(self):
        return {
            "convert_schema": convert_schema,
        }
