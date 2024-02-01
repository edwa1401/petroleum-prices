import datetime
import logging

from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework import generics, permissions, viewsets

from prices_analyzer.models import Depot, Prices, ProductionPlace, UserRouts
from prices_analyzer.serializers import PricesSerializer
from rail_tariff.models import RzdStation
from rest_api.filters import PetroleumsFilter
from rest_api.models import DensityMap, PetroleumMap
from rest_api.serializers import (
    DensityMapSerializer,
    DepotSerializer,
    PetroleumMapSerializer,
    ProductionPlacesSerializer,
    RzdStationSerializer,
    UserRoutsSerializer,
)
from django_filters import rest_framework as filters


logger = logging.getLogger(__name__)

class PetroleumMapList(generics.ListAPIView):
    queryset = PetroleumMap.objects.all()
    serializer_class = PetroleumMapSerializer
    permission_classes = [permissions.IsAuthenticated]


class PetroleumMapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PetroleumMap.objects.all()
    serializer_class = PetroleumMapSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class DensityMapList(generics.ListAPIView):
    queryset = DensityMap.objects.all()
    serializer_class = DensityMapSerializer
    permission_classes = [permissions.IsAuthenticated]


class DensityMapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DensityMap.objects.all()
    serializer_class = DensityMapSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class ProductionPlacesList(generics.ListAPIView):
    queryset = ProductionPlace.objects.all()
    serializer_class = ProductionPlacesSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductionPlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductionPlace.objects.all()
    serializer_class = ProductionPlacesSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class RzdStationListView(generics.ListAPIView):
    queryset = RzdStation.objects.all()
    serializer_class = RzdStationSerializer
    permission_classes = [permissions.IsAuthenticated]


class RzdStationCreateView(generics.ListCreateAPIView):
    queryset = RzdStation.objects.all()
    serializer_class = RzdStationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class RzdStationUpdateView(generics.UpdateAPIView):
    queryset = RzdStation.objects.all()
    lookup_field = 'code'
    serializer_class = RzdStationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class RzdStationViewSet(viewsets.ModelViewSet):
    queryset = RzdStation.objects.all()
    lookup_field = 'code'
    serializer_class = RzdStationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class DepotListView(generics.ListAPIView):
    queryset = Depot.objects.all()
    serializer_class = DepotSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('name',)


class DepotCreateView(generics.ListCreateAPIView):
    queryset = Depot.objects.all()
    serializer_class = DepotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer) -> None: # type: ignore[no-untyped-def]
        logger.debug('user=%s', self.request.user)
        serializer.save(user=self.request.user)
        logger.debug('user=%s', self.request.user)


class PricesUserListView(generics.ListAPIView):

    serializer_class = PricesSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('depot',)

    def get_queryset(self) -> QuerySet[Prices]:
        user = self.request.user
        logger.debug('user=%s', user)

        depots = Depot.objects.filter(user__username=user.username).prefetch_related('user')
        logger.debug('depots=%s', depots)

        end_day = datetime.datetime.now()
        start_day = end_day - datetime.timedelta(days=14)


        prices = Prices.objects.filter(
            Q(petroleum__day__lte=end_day),
            Q(petroleum__day__gte=start_day),
            Q(depot__in=depots)).prefetch_related('depot').prefetch_related(
            'petroleum').prefetch_related('production_place').prefetch_related('rail_tariff')
        
        logger.debug('prices=%s', prices)

        return prices
    

class PricesViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = PricesSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PetroleumsFilter

    def get_queryset(self) -> QuerySet[Prices]:
        user = self.request.user
        logger.debug('user=%s', user)

        depots = Depot.objects.filter(user__username=user.username).prefetch_related('user')
        logger.debug('depots=%s', depots)


        prices = Prices.objects.filter(depot__in=depots).prefetch_related(
            'depot').prefetch_related('petroleum').prefetch_related(
                'production_place').prefetch_related('rail_tariff')
        
        logger.debug('prices=%s', prices)

        return prices
    
    
class UserRoutsCreateView(generics.ListCreateAPIView):
    serializer_class = UserRoutsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[UserRouts]:
        user = self.request.user

        depots = Depot.objects.filter(user__username=user.username).prefetch_related('user')
        logger.debug('depots=%s', depots)

        user_routs = UserRouts.objects.filter(
            depot__in=depots).prefetch_related('depot').prefetch_related('production_place')
        
        logger.debug('user_production_places=%s', user_routs)

        return user_routs


class UserRoutsPricesView(generics.ListAPIView):

    serializer_class = PricesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Prices]:
        user = self.request.user
        logger.debug('user=%s', user)

        depots = Depot.objects.filter(user__username=user.username).prefetch_related('user')
        logger.debug('depots=%s', depots)

        # TODO
        # заменить/удалить Depot и Prod Places в Prices на UserRouts
        # переделать prices_analyzer/services/create_prod_places.py 
        # переделать все въюхи

        custom_routs = UserRouts.objects.filter(
            depot__in=depots).values_list('production_place')

        end_day = datetime.datetime.now()
        start_day = end_day - datetime.timedelta(days=14)


        prices = Prices.objects.filter(
            Q(petroleum__day__lte=end_day),
            Q(petroleum__day__gte=start_day),
            Q(depot__in=depots),
            Q(production_place__in=custom_routs),
            ).prefetch_related('depot').prefetch_related(
            'petroleum').prefetch_related('production_place').prefetch_related('rail_tariff')
        
        logger.debug('prices=%s', prices)

        return prices
