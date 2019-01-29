

from rest_framework.permissions import AllowAny
from rest_framework.renderers import *
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.schemas.generators import LinkNode, insert_into
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class MySchemaGenerator(SchemaGenerator):

    def get_links(self, request=None):
        links = LinkNode()

        paths = []
        view_endpoints = []
        for path, method, callback in self.endpoints:
            view = self.create_view(callback, method, request)
            path = self.coerce_path(path, method, view)
            paths.append(path)
            view_endpoints.append((path, method, view))

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
                continue
            link = view.schema.get_link(path, method, base_url=self.url)
            # 将自定义的参数加入到 fields 中
            # 通用 fields
            link._fields += getattr(view, 'fields', ())
            # method fields
            link._fields += self.get_core_fields(view, method)

            subpath = path[len(prefix):]
            keys = self.get_keys(subpath, method, view)

            # from rest_framework.schemas.generators import LinkNode, insert_into
            insert_into(links, keys, link)

        return links

    @staticmethod
    # 从类中取出我们自定义的参数, 交给 swagger 以生成接口文档.
    def get_core_fields(view, method):
        handler = getattr(view, f'{method.lower()}_fields', ())
        return handler


class SwaggerSchemaView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    # 不做认证
    # authentication_classes = [SwaggerAuthentication, ]
    permission_classes = [AllowAny]
    # 设置渲染器
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer,
    ]

    @classmethod
    def get(cls, request):
        generator = MySchemaGenerator(title='yimart_service_api')

        schema = generator.get_schema(request=request)
        return Response(schema)
