from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorizeRequestSerializer, CategorizeResponseSerializer
from .services import process_transaction

class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok"})

class CategorizeView(APIView):
    def post(self, request):
        serializer = CategorizeRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "invalid_request", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        data = serializer.validated_data
        
        try:
            result = process_transaction(data['transaction'], data['company_context'])
        except ValueError as e:
            if str(e) == "llm_unavailable":
                return Response(
                    {"error": "llm_unavailable"},
                    status=status.HTTP_502_BAD_GATEWAY
                )
            return Response(
                {"error": "internal_error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        response_serializer = CategorizeResponseSerializer(data=result)
        if not response_serializer.is_valid():
            return Response(
                {"error": "llm_bad_response", "details": response_serializer.errors},
                status=status.HTTP_502_BAD_GATEWAY
            )
            
        return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
