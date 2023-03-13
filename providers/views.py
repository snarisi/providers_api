import json

from rest_framework import generics
from rest_framework.response import Response

from .models import Providers
from .serializers import ProviderSerializer


class ProvidersView(generics.ListAPIView):
    queryset = Providers.objects.all()
    serializer_class = ProviderSerializer

    def list(self, request):

        # Filter on whether they are active or not
        providers = self._filter_by_active(request, self.queryset)

        # Filter through providers on any combination of user traits
        providers = self._filter_user_traits(request, providers)

        # Sort by rating, descending
        providers = self._sort_by_rating(providers)

        # Sort by the number of times a provider has appeared in a search, ascending
        providers = self._sort_by_search_appearances(providers)

        serializer = ProviderSerializer(providers, many=True)

        return Response(serializer.data)

    def _filter_by_active(self, request, providers):
        # TODO: make these actually booleans maybe
        if request.GET.get('active', '').lower() == 'true':
            return providers.filter(active=True)
        elif request.GET.get('active', '').lower() == 'false':
            return providers.filter(active=False)
        else:
            return providers

    def _get_request_data(self, request, data):
        return request.GET.get(data)

    def _filter_user_traits(self, request, providers):
        if self._get_request_data(request, 'first_name'):
            providers = providers.filter(
                first_name__contains=self._get_request_data(request, 'first_name')
            )
        if self._get_request_data(request, 'last_name'):
            providers = providers.filter(
                last_name__contains=self._get_request_data(request, 'last_name')
            )
        if self._get_request_data(request, 'sex'):
            providers = providers.filter(
                sex__contains=self._get_request_data(request, 'sex')
            )
        if self._get_request_data(request, 'birth_date'):
            providers = providers.filter(
                birth_date__contains=self._get_request_data(request, 'birth_date')
            )
        if self._get_request_data(request, 'rating'):
            providers = providers.filter(
                rating__gte=self._get_request_data(request, 'rating')
            )
        if self._get_request_data(request, 'company'):
            providers = providers.filter(
                company__contains=self._get_request_data(request, 'company')
            )
        if self._get_request_data(request, 'country'):
            providers = providers.filter(
                country__contains=self._get_request_data(request, 'country')
            )
        if self._get_request_data(request, 'language'):
            providers = providers.filter(
                language__contains=self._get_request_data(request, 'language')
            )
        if self._get_request_data(request, 'primary_skills'):
            primary_skills = request.GET.get('primary_skills')
            if primary_skills.startswith('[') and primary_skills.endswith(']'):
                primary_skills = json.loads(primary_skills)
            else:
                primary_skills = [primary_skills,]

            for primary_skill in primary_skills:
                providers = providers.filter(primary_skills__icontains=primary_skill)
        if self._get_request_data(request, 'secondary_skills'):
            secondary_skills = request.GET.get('secondary_skills')
            if secondary_skills.startswith('[') and secondary_skills.endswith(']'):
                secondary_skills = json.loads(secondary_skills)
            else:
                secondary_skills = [secondary_skills,]

            for secondary_skill in secondary_skills:
                providers = providers.filter(secondary_skills__icontains=secondary_skill)

        return providers

    def _sort_by_search_appearances(self, providers):
        for provider in providers:
            provider.search_returns += 1
            provider.save()
        return sorted(providers, key=lambda k: k.search_returns, reverse=False)

    def _sort_by_rating(self, providers):
        return providers.order_by('-rating')
