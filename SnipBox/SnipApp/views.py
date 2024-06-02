from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Snippet, Tag
from .serializers import SnippetSerializer, TagSerializer


# Create your views here.

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Snippet.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        return Response({
            'message': 'Snippet created successfully.',
            'snippet': serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def overview(self, request):
        snippets = self.get_queryset()
        count = snippets.count()
        if count > 0:
            serializer = self.get_serializer(snippets, many=True)
            return Response({
                'message': f'Total {count} snippets found.',
                'total_count': count,
                'snippets': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'No snippets found.',
                'total_count': 0,
                'snippets': []
            }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            snippets = self.get_queryset()
            serializer = self.get_serializer(snippets, many=True)
            return Response({
                'message': 'Snippet deleted successfully.',
                'snippets': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        snippets = self.get_queryset()
        serializer = self.get_serializer(snippets, many=True)
        if snippets.exists():
            return Response({
                'message': 'Snippets retrieved successfully.',
                'snippets': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'No snippets found.',
                'snippets': []
            }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'message': 'Snippet retrieved successfully.',
                'snippet': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                'message': 'Snippet updated successfully.',
                'snippet': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def snippets(self, request, pk=None):
        try:
            tag = self.get_object()
            snippets = Snippet.objects.filter(tags=tag, created_by=request.user)
            if snippets.exists():
                serializer = SnippetSerializer(snippets, many=True)
                return Response({
                    'message': f'Snippets found for tag "{tag.tag_title}".',
                    'snippets': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': f'No snippets found for tag "{tag.tag_title}".',
                    'snippets': []
                }, status=status.HTTP_200_OK)
        except Tag.DoesNotExist:
            return Response({
                'message': 'Tag not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
