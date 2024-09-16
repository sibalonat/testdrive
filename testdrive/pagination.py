from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 15

class CustomPageNumberPagination(PageNumberPagination):
    page_size = DEFAULT_PAGE
    page_size_query_param = 'page_size'
    max_page_size = DEFAULT_PAGE_SIZE

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'meta': {
                'last_page': self.page.paginator.num_pages,
                'page': int(self.request.query_params.get('page', DEFAULT_PAGE)),
                # 'page_size': int(self.request.GET.get('page_size', self.page_size)),
                
                'page_size': int(self.request.query_params.get('page_size', DEFAULT_PAGE_SIZE)),
            },
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            # 'results': data
        })