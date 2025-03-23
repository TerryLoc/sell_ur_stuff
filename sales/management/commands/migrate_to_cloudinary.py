import os
import requests
from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.files import File
from django.core.files.base import ContentFile
from django.db.models import FileField, ImageField
from django.conf import settings
import cloudinary
import cloudinary.uploader


class Command(BaseCommand):
    help = "Migrate existing media files to Cloudinary"

    def handle(self, *args, **options):
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE["CLOUD_NAME"],
            api_key=settings.CLOUDINARY_STORAGE["API_KEY"],
            api_secret=settings.CLOUDINARY_STORAGE["API_SECRET"],
        )

        # Get all installed apps
        for app_config in apps.get_app_configs():
            self.stdout.write(f"Checking models in {app_config.label}")

            # Get all models in each app
            for model in app_config.get_models():
                self.stdout.write(f"  Checking model {model.__name__}")

                # Find fields that are file or image fields
                file_fields = []
                for field in model._meta.get_fields():
                    if isinstance(field, (FileField, ImageField)):
                        file_fields.append(field.name)

                if not file_fields:
                    continue

                self.stdout.write(f"    Found fields: {', '.join(file_fields)}")

                # Get all instances of this model
                instances = model.objects.all()
                for instance in instances:
                    for field_name in file_fields:
                        field = getattr(instance, field_name)

                        # Skip empty fields
                        if not field:
                            continue

                        # Check if file exists on local filesystem
                        if not hasattr(field, "path") or not os.path.exists(field.path):
                            self.stdout.write(
                                self.style.WARNING(
                                    f"      File not found or already on Cloudinary: {field.name}"
                                )
                            )
                            continue

                        # Upload to Cloudinary
                        try:
                            self.stdout.write(f"      Uploading {field.name}")

                            # Open the file
                            with open(field.path, "rb") as f:
                                # Upload to Cloudinary
                                result = cloudinary.uploader.upload(field.path)

                                # Get the URL from the result
                                cloudinary_url = result["secure_url"]

                                # Get the filename from the original path
                                filename = os.path.basename(field.path)

                                # Download the file from Cloudinary to a ContentFile
                                response = requests.get(cloudinary_url)
                                content_file = ContentFile(response.content)

                                # Update the model's field with the new file
                                field_instance = getattr(instance, field_name)
                                field_instance.save(filename, content_file, save=False)

                                # Save the instance to update the database
                                instance.save()

                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"      Successfully uploaded and updated {field.name} to {cloudinary_url}"
                                )
                            )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(
                                    f"      Error uploading {field.name}: {str(e)}"
                                )
                            )

        self.stdout.write(self.style.SUCCESS("Migration complete!"))
