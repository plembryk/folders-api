from rest_framework.routers import DefaultRouter

from groups.views import FolderViewSet, WordGroupViewSet, WordViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"folders", FolderViewSet, basename="folders")
router.register(r"word-groups", WordGroupViewSet, basename="word-groups")
router.register(r"words", WordViewSet, basename="words")


urlpatterns = router.urls
