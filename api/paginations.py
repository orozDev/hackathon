from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'limit'
    page_query_param = 'offset'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'limit'
    page_query_param = 'offset'
    max_page_size = 100
