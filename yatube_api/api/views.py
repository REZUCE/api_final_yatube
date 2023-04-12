from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins, permissions
from rest_framework.pagination import LimitOffsetPagination
from .permissions import IsOwnerOrReadOnly
from posts.models import Group, Post, Follow
from .serializers import (PostSerializer, GroupSerializer,
                          CommentSerializer, FollowSerializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Отобразить группу (списком).
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Получить подписки (списком).
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username',)

    def get_queryset(self):
        new_queryset = Follow.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """
    Получить все посты (списком).
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly, ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получить комментарии (списком).
    """
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly, ]

    def get_post(self):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return post

    def get_queryset(self):
        new_queryset = self.get_post().comments.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
