# from django.http import JsonResponse
# from rest_framework import status


# class CustomPermissionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         if response.status_code == 403 and not request.user.is_authenticated:
#             return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
#         return response
