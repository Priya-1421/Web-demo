from django.contrib import admin
from .models import *
# Register your models here.


class LOGIN_TABLE(admin.ModelAdmin):
    list_display = ["name","email_id","phone_no","password","usertype"]
admin.site.register(login_table,LOGIN_TABLE)


class USER_TABLE(admin.ModelAdmin):
    list_display = ["l_id","dob","address","user_photos","aadhar_photo"]
admin.site.register(user_detail_table,USER_TABLE)


class ITEM_TABLE(admin.ModelAdmin):
    list_display = ["user_id","Item_name","Item_info","status","pickup_address","drop_address","no_of_items","item_weight","product_photos","farea_id","fcity_id","fstate_id","tarea_id","tcity_id","tstate_id"]


admin.site.register(items_details,ITEM_TABLE)


class BID_TABLE(admin.ModelAdmin):
    list_display = ["login_id","item_id","bidamount","bidstatus","biddate","bidapprovedate","apprflag"]
admin.site.register(bidding_table,BID_TABLE)


class BOOKING_TABLE(admin.ModelAdmin):
    list_display = ["item_id","bid_id","payment_status"]
admin.site.register(booking_table,BOOKING_TABLE)


class PAYMENT_TABLE(admin.ModelAdmin):
    list_display = ["id","booking_id","bid_id","amount","p_status","datetime"]
admin.site.register(payment_table,PAYMENT_TABLE)


class Card_Detail(admin.ModelAdmin):
    list_display = ["name","card_number","card_cvv","exp_date","card_balance"]
admin.site.register(card_detail,Card_Detail)


class STATE_TABLE(admin.ModelAdmin):
    list_display = ["state_name"]
admin.site.register(state_table,STATE_TABLE)


class CITY_TABLE(admin.ModelAdmin):
    list_display = ["city_name","state_id"]
admin.site.register(city,CITY_TABLE)


class AREA_TABLE(admin.ModelAdmin):
    list_display =  ["city_id","state_id","area_name"]
admin.site.register(area_table,AREA_TABLE)


class COMPANY(admin.ModelAdmin):
    list_display = ["cmp_id","address","reg_no","second_number","service_area","Movingtype"]
admin.site.register(company_table,COMPANY)


class COMPLAIN(admin.ModelAdmin):
    list_display = ["name","email","phone","message","timestamp"]
admin.site.register(complain,COMPLAIN)

class FEEDBACK(admin.ModelAdmin):
    list_display = ["name","email","phone","ratings","message","timestamp"]
admin.site.register(feedback,FEEDBACK)