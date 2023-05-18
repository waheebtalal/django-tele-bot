from django.db import models


class TgUser(models.Model):
    # Fields
    id = models.TextField(primary_key=True, max_length=30)
    name = models.TextField(max_length=30)
    username = models.TextField(max_length=30,blank=True)
    phone = models.TextField(max_length=30,blank=True)
    admin = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    long_lim = models.IntegerField(default=7200)
    size_lim = models.IntegerField(default=512)
    spf_msg = models.BooleanField(default=False)
    message = models.TextField(max_length=30,blank=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.id.__str__() + " - " + self.name.__str__() + " - " + self.username.__str__())


class TgMessageStore(models.Model):
    # Relationships
    message_user_constraint = models.ForeignKey("TgUser.TgUser", on_delete=models.CASCADE)

    # Fields
    message_text = models.TextField(max_length=30)
    message_blob = models.BinaryField()

    class Meta:
        pass

    def __str__(self):
        return str(self.message_user_constraint)


class TgProcess(models.Model):
    # Relationships
    process_user_constraint = models.ForeignKey("TgUser.TgUser", on_delete=models.CASCADE)

    # Fields
    process_id = models.TextField(max_length=30)
    start_time = models.TextField(max_length=30)
    messege_id = models.TextField(max_length=30)
    end_time = models.TextField(max_length=30)
    is_run = models.BooleanField(default=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.process_user_constraint)
