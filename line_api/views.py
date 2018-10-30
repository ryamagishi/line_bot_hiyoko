from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def main(request):
    return Response({'data': 'ok'}, status=status.HTTP_201_CREATED)
