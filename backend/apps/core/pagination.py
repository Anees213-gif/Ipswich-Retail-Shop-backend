"""
Custom pagination classes for API responses
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination that maintains DRF compatibility while providing
    frontend-friendly response format
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            # Frontend-friendly format
            'meta': {
                'page': self.page.number,
                'pageSize': self.page.paginator.per_page,
                'totalItems': self.page.paginator.count,
                'totalPages': self.page.paginator.num_pages,
                'hasNext': self.page.has_next(),
                'hasPrevious': self.page.has_previous(),
            }
        })


class FrontendCompatiblePagination(PageNumberPagination):
    """
    Pagination that returns frontend-expected format
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'products': data,  # Frontend expects 'products' key
            'meta': {
                'page': self.page.number,
                'pageSize': self.page.paginator.per_page,
                'totalItems': self.page.paginator.count,
                'totalPages': self.page.paginator.num_pages,
                'hasNext': self.page.has_next(),
                'hasPrevious': self.page.has_previous(),
            },
            'filters': {
                'categories': [],  # Will be populated by view
                'priceRange': {'min': 0, 'max': 1000},  # Will be calculated
            }
        })
