from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from drainpipe.service import drainpipe_service
from constants.seoul_district_code_map import DRAINPIPE_DATA_DISTRICT_CODES


def _validate_disctrict_code(district_code: str):
    return district_code in DRAINPIPE_DATA_DISTRICT_CODES.keys()


@method_decorator(csrf_exempt)
@parser_classes([JSONParser])
@api_view(["GET"])
def find_drainpipe_data_with_limit(request, district_code: str):
    if _validate_disctrict_code(district_code):
        return JsonResponse(
            drainpipe_service.find_realtime_drainpipe_data_with_limit(district_code),
            status=status.HTTP_200_OK,
        )
    else:
        return JsonResponse(
            {"msg": "Invalid district code"},
            status=status.HTTP_400_BAD_REQUEST,
        )
