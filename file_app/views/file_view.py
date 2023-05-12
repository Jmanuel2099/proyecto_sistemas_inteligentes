import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from file_app.controller.file_controller import FileController


class LoadFileView:

    def __init__(self) -> None:
        self.controller = FileController()

    def _get_request_body(self, request):
        return json.loads(request.body)
    
    # @require_POST
    @csrf_exempt
    def load_file(self, request):
        if request.FILES:
            file = request.FILES['file']
            self.controller.load_file(file)
            return JsonResponse({"mensaje": "Archivo recibido exitosamente"})

    @csrf_exempt
    def describe_file(self, request):
        response = self.controller.describe_file()
        return JsonResponse(response)
    
    @csrf_exempt
    def statistical_analysis(self, request, method_id):
        self.controller.process_missing_data(method_id)
        return JsonResponse({"mensaje": "Metodo aplicado"})