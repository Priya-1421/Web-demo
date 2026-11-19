from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.shortcuts import render

from .models import *


def index(request):
    try:
        if request.session['log_id'] is not None:
            lid = request.session['log_id']
            user = login_table.objects.get(id=lid)
            sdetails = state_table.objects.all()
            cdetails = city.objects.all()
            adetails = area_table.objects.all()
            if user.usertype == 'User':
                try:
                    profiledata = user_detail_table.objects.get(l_id=lid)
                except user_detail_table.DoesNotExist:
                    profiledata = None
            elif user.usertype == "Company":
                try:
                    profiledata = company_table.objects.get(cmp_id=lid)
                except company_table.DoesNotExist:
                    profiledata = None
            print("PROFILEDATA",profiledata)
            context = {
                'state': sdetails,
                'city': cdetails,
                'area': adetails,
                'profiledata': profiledata,
                'user': user
            }
            if user.usertype == 'Company':
                return render(request,'index.html',context)
            else:
                return render(request,'userindex.html',context)
        else:
            return render(request,'login.html')
    except:
        return render(request,'index.html')


def login(request):
    return render(request,'login.html')


def logindata(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        usertype = request.POST.get("usertype")

        data = login_table(name=name,email_id=email,phone_no=phone,password=password,usertype=usertype)
        data.save()
        messages.success(request,"Data Inserted Successfully. You can Login now")
        return render(request,'login.html')
    else:
        messages.error(request,"Error occured")
        return redirect(signup)


def signup(request):
    return render(request,'signup.html')


def about(request):
    try:
        if request.session['log_id']:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            if user.usertype == "User":
                try:
                    profiledata = user_detail_table.objects.get(l_id=user.id)
                except:
                    profiledata = None
            elif user.usertype == "Company":
                try:
                    profiledata = company_table.objects.get(cmp_id=user.id)
                except:
                    profiledata = None
                print(user.usertype,"heloleoapd",profiledata)
            context = {
                'user':user,
                'profiledata': profiledata
            }
            return render(request,'about.html',context)
    except:
        return render(request,'login.html')


def blog(request):
    try:
        if request.session['log_id']:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            if user.usertype == "User":
                try:
                    profiledata = user_detail_table.objects.get(l_id=user.id)
                except:
                    profiledata = None
            elif user.usertype == "Company":
                try:
                    profiledata = company_table.objects.get(cmp_id=user.id)
                except:
                    profiledata = None
            context = {
                'user':user,
                'profiledata': profiledata
            }
            return render(request,'blog.html',context)
    except:
        return render(request,'login.html')


def blogs(request):
    try:
        if request.session['log_id']:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            if user.usertype == "User":
                try:
                    profiledata = user_detail_table.objects.get(l_id=user.id)
                except:
                    profiledata = None
            elif user.usertype == "Company":
                try:
                    profiledata = company_table.objects.get(cmp_id=user.id)
                except:
                    profiledata = None
            context = {
                'user':user,
                'profiledata': profiledata
            }
            return render(request,'blog-single.html',context)
    except:
        return render(request,'login.html')


def comings(request):
    try:
        if request.session['log_id'] is not None:
            return render(request,'coming-soon.html')
    except:
        return render(request,'login.html')


def contact(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            data = login_table.objects.get(id=uid)
            if data.usertype == "User":
                try:
                    profiledata = user_detail_table.objects.get(l_id=data.id)
                except:
                    profiledata = None
            elif data.usertype == "Company":
                try:
                    profiledata = company_table.objects.get(cmp_id=data.id)
                except:
                    profiledata = None
            context = {
                'data':data,
                'profiledata': profiledata
            }
            return render(request,'contact.html',context)
    except:
        return render(request,'login.html')


def managebooking(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            Company = False
            if user.usertype == "Company":
                Company = True
                try:
                    profiledata = company_table.objects.get(cmp_id=uid)
                except company_table.DoesNotExist:
                    profiledata = None
            elif user.usertype == "User":
                try:
                    profiledata = user_detail_table.objects.get(l_id=uid)
                except user_detail_table.DoesNotExist:
                    profiledata = None
            if Company:
                mybookingdata = booking_table.objects.filter(bid_id__login_id=uid)
            else:
                mydata = items_details.objects.filter(user_id=login_table(id=uid))
                mybookingdata = booking_table.objects.filter(item_id__in=mydata)

            # Paginate
            page = request.GET.get('page', 1)
            paginator = Paginator(mybookingdata, 3)  # Show 10 items per page
            try:
                mybookingdata = paginator.page(page)
            except PageNotAnInteger:
                mybookingdata = paginator.page(1)
            except EmptyPage:
                mybookingdata = paginator.page(paginator.num_pages)

            context = {
                'user': user,
                'Company': Company,
                'profiledata': profiledata,
                'mybookingdata': mybookingdata,
            }
            return render(request, 'Managebooking.html', context)
    except Exception as e:
        print("error",e)
        return render(request,'login.html')


def bidding(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            userdata = login_table.objects.get(id=uid)
            try:
                profiledata = user_detail_table.objects.get(l_id=uid)
                myitemdata = items_details.objects.filter(user_id=login_table(id=uid))
                mybiddata = bidding_table.objects.filter(item_id__in=myitemdata).exclude(bidstatus="Rejected")
                # Paginate
                page = request.GET.get('page', 1)
                paginator = Paginator(mybiddata, 3)
                try:
                    mybiddata = paginator.page(page)
                except PageNotAnInteger:
                    mybiddata = paginator.page(1)
                except EmptyPage:
                    mybiddata = paginator.page(paginator.num_pages)
            except:
                profiledata = None
                mybiddata = None
            context = {
                'userdata': userdata,
                'profiledata': profiledata,
                'mybiddata': mybiddata,
            }
            return render(request,'Bidding.html',context)
    except:
        return render(request,'login.html')


def Viewdata(request):
    try:
        if request.session['log_id']:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            try:
                profiledata = company_table.objects.get(cmp_id=user.id)
                mydata = bidding_table.objects.filter(login_id=login_table(id=uid))
            except:
                profiledata = None
                mydata = None
            page = request.GET.get('page', 1)
            paginator = Paginator(mydata, 3)
            try:
                mydata = paginator.page(page)
            except PageNotAnInteger:
                mydata = paginator.page(1)
            except EmptyPage:
                mydata = paginator.page(paginator.num_pages)
            context = {
                'user':user,
                'profiledata': profiledata,
                'mydata': mydata
            }
            return render(request,'Viewdata.html',context)
    except Exception as e:
        print(e)
        return render(request, 'login.html')


def services(request):
    try:
        if request.session['log_id']:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            if user.usertype == "User":
                try:
                    profiledata = user_detail_table.objects.get(l_id=user.id)
                    data = items_details.objects.filter(user_id=login_table(id=uid))
                except:
                    profiledata = None
                    data = None
            elif user.usertype == "Company":
                try:
                    profiledata = company_table.objects.get(cmp_id=user.id)
                except:
                    profiledata = None
                    data = None
            context = {
                'user':user,
                'data':data,
                'profiledata': profiledata
            }
            return render(request,'services.html',context)
    except:
        return render(request,'login.html')


def cmpservices(request,cityid):
    try:
        if request.session['log_id']:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            try:
                profiledata = company_table.objects.get(cmp_id=uid)
            except:
                profiledata = None
            data = items_details.objects.filter(fcity_id=cityid).exclude(status="unavailable")
            if data.exists():
                display = True
            else:
                display = False
            context = {
                'user': user,
                'data': data,
                'profiledata': profiledata,
                'display':display
            }
            return render(request,'services.html',context)
    except:
        return render(request,'login.html')


def servicess(request,itemid):
    try:
        if request.session['log_id']:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            item_data = items_details.objects.get(id=itemid)
            biddata = bidding_table.objects.filter(login_id=uid)
            if biddata.exists():
                for biddata in biddata:
                    if item_data.id == biddata.item_id.id:
                        bidstatus = False
                    else:
                        bidstatus = True
            else:
                bidstatus = True

            print("dsldsds\n",bidstatus)

            context = {
                'user': user,
                'data': item_data,
                'bid':bidstatus
            }
            return render(request,'services-single.html',context)
    except Exception as e:
        print("error",e)
        return render(request,'login.html')


def teams(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            if user.usertype == 'User':
                details = user_detail_table.objects.get(l_id=uid)

                context = {
                    'user': user, 'details': details
                }

                return render(request,'team-single.html',context)
            elif user.usertype == 'Company':
                details = company_table.objects.get(cmp_id=uid)

                context = {
                    'user': user, 'details': details
                }
                return render(request, 'team-single.html', context)
    except:
        return render(request,'login.html')


def signin(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = login_table.objects.get(email_id=email, password=password)
            try:
                request.session['log_email'] = user.email_id
                request.session['log_id'] = user.id
                request.session.save()

            except login_table.DoesNotExist:
                user = None

            if user is not None:
                messages.success(request,"Successfullt Log In !")
                if user.usertype == 'Company':
                    return redirect(index)
                if user.usertype == 'User':
                    return redirect(index)
    except:
        messages.error(request,"Please enter correct email and password")
        return render(request,'login.html')


def userindex(request):
    try:
        if request.session['log_email'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            try:
                profiledata = user_detail_table.objects.get(l_id=user.id)
            except user_detail_table.DoesNotExist:
                profiledata = None
            context = {
                'profiledata':profiledata
            }
            return render(request,'userindex.html',context)
        else:
            return render(request,'login.html')
    except:
        return render(request,'login.html')


def additemdetails(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            if request.method == "POST":
                itemname = request.POST.get('itemname')
                pickupaddress = request.POST.get('pickupaddress')
                dropaddress = request.POST.get('dropaddress')
                message = request.POST.get('message')
                state = request.POST.get('state')
                noofitems = request.POST.get('noofitems')
                itemweigh = request.POST.get('itemsweight')
                itemsphoto = request.FILES['itemsphoto']
                c = request.POST.get('city')
                area = request.POST.get('area')
                tstate = request.POST.get('tstate')
                tcity = request.POST.get('tcity')
                tarea = request.POST.get('tarea')

                data = items_details(user_id=login_table(id=uid),Item_name=itemname,Item_info=message,pickup_address=pickupaddress,
                                     drop_address=dropaddress,farea_id=area_table(id=area),fstate_id=state_table(id=state),
                                     fcity_id=city(id=c),tarea_id=tarea,tstate_id=tstate,
                                     tcity_id=tcity,no_of_items=noofitems,item_weight=itemweigh,item_images=itemsphoto)

                data.save()
                messages.success(request,'Data inserted succesfully')
                return redirect(services)
    except Exception as e:
        print('ERROR:',e)
        return render(request,'login.html')


def logout(request):
    try:
        if request.session['log_id'] is not None:
            del request.session['log_email']
            del request.session['log_id']
            return redirect(index)
    except:
            return redirect(index)


def editprofile(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            if user.usertype == 'User':
                role = 'User'
                details = user_detail_table.objects.get(l_id=uid)
            elif user.usertype == 'Company':
                role = 'Company'
                details = company_table.objects.get(cmp_id=uid)

            context = {
                'user': user,
                'role': role,
                'details': details

            }

            return render(request,'editprofile.html',context)
    except login_table.DoesNotExist:
        return render(request,'login.html')


def updateprofile(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            if user.usertype == 'User':
                details = user_detail_table.objects.get(l_id=uid)

                if request.method == 'POST':

                    name = request.POST.get("name")
                    phone = request.POST.get("phone")
                    email = request.POST.get("email")
                    address = request.POST.get("address")

                    user.name = name
                    user.phone_no = phone
                    user.email_id = email
                    details.address = address

                    if 'profilepic' in request.FILES:
                        profile = request.FILES["profilepic"]
                        details.photo = profile

                    if 'aadharphoto' in request.FILES:
                        aadhar = request.FILES["aadharphoto"]
                        details.aadhar = aadhar

                    user.save()
                    details.save()

                    context = {'user':user,'details':details}

                    messages.success(request, 'Your profile has been updated successfully.')
                    return render(request,'team-single.html',context)
            elif user.usertype == 'Company':
                details = company_table.objects.get(cmp_id=uid)

                if request.method == 'POST':

                    name = request.POST.get("name")
                    phone = request.POST.get("phone")
                    email = request.POST.get("email")
                    address = request.POST.get("address")

                    user.name = name
                    user.phone_no = phone
                    user.email_id = email
                    details.address = address

                    if 'profilepic' in request.FILES:
                        profile = request.FILES["profilepic"]
                        details.photo = profile

                    if 'aadharphoto' in request.FILES:
                        aadhar = request.FILES["aadharphoto"]
                        details.aadhar = aadhar

                    user.save()
                    details.save()

                    context = {'user': user, 'details': details}

                    messages.success(request, 'Your profile has been updated successfully.')
                    return render(request, 'profile.html', context)
    except user_detail_table.DoesNotExist:
        return render(request, "login.html")


def updatepassword(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)

            new_password = request.POST.get('passsword1')
            confirm_password = request.POST.get('password2')

            if new_password == confirm_password:
                user.password = new_password
                user.save()
                messages.success(request,'Password Updated')
                return render(request,'login.html')
            else:
                messages.error(request,'Error Occured!')
                return redirect(changepassword)
    except:
        return render(request,'login.html')


def changepassword(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            context = {
                'user':user
            }
            return render(request,'changepassword.html',context)
    except:
        return render(request,'login.html')


def rejectbid(request,id):
    try:
        if request.session['log_id'] is not None:
            bid = bidding_table.objects.get(id=id)
            bid.bidstatus = "Rejected"
            bid.save(update_fields=['bidstatus'])
            uid = request.session['log_id']
            userdata = login_table.objects.get(id=uid)
            profiledata = user_detail_table.objects.get(l_id=uid)
            myitemdata = items_details.objects.filter(user_id=login_table(id=uid))
            mybiddata = bidding_table.objects.filter(item_id__in=myitemdata).exclude(bidstatus="Rejected")
            context = {
                'userdata': userdata,
                'profiledata': profiledata,
                'mybiddata': mybiddata,
            }

            messages.error(request, 'Bid Rejected')
            return redirect(bidding)
    except:
        return render(request,'login.html')


def approvebid(request, abid):
    try:
        if request.session['log_id'] is not None:
            lid = request.session['log_id']
            bid = bidding_table.objects.get(id=abid)
            userdata = login_table.objects.get(id=lid)
            profiledata = user_detail_table.objects.get(l_id=lid)
            bid.bidstatus = "Approved"
            bid.apprflag = 1
            bid.save(update_fields=['bidstatus','apprflag'])

            uid = bid.item_id.id
            status = "Pending"

            bookingdata = booking_table(item_id=items_details(id=uid), bid_id=bidding_table(id=abid), payment_status=status)
            bookingdata.save()

            mydata = items_details.objects.filter(user_id=login_table(id=uid),id=uid)

            try:
                mybiddata = bidding_table.objects.filter(item_id__in=mydata).exclude(bidstatus="Approved")
            except bidding_table.DoesNotExist:
                mybiddata = None

            for mb in mybiddata:
                mb.bidstatus = "Rejected"
                mb.save(update_fields=['bidstatus'])

            messages.success(request, 'Bid Approved Please refer My bookings tab for further process.')
            context = {
                'userdata': userdata,
                'profiledata': profiledata,
                'mybiddata': mybiddata,
            }
            return redirect(bidding)
    except:
        return render(request,'login.html')


def feedbackpage(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            if user.usertype == "User":
                try:
                    profiledata = user_detail_table.objects.get(l_id=user.id)
                except:
                    profiledata = None
            elif user.usertype == "Company":
                try:
                    print("USERTYPE: \n", user.usertype)
                    profiledata = company_table.objects.get(cmp_id=user.id)
                except:
                    profiledata = None
            context = {
                'data':user,
                'profiledata': profiledata
            }
            return render(request,'Feedback.html',context)
    except:
        return render(request,'login.html')


def addfeedback(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            details = login_table.objects.get(id=uid)
            sdetails = state_table.objects.all()
            cdetails = city.objects.all()
            adetails = area_table.objects.all()
            if request.method == "POST":
                name = request.POST.get("name")
                email = request.POST.get("email")
                phone = request.POST.get("phone")
                ratings = request.POST.get("rating")
                message = request.POST.get("message")

                data = feedback(name=name,email=email,phone=phone,message=message,ratings=ratings)
                data.save()
                messages.success(request,'Thanks for the feedback')
                if details.usertype == 'User':
                    return redirect(index)
                elif details.usertype == 'Company':
                    return redirect(index)
    except:
        return render(request,'login.html')


def addcomplain(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            details = login_table.objects.get(id=uid)
            sdetails = state_table.objects.all()
            cdetails = city.objects.all()
            adetails = area_table.objects.all()
            if request.method == "POST":
                name = request.POST.get("name")
                email = request.POST.get("email")
                phone = request.POST.get("phone")
                message = request.POST.get("message")

                data = complain(name=name,email=email,phone=phone,message=message)
                data.save()
                messages.success(request,'Sorry for the inconvience')
                if details.usertype == 'User':
                    return redirect(index)
                elif details.usertype == 'Company':
                    return redirect(index)
    except:
        return render(request,'login.html')


def biddingdata(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            city_id = request.POST.get('city')
            return redirect(cmpservices,city_id)
    except:
        return render(request,'login.html')


def userprofilepage(request,userid):
    try:
        if request.session['log_id'] is not None:
            id = request.session['log_id']
            user = login_table.objects.get(id=userid)
            if user.usertype == 'User':
                details = user_detail_table.objects.get(l_id=userid)
                context = {
                            'user': user, 'details': details
                }

        return render(request, 'team-single.html', context)
    except:
        return render(request,'login.html')


def makeabid(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            if request.method == 'POST':
                bidamount = request.POST.get("bidamount")
                itemid = request.POST.get("itemid")
                # data = user_detail_table.objects.get(l_id=uid)
                from django.utils import timezone
                current_date = timezone.now().date()
                biddata = bidding_table(login_id=login_table(id=uid), item_id=items_details(id=itemid),
                                        bidamount=bidamount, bidstatus="Submitted", bidapprovedate=current_date)
                biddata.save()
                messages.success(request, 'Bid Submitted Successfully')
                return redirect(index)
    except Exception as e:
        print("error",e)
        return render(request,'login.html')


def makepayment(request,mid):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            bookingdata = booking_table.objects.get(item_id=mid)
            context = {
                'mid': mid,
                'bookingdata': bookingdata
            }
            return render(request,'coming-soon.html',context)
    except:
        return render(request,'login.html')


def paymentsubmit(request):
    try:
        if request.session['log_id'] is not None:
            if request.method == 'POST':
                cardname = request.POST.get("name")
                cardnumber = request.POST.get("cardnumber")
                expiry = request.POST.get("expiry")
                cvv = request.POST.get("cvv")
                paymentamount = request.POST.get("paymentamount")
                bookingid = request.POST.get("bookingid")

                bookingobj = booking_table.objects.get(bid_id=bookingid)
                bidid = bookingobj.bid_id.id

                cardobj = card_detail.objects.get()
                cardbal = cardobj.card_balance
                # print("this is amount " + paymentamount)
                # print(type(paymentamount))

                ipaymentamount = int(paymentamount)

                if cardnumber == "4321432143214321" and expiry == "1234" and cvv == "321" and cardbal >= ipaymentamount:

                    bookingobj.payment_status = "Done"
                    bookingobj.save(update_fields=['payment_status'])
                    curbal = cardobj.card_balance
                    cardobj.card_balance = curbal - ipaymentamount
                    cardobj.save(update_fields=['card_balance'])

                    from django.utils import timezone
                    current_date = timezone.now().date()

                    bidobj = bidding_table.objects.get(id=bidid)
                    itemid = bidobj.item_id.id
                    itembj = items_details.objects.get(id=itemid)
                    itembj.status = "unavailable"
                    itembj.save(update_fields=['status'])
                    bidobj.bidstatus = "Payment is Done. Bid is closed now."
                    bidobj.bidapprovedate = current_date
                    bidobj.apprflag = 1
                    bidobj.save(update_fields=['bidstatus','bidapprovedate','apprflag'])

                    paymentdata = payment_table(booking_id=booking_table(id=bookingobj.id),bid_id=bidding_table(id=bidid), amount=ipaymentamount,p_status="Successful")
                    paymentdata.save()
                    messages.success(request, 'Payment Done Successfully.')
                    return redirect(managebooking)
                else:
                    paymentdata = payment_table(booking_id=booking_table(id=bookingobj.id), bid_id=bidding_table(id=bidid),amount=ipaymentamount,
                                                p_status="Failed")
                    print(paymentdata)
                    # paymentdata.save()
                    messages.error(request, 'Transaction Failed')
                    return redirect(managebooking)
    except Exception as e:
        print("error",e)
        return render(request,'login.html')


def edititem(request,id):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            profiledata = user_detail_table.objects.get(l_id=uid)
            itemdata = items_details.objects.get(id=id)
            statedetail = state_table.objects.all()
            citydetail = city.objects.all()
            areadetail = area_table.objects.all()
            edit = True
            context = {
                    'user': user,
                    'edit': edit,
                    'profiledata': profiledata,
                    'state': statedetail,
                    'city': citydetail,
                    'area': areadetail,
                    'itemdata': itemdata
            }
            return render(request,'items.html',context)
    except:
        return render(request,'login.html')


def removeitem(request,id):
    try:
        if request.session['log_id'] is not None:
            mydata = items_details.objects.get(id=id)
            try:
                mybiddata = bidding_table.objects.filter(item_id=mydata)
            except bidding_table.DoesNotExist:
                mybiddata = None

            if mybiddata.exists():
                messages.error(request, 'You Can not remove this')
                return redirect(servicess,id)
            else:
                mydata.status = "unavailable"
                mydata.save(update_fields=['status'])
                messages.error(request, 'Successfully removed from user pannel')
                return redirect(servicess,id)
    except Exception as e:
        print("error",e)
        return render(request,'login.html')


def updateitem(request,id):
    try:
        if request.session['log_id'] is not None:
            data = items_details.objects.get(id=id)
            uid = request.session['log_id']
            if request.method == "POST":
                pickupaddress = request.POST.get('pickupaddress')
                dropaddress = request.POST.get('dropaddress')
                message = request.POST.get('message')
                state = request.POST.get('state')
                noofitems = request.POST.get('noofitems')
                itemweigh = request.POST.get('itemsweight')
                c = request.POST.get('city')
                area = request.POST.get('area')
                tstate = request.POST.get('tstate')
                tcity = request.POST.get('tcity')
                tarea = request.POST.get('tarea')

                if 'itemsphotos' in request.FILES:
                    profile = request.FILES["itemsphotos"]
                    data.item_images = profile

                data.pickup_address = pickupaddress
                data.drop_address = dropaddress
                data.Item_info = message
                data.fstate_id = state_table.objects.get(id=state)
                data.fcity_id = city.objects.get(id=c)
                data.farea_id = area_table.objects.get(id=area)
                data.tstate_id = tstate
                data.tcity_id = tcity
                data.tarea_id = tarea
                data.no_of_items = noofitems
                data.item_weight = itemweigh
                data.save()
                messages.success(request, 'Data Updated succesfully')
                return redirect(services)
    except Exception as e:
        print('Error',e)
        return render(request,'login.html')


def viewdata(request,itemid):
    try:
        if request.session['log_id'] is not None:
            return redirect(servicess,itemid)
    except Exception as e:
        print("error",e)
        return render(request,'login.html')


def displayitemform(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            if user.usertype == "User":
                try:
                    profiledata = user_detail_table.objects.get(l_id=user.id)
                except:
                    profiledata = None
            statedetail = state_table.objects.all()
            citydetail = city.objects.all()
            areadetail = area_table.objects.all()
            context = {
                'state':statedetail,
                'city':citydetail,
                'area': areadetail,
                'user': user,
                'profiledata':profiledata
            }
            return render(request,'items.html',context)
    except:
        return redirect(index)


def forgotpassword(request):
    return render(request,'forgotpassword.html')


def forgotpwd(request):
    if request.method == 'POST':
        username = request.POST['email']
        try:
            user = login_table.objects.get(email_id=username)

        except login_table.DoesNotExist:
            user = None

        # if user exist then only below condition will run otherwise it will give error as described in else condition.
        if user is not None:
            #################### Password Generation ##########################
            import random
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  # we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################

            msg = "hello here it is your new password  " + password  # this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail
            send_mail(
                "Forgot Password Update",
                msg,
                "krushanuinfolabz@gmail.com",
                [username],
                fail_silently=False,
            )

            # now update the password in model
            cuser = login_table.objects.get(email_id=username)
            cuser.password = password
            cuser.save(update_fields=['password'])

            print('Mail sent')
            messages.info(request, 'mail is sent')
            return redirect(index)

        else:
            messages.info(request, 'This account does not exist')
            return redirect(index)

    return render(request, "index.html")

def completerpofile(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            try:
                profiledata = user_detail_table.objects.get(l_id=user.id)
            except:
                profiledata = None
            if user.usertype == "Company":
                state = state_table.objects.all()
                context = {
                    'user': user,
                    'profiledata':profiledata,
                    'state':state
                }
                return render(request,'profile.html',context)
            elif user.usertype == "User":
                context = {
                    'user': user,
                    'profiledata':profiledata
                }
                return render(request,'profile.html',context)
    except:
        return render(request,'login.html')


def completeprofilesubmit(request):
    try:
        if request.session['log_id'] is not None:
            uid = request.session['log_id']
            user = login_table.objects.get(id=uid)
            if user.usertype == "User":
                if request.method == "POST":
                    uaddress = request.POST.get('address')
                    udob = request.POST.get("dob")
                    file = request.FILES['profilepic']
                    aadharfile = request.FILES['aadharphoto']
                    userdata = user_detail_table(l_id=login_table(id=uid), dob=udob, address=uaddress, photo=file, aadhar=aadharfile)
                    userdata.save()
                    messages.success(request, 'Data Inserted Successfully.')
                    return redirect(index)
                else:
                    messages.error(request,'error occured')
            elif user.usertype == "Company":
                state = state_table.objects.all()
                if request.method == "POST":
                    caddress = request.POST.get('address')
                    regno = request.POST.get('Registernumber')
                    secondno = request.POST.get('secondnumber')
                    servicestate = request.POST.get('state')
                    movingtype = request.POST.get('servicearea')

                    userdata = company_table(cmp_id=login_table(id=uid),address=caddress,reg_no=regno,second_number=secondno,service_area=state_table(id=servicestate),Movingtype=movingtype)
                    userdata.save()
                    messages.success(request, 'Data Inserted Successfully.')
                    return redirect(index)
                else:
                    messages.error(request, 'error occured')

    except:
        return render(request,'login.html')


