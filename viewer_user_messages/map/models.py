from django.db import models


class PointOnTheMap(models.Model):
    message_id = models.AutoField(primary_key=True)
    photo_path = models.CharField(blank=True, null=True)
    latitude = models.FloatField()
    message = models.CharField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    longitude = models.FloatField()

    def __str__(self):
        return f"message_id = {self.message_id}, '{self.message}'"

    class Meta:
        managed = False
        db_table = 'point_on_the_map'


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=100)
    user_photo_path = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"user_id = {self.user_id} '{self.name}'"

    class Meta:
        managed = False
        db_table = 'user'

