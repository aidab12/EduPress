import os
from django.db import models

from edu.models import UUIDBaseModel
from django.core.files.uploadedfile import SimpleUploadedFile

class CreatedImageModelTest(UUIDBaseModel):
    @classmethod
    def upload_to(cls, instance, filename):
        model_name = cls.__name__.lower()
        filename = os.path.basename(filename)
        return f"thumbnails/{model_name}/{filename}"

    url = models.ImageField(upload_to=upload_to)



# создаём фейковый файл (в памяти)
fake_image = SimpleUploadedFile("avatar.png", b"file_content", content_type="image/png")

# создаём инстанс модели
obj = CreatedImageModelTest(url=fake_image)

# пока не сохраняем, просто проверим путь
print(obj.url.field.upload_to(CreatedImageModelTest, "avatar.png"))
