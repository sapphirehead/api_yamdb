from django.shortcuts import get_object_or_404
from .models import Comments, Review, Titles
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsUserOrAdminOrModerOrReadOnly
from api.serializers import (CommentSerializer, ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsUserOrAdminOrModerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Titles, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Titles, id=review_id)
        serializer.save(reviews=review, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsUserOrAdminOrModerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        comment = get_object_or_404(Comments, id=self.kwargs.get('comment_id'))
        return comment.all()

    def perform_create(self, serializer):
        comment_id = self.kwargs.get("comment_id")
        comment = get_object_or_404(Comments, id=comment_id)
        serializer.save(comments=comment, author=self.request.user)
