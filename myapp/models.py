from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
class login_table(models.Model):
    name = models.CharField(max_length=100)
    email_id = models.EmailField()
    phone_no = models.IntegerField()
    password = models.CharField(max_length=300, default="admin")
    ROLE = (
        ("Company", "Company"),
        ("User", "User")
    )
    usertype = models.CharField(max_length=100, choices=ROLE)

    def __str__(self):
        return self.name


class user_detail_table(models.Model):
    l_id = models.ForeignKey(login_table, on_delete=models.CASCADE)
    dob = models.DateField()
    address = models.TextField()
    photo = models.ImageField(upload_to="media/photos")
    aadhar = models.ImageField(upload_to="media/photos")

    def aadhar_photo(self):
        return mark_safe('<img src ="{}" width ="100"/>'.format(self.aadhar.url))

    aadhar_photo.allow_tags = True

    def user_photos(self):
        return mark_safe('<img src ="{}" width ="100"/>'.format(self.photo.url))

    user_photos.allow_tags = True

    def __str__(self):
        return self.l_id.name


class state_table(models.Model):
    state_name = models.CharField(max_length=25)

    def __str__(self):
        return self.state_name


class city(models.Model):
    city_name = models.CharField(max_length=25)
    state_id = models.ForeignKey(state_table, on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name


class area_table(models.Model):
    city_id = models.ForeignKey(city, on_delete=models.CASCADE)
    state_id = models.ForeignKey(state_table, on_delete=models.CASCADE)
    area_name = models.CharField(max_length=25)

    def __str__(self):
        return self.area_name


class company_table(models.Model):
    cmp_id = models.ForeignKey(login_table, on_delete=models.CASCADE)
    address = models.TextField()
    reg_no = models.CharField(max_length=45)
    second_number = models.IntegerField()
    service_area = models.ForeignKey(state_table,on_delete=models.CASCADE)
    type = (
        ("Commercial", "Commercial"),
        ("Residential", "Residentail"),
        ("Both","Both")
    )
    Movingtype = models.CharField(max_length=100, choices=type)

    def __str__(self):
        return self.cmp_id.name


class items_details(models.Model):
    user_id = models.ForeignKey(login_table, on_delete=models.CASCADE)
    Item_name = models.CharField(max_length=50,null=True)
    Item_info = models.TextField()
    pickup_address = models.TextField()
    drop_address = models.TextField()
    Status = (
        ('available', 'available'),
        ('unavailable', 'unavailable'),
    )
    status = models.CharField(max_length=150, choices=Status,default='available')
    farea_id = models.ForeignKey(area_table, on_delete=models.CASCADE)
    tarea_id = models.CharField(max_length=50)
    fcity_id = models.ForeignKey(city, on_delete=models.CASCADE)
    tcity_id = models.CharField(max_length=50)
    fstate_id = models.ForeignKey(state_table, on_delete=models.CASCADE)
    tstate_id = models.CharField(max_length=50)
    no_of_items = models.IntegerField()
    item_weight = models.CharField(max_length=10)
    item_images = models.ImageField(upload_to='product_photos')

    def product_photos(self):
        return mark_safe('<img src="{}" width="100">'.format(self.item_images.url))


class bidding_table(models.Model):
    login_id = models.ForeignKey(login_table, on_delete=models.CASCADE)
    item_id = models.ForeignKey(items_details, on_delete=models.CASCADE)
    bidamount = models.IntegerField()
    bidstatus = models.CharField(max_length=50)
    biddate = models.DateField(auto_now=True)
    bidapprovedate = models.DateField()
    apprflag = models.BooleanField(default=0)


class booking_table(models.Model):
    item_id = models.ForeignKey(items_details, on_delete=models.CASCADE)
    bid_id = models.ForeignKey(bidding_table, on_delete=models.CASCADE)
    Status = (
        ('Done', 'Done'),
        ('Pending', 'Pending'),
    )
    payment_status = models.CharField(max_length=150, choices=Status)


class payment_table(models.Model):
    booking_id = models.ForeignKey(booking_table, on_delete=models.CASCADE)
    bid_id = models.ForeignKey(bidding_table, on_delete=models.CASCADE)
    amount = models.CharField(max_length=150)
    Status = (
        ('Successful', 'Successful'),
        ('Failed', 'Failed'),
    )
    p_status = models.CharField(max_length=150, choices=Status)
    datetime = models.DateTimeField(auto_now=True)


class card_detail(models.Model):
    name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=50)
    card_cvv = models.CharField(max_length=50)
    exp_date = models.CharField(max_length=50)
    card_balance = models.IntegerField(default=1000000)

    def __str__(self):
        return self.card_number


class complain(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.IntegerField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class feedback(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.IntegerField()
    ratings = models.IntegerField(null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
