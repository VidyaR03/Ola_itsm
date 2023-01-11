class loginauth(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    roleid = models.IntegerField()
    
    class Meta:
        db_table = "loginauth"