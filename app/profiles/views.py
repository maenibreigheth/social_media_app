from rest_framework import viewsets, mixins, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import Profile
from profiles.serializers import ProfileSerializer, SearchProfileSerializer


class ProfileViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get', 'put', 'patch', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):

        profile = Profile.objects.get(user=request.user)

        if request.method == 'GET':
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PUT':
            serializer = ProfileSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=profile, validated_data=serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = ProfileSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=profile, validated_data=serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


class SearchForProfiles(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def paginate_qs(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SearchProfileSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SearchProfileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        first_name = request.query_params.get('first_name', None)
        last_name = request.query_params.get('last_name', None)

        s1_profiles = Profile.objects.filter(first_name=first_name).order_by('-id')
        if last_name:
            s2_profiles = s1_profiles.filter(last_name=last_name)
            self.paginate_qs(s2_profiles)
        self.paginate_qs(s1_profiles)
