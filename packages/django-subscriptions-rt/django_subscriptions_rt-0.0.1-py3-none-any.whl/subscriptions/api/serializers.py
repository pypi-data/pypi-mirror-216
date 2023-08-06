from decimal import Decimal
from typing import Optional

from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField

from ..fields import relativedelta_to_dict
from ..models import Plan, Subscription


class PlanSerializer(ModelSerializer):
    charge_amount = SerializerMethodField()
    charge_period = SerializerMethodField()
    max_duration = SerializerMethodField()

    class Meta:
        model = Plan
        fields = 'id', 'codename', 'name', 'charge_amount', 'charge_amount_currency', 'charge_period', 'max_duration',

    def get_charge_amount(self, obj) -> Optional[Decimal]:
        return obj.charge_amount and obj.charge_amount.amount

    def get_charge_period(self, obj) -> dict:
        return relativedelta_to_dict(obj.charge_period)

    def get_max_duration(self, obj) -> dict:
        return relativedelta_to_dict(obj.max_duration)


class SubscriptionSerializer(ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = Subscription
        fields = 'id', 'plan', 'start', 'end',


class PaymentSerializer(Serializer):
    pass  # TODO
