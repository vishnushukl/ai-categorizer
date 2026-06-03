from rest_framework import serializers

class TransactionSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    payee = serializers.CharField(required=False, allow_null=True, allow_blank=True)

class HistoricalTransactionSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    category = serializers.CharField(required=True)
    payee = serializers.CharField(required=False, allow_null=True, allow_blank=True)

class CompanyContextSerializer(serializers.Serializer):
    company_id = serializers.CharField(required=True)
    industry = serializers.CharField(required=True)
    chart_of_accounts = serializers.ListField(
        child=serializers.CharField(), required=True, min_length=1
    )
    historical_transactions = HistoricalTransactionSerializer(
        many=True, required=False, default=list
    )

class CategorizeRequestSerializer(serializers.Serializer):
    transaction = TransactionSerializer(required=True)
    company_context = CompanyContextSerializer(required=True)

class CategorizeResponseSerializer(serializers.Serializer):
    category = serializers.CharField()
    confidence = serializers.FloatField()
    reasoning = serializers.CharField()
    is_valid_category = serializers.BooleanField()
    suggested_category_raw = serializers.CharField(allow_null=True, required=False)
    model = serializers.CharField()
