# -*- coding: utf-8 -*-
from typing import Any, Dict, Union

from kiara.api import KiaraModule, Value, ValueMap, ValueMapSchema
from kiara.defaults import DEFAULT_PRETTY_PRINT_CONFIG
from kiara.modules.included_core_modules.pretty_print import PrettyPrintModule
from kiara.utils.output import ArrowTabularWrap


class RenderMarkdown(KiaraModule):

    _module_type_name = "render.markdown.to.html"

    def create_inputs_schema(
        self,
    ) -> ValueMapSchema:

        return {"markdown": {"type": "string", "doc": "The markdown string"}}

    def create_outputs_schema(
        self,
    ) -> ValueMapSchema:

        return {"html": {"type": "html", "doc": "The rendered html"}}

    def process(self, inputs: ValueMap, outputs: ValueMap):

        import markdown

        markdown_string = inputs.get_value_data("markdown")
        html = markdown.markdown(markdown_string)

        outputs.set_value("html", html)


class PrettyPrintWebModule(PrettyPrintModule):

    _module_type_name = "pretty_print.html"

    def pretty_print__table__as__html(
        self, value: Value, render_config: Dict[str, Any]
    ):

        max_rows = render_config.get(
            "max_no_rows", DEFAULT_PRETTY_PRINT_CONFIG["max_no_rows"]
        )
        max_row_height = render_config.get(
            "max_row_height", DEFAULT_PRETTY_PRINT_CONFIG["max_row_height"]
        )
        max_cell_length = render_config.get(
            "max_cell_length", DEFAULT_PRETTY_PRINT_CONFIG["max_cell_length"]
        )

        half_lines: Union[None, int] = None
        if max_rows:
            half_lines = int(max_rows / 2)

        atw = ArrowTabularWrap(value.data.arrow_table)
        result = atw.as_html(
            rows_head=half_lines,
            rows_tail=half_lines,
            max_row_height=max_row_height,
            max_cell_length=max_cell_length,
        )
        return result
