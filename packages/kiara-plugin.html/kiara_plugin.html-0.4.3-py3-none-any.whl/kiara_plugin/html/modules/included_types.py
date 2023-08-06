# -*- coding: utf-8 -*-
from typing import Any, Mapping

from airium import Airium

from kiara.api import Value
from kiara.models.filesystem import KiaraFileBundle
from kiara.models.rendering import RenderValueResult
from kiara.modules.included_core_modules.render_value import RenderValueModule


class RenderCoreTypeModuleWeb(RenderValueModule):
    _module_type_name = "render.included_types.for.web"

    def render__none__as__html(self, value: Value, render_config: Mapping[str, Any]):

        return RenderValueResult(
            value_id=value.value_id,
            render_config=render_config,
            render_manifest=self.manifest.manifest_hash,
            rendered="<div>-- value empty --</div>",
            related_scenes={},
        )

    def render__file_bundle__as__html(
        self, value: Value, render_config: Mapping[str, Any]
    ):

        import humanfriendly

        # render_scene = render_config.get("scene_name", "data")
        file_bundle: KiaraFileBundle = value.data

        # to_render = file_bundle.dict()

        doc = Airium()
        with doc.table():
            with doc.tr():
                with doc.th():
                    doc("included_files")
                with doc.th():
                    doc("metadata")
            with doc.tr():
                with doc.td():
                    with doc.table():
                        for file_name, incl_file in file_bundle.included_files.items():
                            with doc.tr():
                                with doc.td():
                                    doc(file_name)
                                with doc.td():
                                    file_size = humanfriendly.format_size(
                                        incl_file.size
                                    )
                                    doc(file_size)
                with doc.td():
                    with doc.table():
                        with doc.tr():
                            with doc.td():
                                doc("bundle name")
                            with doc.td():
                                doc(file_bundle.bundle_name)
                        with doc.tr():
                            with doc.td():
                                doc("bundle size")
                            with doc.td():
                                bundle_size = humanfriendly.format_size(
                                    file_bundle.size
                                )
                                doc(bundle_size)

        pretty = str(doc)

        return RenderValueResult(
            value_id=value.value_id,
            render_config=render_config,
            render_manifest=self.manifest.manifest_hash,
            rendered=pretty,
            related_scenes={},
        )
