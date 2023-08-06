# -*- coding: utf-8 -*-
from typing import Any, Mapping

import orjson
from pygments import highlight
from pygments.lexers.data import JsonLexer
from pymdownx.highlight import HtmlFormatter

from kiara.api import Value
from kiara.exceptions import KiaraProcessingException
from kiara.models.data_types import KiaraDict
from kiara.models.rendering import RenderScene, RenderValueResult
from kiara.modules.included_core_modules.render_value import RenderValueModule
from kiara.utils.json import orjson_dumps


class RenderCoreTypeModuleWeb(RenderValueModule):
    _module_type_name = "render.core_types.for.web"

    def render__dict__as__html(self, value: Value, render_config: Mapping[str, Any]):

        render_scene = render_config.get("scene_name", "data")
        # input_number_of_rows = render_config.get("number_of_rows", 20)
        # input_row_offset = render_config.get("row_offset", 0)
        as_table = render_config.get("as_table", True)

        dict_model: KiaraDict = value.data

        if render_scene == "data":
            to_render = dict_model.dict_data
        elif render_scene == "schema":
            to_render = dict_model.data_schema
        else:
            raise KiaraProcessingException(
                f"Invalid value '{render_scene}' argument 'scene_name': only 'data' and 'schema' are allowed"
            )

        from json2html import json2html

        if as_table:
            if not to_render:
                pretty = "-- empty dict --"
            else:
                pretty = json2html.convert(
                    json=to_render,
                    table_attributes=f'id="dict-preview-{ value.value_id }" class=""',
                )
        else:
            json_string = orjson_dumps(
                dict_model.dict_data,
                option=orjson.OPT_NON_STR_KEYS | orjson.OPT_INDENT_2,
            )
            pretty = highlight(json_string, JsonLexer(), HtmlFormatter())

        related_scenes = {
            "data": RenderScene.construct(
                title="data",
                disabled=render_scene == "data",
                description="Render the data of the dict.",
                manifest_hash=self.manifest.manifest_hash,
                render_config={"scene_name": "data"},
            ),
            "schema": RenderScene.construct(
                title="schema",
                disabled=render_scene == "schema",
                description="Show the (json) schema of the dict value.",
                manifest_hash=self.manifest.manifest_hash,
                render_config={"scene_name": "schema"},
            ),
        }

        return RenderValueResult(
            value_id=value.value_id,
            render_config=render_config,
            render_manifest=self.manifest.manifest_hash,
            rendered=pretty,
            related_scenes=related_scenes,
        )
