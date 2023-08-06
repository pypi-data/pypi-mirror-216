# -*- coding: utf-8 -*-

# from kiara.models.render_value import RenderMetadata, RenderValueResult, RenderScene
# from kiara.models.values.value import Value
# from kiara_plugin.tabular.models.table import BaseRenderTableScene, RenderTableScene
#
# """This module contains the metadata (and other) models that are used in the ``kiara_plugin.html`` package.
#
# Those models are convenience wrappers that make it easier for *kiara* to find, create, manage and version metadata -- but also
# other type of models -- that is attached to data, as well as *kiara* modules.
#
# Metadata models must be a sub-class of [kiara.metadata.MetadataModel][kiara.metadata.MetadataModel]. Other models usually
# sub-class a pydantic BaseModel or implement custom base classes.
# """
#
# class RenderHtmlValueScene(RenderScene):
#
#     _kiara_model_id = "instance.render_scene.html_any"
#
#     @classmethod
#     def retrieve_source_type(cls) -> str:
#         return "any"
#
#     def render_as__html(self, value: "Value"):
#         render_config = {
#         "show_pedigree": False,
#         "show_serialized": False,
#         "show_data_preview": False,
#         "show_properties": True,
#         "show_destinies": True,
#         "show_destiny_backlinks": True,
#         "show_lineage": True,
#         "show_environment_hashes": False,
#         "show_environment_data": False,
#         }
#         pretty = value.create_info().create_html(**render_config)
#
#         render_metadata = RenderMetadata(this_scene=self)
#         return RenderValueResult(rendered=pretty, metadata=render_metadata)
#
# class RenderHtmlArrayScene(BaseRenderTableScene):
#
#     _kiara_model_id = "instance.render_scene.html_array"
#
#     @classmethod
#     def retrieve_source_type(cls) -> str:
#         return "array"
#
#     def render_as__html(self, value: Value):
#
#         render_config = {
#         "show_pedigree": False,
#         "show_serialized": False,
#         "show_data_preview": False,
#         "show_properties": True,
#         "show_destinies": True,
#         "show_destiny_backlinks": True,
#         "show_lineage": True,
#         "show_environment_hashes": False,
#         "show_environment_data": False,
#         }
#
#         if self.render_metadata:
#             pretty = value.create_info().create_html(**render_config)
#             related_scenes = {
#                 "data": RenderTableScene()
#             }
#         else:
#             wrap, related_scenes = self.preprocess_table(value=value)
#             related_scenes["metadata"] = RenderTableScene(render_metadata=True)
#             pretty = wrap.as_html(max_row_height=1)
#
#         render_metadata = RenderMetadata(related_scenes=related_scenes, this_scene=self)
#
#         return RenderValueResult(rendered=pretty, metadata=render_metadata)
#
#
# class RenderHtmlTableScene(BaseRenderTableScene):
#
#     _kiara_model_id = "instance.render_scene.html_table"
#
#     def render_as__html(self, value: Value):
#
#         render_config = {
#         "show_pedigree": False,
#         "show_serialized": False,
#         "show_data_preview": False,
#         "show_properties": True,
#         "show_destinies": True,
#         "show_destiny_backlinks": True,
#         "show_lineage": True,
#         "show_environment_hashes": False,
#         "show_environment_data": False,
#         }
#
#         if self.render_metadata:
#             pretty = value.create_info().create_html(**render_config)
#             related_scenes = {
#                 "data": RenderTableScene()
#             }
#         else:
#             wrap, related_scenes = self.preprocess_table(value=value)
#             related_scenes["metadata"] = RenderTableScene(render_metadata=True)
#             pretty = wrap.as_html(max_row_height=1)
#
#         render_metadata = RenderMetadata(related_scenes=related_scenes, this_scene=self)
#
#         return RenderValueResult(rendered=pretty, metadata=render_metadata)
