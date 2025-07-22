from rest_framework import pagination
from rest_framework.response import Response

class SchoolCursorpagination(pagination.PageNumberPagination):
  page_size = 20

  def get_paginated_response(self, data):
    return Response({
      'count': self.page.paginator.count,
      'page': self.page.number,
      'has_next': self.page.has_next(),
      'has_previous': self.page.has_previous(),
      'total_pages': self.page.paginator.num_pages,
      'per_page': self.page_size,
      'results': data
    })