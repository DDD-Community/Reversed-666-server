from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response: Response = renderer_context['response']

        """
        response, data 의 정보를 활용하여 커스텀한 응답 형태를 만들 수 있습니다.  
        """
        formed_data = {
            'meta': {},
            'data': {},
        }

        renderer_context['response'].data = formed_data
        return super().render(formed_data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)