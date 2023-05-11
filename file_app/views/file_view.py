import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from file_app.services.handling_file.file import File


class LoadFileView:

    def __init__(self) -> None:
        self.load_file_service = File()

    def _get_request_body(self, request):
        return json.loads(request.body)
    
    # @require_POST
    @csrf_exempt
    def load_file(self, request):
        if request.FILES:
            file = request.FILES['file']
            self.load_file_service.load_file(file)
            
            return JsonResponse({"mensaje": "Archivo recibido exitosamente"})

    @csrf_exempt
    def describe_file(self, request):
        response = self.load_file_service.describe_data()
        return JsonResponse(response)