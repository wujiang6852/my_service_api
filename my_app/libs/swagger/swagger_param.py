
import coreapi


def swagger_doc(name="default", description=None, location="query", required=True, _type="string", *args, **kwargs):
    return coreapi.Field(name=name, location=location, required=required, description=description, type=_type,
                         *args, **kwargs)
