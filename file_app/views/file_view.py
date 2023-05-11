import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from file_app.services.handling_file.file import File


class LoadFileView:

    def __init__(self) -> None:
        pass

    def _get_request_body(self, request):
        return json.loads(request.body)
    
    @csrf_exempt
    def load_file(self, request):
        # try:
        if request.FILES:
            file = request.FILES['file']
            
            load_file_service = File()
            load_file_service.load_file(file)
            
            return JsonResponse({"mensaje": "Archivo recibido exitosamente"})
        # except:
        #     return JsonResponse({"mensaje": "No se recibió ningún archivo"})