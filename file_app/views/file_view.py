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
        try:
            if not request.FILES:
                return JsonResponse(
                    {
                        'Error': '400 Bad Request', 
                        'Message': 'A file was expected to be received.'
                     })

            file = request.FILES['file']
            if file.name.split('.')[1] != 'xlsx':
                return JsonResponse(
                    {
                        'Error': '400 Bad Request', 
                        'Message': 'An xlsx export file was expected.'
                    })

            self.controller.load_file(file)
            return JsonResponse({"Message": "Success"})

        except Exception as error:
            print(error)
            return JsonResponse({'Error': '500 Internal Server Error'})


    @csrf_exempt
    def describe_file(self, request):
        try:
            response = self.controller.describe_file()
            if response is None:
                return JsonResponse(
                    {
                        'Error': '424 Failed Dependency', 
                        'Message': 'No document has been uploaded yet.'
                    })

            return JsonResponse(response)
        except Exception as error:
            print(error)
            return JsonResponse({'Error': '500 Internal Server Error'})

    @csrf_exempt
    def statistical_analysis(self, request, method_id):
        try:
            if (method_id != self.controller.AVERAGE_IMPUTATION_METHOD 
                or method_id != self.controller.DESCARD_METHOD):
                return JsonResponse(
                    {
                        'Error': '408 Time out',
                        'Message': 'Method_id parameter must be 1 or 2.'
                    })

            self.controller.process_missing_data(method_id)
            return JsonResponse({"Message": "Method applied successfully."})
        except Exception as error:
            print(error)
            return JsonResponse({'Error': '500 Internal Server Error'})
