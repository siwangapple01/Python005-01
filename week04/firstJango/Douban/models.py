from django.db import models

# Create your models here.


class DoubanComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    n_star = models.IntegerField()
    short = models.CharField(max_length=400)

    class Meta:
        managed = False
        db_table = 'movieratingcomment'
