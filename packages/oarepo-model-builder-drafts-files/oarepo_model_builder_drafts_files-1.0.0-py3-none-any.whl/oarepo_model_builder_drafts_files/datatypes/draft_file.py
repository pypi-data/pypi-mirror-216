import marshmallow as ma
from oarepo_model_builder.datatypes import ModelDataType


class DraftFileDataType(ModelDataType):
    model_type = "draft_file"

    class ModelSchema(ModelDataType.ModelSchema):
        type = ma.fields.Str(
            load_default="draft_file",
            required=False,
            validate=ma.validate.Equal("draft_file"),
        )

    def prepare(self, context):
        self.parent_record = context["parent_record"]
        self.file_record = context["file_record"]
        super().prepare(context)
