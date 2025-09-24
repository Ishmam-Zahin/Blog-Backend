from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
import requests

class UploadImage(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response(data={'detail': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        apikey = '17986a50063ae01bd9933a71234eee07'
        url = f'https://api.imgbb.com/1/upload?key={apikey}'
        files = {'image': image}
        response = requests.post(url=url, files=files)
        if response.status_code != 200:
            return Response(data={'detail': 'Imgbb upload failed'}, status=status.HTTP_400_BAD_REQUEST)
        data = response.json()
        return Response(data={'url': data['data']['url']}, status=status.HTTP_200_OK)