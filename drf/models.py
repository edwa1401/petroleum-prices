from django.db import models

class Hallo(models.Model):
    name = models.CharField(max_length=1000, blank=False)
    msg = models.TextField(default='hallo')

    def __repr__(self) -> str:
        return f'msg: {self.msg} {self.name}'
