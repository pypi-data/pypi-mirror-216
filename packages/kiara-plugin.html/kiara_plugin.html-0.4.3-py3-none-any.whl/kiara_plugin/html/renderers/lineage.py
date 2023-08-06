# -*- coding: utf-8 -*-
import base64
import uuid
from typing import Any, Dict, Iterable, Type, Union

from airium import Airium
from pydantic import Field, root_validator

from kiara.api import Kiara, Value
from kiara.exceptions import KiaraException
from kiara.models.values.lineage import ValueLineage
from kiara.models.values.value import ORPHAN, ValuePedigree
from kiara.renderers import (
    KiaraRenderer,
    KiaraRendererConfig,
    RenderInputsSchema,
    SourceTransformer,
)
from kiara.utils.graphs import create_image


class LineageHtmlInputs(RenderInputsSchema):

    render_style: str = Field(
        description="The style to use for rendering the lineage graph.",
        default="default",
    )
    config: Dict[str, Any] = Field(
        description="Additional, optional configuration for the renderer.",
        default_factory=dict,
    )

    @root_validator(pre=True)
    def validate_linage_inputs(cls, values):

        result = {}
        result["render_style"] = values.pop("render_style", "default")
        config = values.pop("config", {})
        if config:
            result["config"] = config
        else:
            result["config"] = values
        return result


class LineageHtmlRendererConfig(KiaraRendererConfig):
    pass


def fill_html_lineage_tree(
    kiara: Kiara,
    pedigree: ValuePedigree,
    node: Union[Airium, None] = None,
    include_ids: bool = False,
    level: int = 0,
) -> Airium:
    """Recursive helper method to get a tree structure from a root value ppedigree."""

    if node is None:
        node = Airium()

    with node.ul():
        with node.li():
            with node.span(klass="nested"):
                node(pedigree.module_type)
            with node.ul(klass="nested"):
                for input_name in sorted(pedigree.inputs.keys()):

                    child_value_id = pedigree.inputs[input_name]
                    child_value = kiara.data_registry.get_value(child_value_id)

                    value_type = child_value.data_type_name
                    if include_ids:
                        v_id_str = f" = {child_value.value_id}"
                    else:
                        v_id_str = ""

                    with node.li():
                        node(f"input: {input_name} ({value_type}) {v_id_str}")
                        if child_value.pedigree != ORPHAN:
                            fill_html_lineage_tree(
                                kiara=kiara,
                                pedigree=child_value.pedigree,
                                node=node,
                                level=level + 1,
                                include_ids=include_ids,
                            )
    return node


class LineageTransformer(SourceTransformer):
    def __init__(self, kiara: Kiara):

        self._kiara: Kiara = kiara
        super().__init__()

    def retrieve_supported_python_classes(self) -> Iterable[Type]:

        return [Value, ValueLineage, str, uuid.UUID]

    def retrieve_supported_inputs_descs(self) -> Union[str, Iterable[str]]:
        return [
            "a value object",
            "a value alias",
            "a value id",
            "a value lineeage object",
        ]

    def validate_and_transform(self, source: Any) -> Union[ValueLineage, None]:
        if isinstance(source, ValueLineage):
            return source
        value = self._kiara.data_registry.get_value(source)
        return value.lineage


class LineageRendererHtml(
    KiaraRenderer[ValueLineage, LineageHtmlInputs, str, LineageHtmlRendererConfig]
):

    _renderer_name = "lineage_html"
    _renderer_config_cls = LineageHtmlRendererConfig  # type: ignore
    _inputs_schema = LineageHtmlInputs  # type: ignore

    def retrieve_doc(self) -> Union[str, None]:

        return "Render a value lineage as html page."

    def retrieve_source_transformers(self) -> Iterable[SourceTransformer]:
        return [LineageTransformer(kiara=self._kiara)]

    def retrieve_supported_render_sources(self) -> str:
        return "value"

    def retrieve_supported_render_targets(self) -> Union[Iterable[str], str]:
        return "lineage_html"

    def _render(self, instance: ValueLineage, render_config: LineageHtmlInputs) -> str:

        render_style = render_config.render_style
        func_name = f"render__{render_style}"
        if not hasattr(self, func_name):
            details = "Available styles:\n\n"
            for attr in dir(self):
                if attr.startswith("render__"):
                    details += f" - {attr.replace('render__', '')}\n"
            raise KiaraException(
                f"Can't render lineage in requested style '{render_style}': style not available.",
                details=details,
            )

        func = getattr(self, func_name)
        result = func(lineage=instance, **render_config.config)

        airium = Airium()
        airium("<!DOCTYPE html>")
        with airium.html(lang="en"):
            with airium.head():
                airium.meta(charset="utf-8")
                airium.title(_t="Value lineage")

            with airium.body():
                airium(result)

        return str(airium)

    def render__default(self, lineage: ValueLineage, **config) -> str:
        """Renders a html tree view using ul/li elements in a recursive helper function.

        There's a lot more we can do here, like replacing the value ids with aliases (if the values have one), or have a preview of the value whe hovering over it. This is really just the bare minimum.

        """

        include_ids = config.get("include_ids", False)
        result = fill_html_lineage_tree(
            kiara=self._kiara,
            pedigree=lineage.value.pedigree,
            node=None,
            include_ids=include_ids,
        )
        return str(result)

    def render__image(self, lineage: ValueLineage, **config) -> str:
        """Renders the lineage as a graph image.

        I wrote this to show how we can include Javascript in the resulting html page. Being able to include the image bytes directly is also neat I think.
        """

        graph = lineage.full_graph

        img = create_image(graph=graph)
        img_enc = base64.b64encode(img).decode("utf-8")
        img_id = f"lineage_graph_img_{lineage.value.value_id}"

        airium = Airium()

        with airium.div():
            with airium.div():
                airium(f"Value lineage for value '{lineage.value.value_id}'")
            with airium.div():
                airium.img(id=img_id, src="")

        with airium.script():
            airium(
                f'document.getElementById("{img_id}").src = "data:image/png;base64,{img_enc}";'
            )

        return str(airium)

    def render__tree(self, lineage: ValueLineage, **config) -> str:

        template = self._kiara.render_registry.get_template(
            "lineage/lineage.html.j2", template_base="kiara_plugin.html"
        )

        result = template.render(value_lineage=lineage, **config)
        return result
