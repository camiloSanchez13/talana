from rest_framework.pagination import  PageNumberPagination

class TwentyResultsPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20