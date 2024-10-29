from uuid import UUID
from celery import shared_task
from .models import Profile
import cloudinary.uploader


# Shared tasks are not bound to a specific app instance, so they can be used in any app in the project
@shared_task(name="upload_avatar_to_cloudinary")
def upload_avatar_to_cloudinary(profile_id: UUID, image_content: bytes) -> None:
    profile = Profile.objects.get(id=profile_id)
    response = cloudinary.uploader.upload(image_content)
    profile.avatar = response.get("url")
    profile.save()


@shared_task(name="update_all_reputations")
def update_all_reputations() -> None:
    for profile in Profile.objects.all():
        profile.update_reputation()
        profile.save()
