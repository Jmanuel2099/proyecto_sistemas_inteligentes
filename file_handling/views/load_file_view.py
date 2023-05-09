import json
import sys
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from proyecto_sistemas_inteligentes.mongodb import db


class LoadFileView:

    def __init__(self) -> None:
        pass

    def _get_request_body(self, request):
        return json.loads(request.body)
    
    @csrf_exempt
    def load_file(self, request):
        request_body = self._get_request_body(request)
        #obtener la coleccion
        db_collection = db.file

        result = db_collection.insert_one({"Saludo": "Hola desde django"})

        return JsonResponse({"new_id": str(result.inserted_id)})

    