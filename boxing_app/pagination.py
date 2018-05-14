from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class BoxingPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'page': self.request.query_params.get(self.page_query_param, 1),
            'next': bool(self.get_next_link()),
            'results': data
        })
