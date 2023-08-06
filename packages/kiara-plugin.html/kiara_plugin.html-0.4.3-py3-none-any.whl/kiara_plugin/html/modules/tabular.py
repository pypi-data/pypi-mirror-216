# -*- coding: utf-8 -*-
from typing import Any, Mapping

from kiara.api import Value
from kiara.models.rendering import RenderValueResult
from kiara_plugin.tabular.modules.db import RenderDatabaseModuleBase
from kiara_plugin.tabular.modules.table import RenderTableModuleBase


class RenderTableModuleWeb(RenderTableModuleBase):
    _module_type_name = "render.table.for.web"

    def render__table__as__html(self, value: Value, render_config: Mapping[str, Any]):

        input_number_of_rows = render_config.get("number_of_rows", 20)
        input_row_offset = render_config.get("row_offset", 0)

        wrap, data_related_scenes = self.preprocess_table(
            value=value,
            input_number_of_rows=input_number_of_rows,
            input_row_offset=input_row_offset,
        )
        pretty = wrap.as_html(max_row_height=1)

        return RenderValueResult(
            value_id=value.value_id,
            render_config=render_config,
            render_manifest=self.manifest.manifest_hash,
            rendered=pretty,
            related_scenes=data_related_scenes,
        )

    def render__array__as__html(self, value: Value, render_config: Mapping[str, Any]):

        return self.render__table__as__html(value=value, render_config=render_config)


class RenderDatabaseModule(RenderDatabaseModuleBase):
    _module_type_name = "render.database.for.web"

    def render__database__as__html(
        self, value: Value, render_config: Mapping[str, Any]
    ):

        input_number_of_rows = render_config.get("number_of_rows", 20)
        input_row_offset = render_config.get("row_offset", 0)

        table_name = render_config.get("table_name", None)

        wrap, data_related_scenes = self.preprocess_database(
            value=value,
            table_name=table_name,
            input_number_of_rows=input_number_of_rows,
            input_row_offset=input_row_offset,
        )
        pretty = wrap.as_html(max_row_height=1)

        result = RenderValueResult(
            value_id=value.value_id,
            render_config=render_config,
            render_manifest=self.manifest.manifest_hash,
            rendered=pretty,
            related_scenes=data_related_scenes,
        )
        return result
