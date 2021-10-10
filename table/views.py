from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import (login_table, login_time, num_of_leaves, cur_running,
                              app_status, cse_dep, ee_dep, mec_dep, hoddean,
                              cse_hod, mec_hod, ee_hod, hod_dean, director, dean, hodapp, deanapp, dirapp)
from random import randint
#from django_random_id_model import RandomIDModel
from django.db import connection
from django.db.models import OuterRef, Subquery, DateTimeField
from datetime import date

def home(request):
    if request.method == 'POST' :
        idd = request.POST['id']
        pas = request.POST['password']
        p = login_table.objects.get(id = idd)
        f = login_time(pro_id = idd)
        if p.password == pas and p.pos =='faculty':
            f.save()
            return render(request,'faculty.html',{'data':p})
        if p.pos =='Dean' or p.pos =='CSEHOD' or p.pos == 'EEHOD' or p.pos =='MECHOD':
            if p.password == pas:
                f.save()
                return render(request,'deanhod.html',{'data':p})
        if p.pos =='Director' and p.password == pas:
            f.save()
            return render(request,"director.html",{'data':p})
        if p.password != pas:
            return HttpResponse("Incorrect Password")

    #p = login_table.objects.all()
    else :
        a = cse_dep.objects.all()
        for i in a:
            if i.datefrom < date.today():
                b = app_status(i.id,'Rejected')
                b.save()
        a = ee_dep.objects.all()
        for i in a:
            if i.datefrom < date.today():
                b = app_status(i.id,'Rejected')
                b.save()
        a = mec_dep.objects.all()
        for i in a:
            if i.datefrom < date.today():
                b = app_status(i.id,'Rejected')
                b.save()
        a = hod_dean.objects.all()
        for i in a:
            if i.datefrom < date.today():
                b = app_status(i.id,'Rejected')
                b.save()
        a = hoddean.objects.all()
        for i in a:
            try:
                d = login_table.objects.filter(id = i.pro_id, pos = 'faculty')
            except login_table.DoesNotExist:
                d = None
            if d is  None:
                if i.datefrom < date.today():
                    b = app_status(i.id,'Rejected')
                    b.save()
            else:
                e = login_table.objects.get(id = i.pro_id)
                if i.datefrom < date.today() and e.pos != 'faculty':
                    b = app_status(i.id,'Rejected')
                    b.save()


        return render(request,"home.html")

def leaves(request, pro):
    #print(pro_id)
    #f=num_of_leaves.objects.all()
    f = num_of_leaves.objects.filter(pro_id = pro)
    return render(request,"leaves.html",{'data':f})

def application(request, pro):
    if request.method =='POST':
        idd = int(request.POST['id'])
        datefrom = request.POST['datefrom']
        dateto = request.POST['dateto']
        numofdays = request.POST['numofdays']
        reason = request.POST['reason']
        is_unique = True
        while is_unique == True:
            pk = randint(1000, 1999) # 19 digits: 1, random 18 digits
            is_unique = cur_running.objects.filter(id=pk).exists()
        print(pro)
        if pro == idd :
            p = cur_running(id = pk, pro_id = idd, datefrom = datefrom, dateto = dateto, reason = reason, num_of_days = numofdays)
            p.save()
            return HttpResponse("Done")
        else:
            return HttpResponse("enter your valid id")
    else:
        ok = pro
        f = login_table.objects.get(id = pro)
        if f.dept_name == 'CSE' and f.pos =='faculty':
            try :
                user =  cse_dep.objects.get(pro_id = ok)
            except cse_dep.DoesNotExist:
                user = None
            if user is None :
                return render(request,"application.html",{'data':pro})
            else:
                return HttpResponse("You have One application running")

        if f.dept_name == 'EE'and f.pos =='faculty':
            try :
                user =  ee_dep.objects.get(pro_id = ok)
            except ee_dep.DoesNotExist:
                user = None
            if user is None  :
                return render(request,"application.html",{'data':pro})
            else:
                return HttpResponse("You have One application running")

        if f.dept_name == 'MEC'and f.pos =='faculty':
            try :
                user =  mec_dep.objects.get(pro_id = ok)
            except mec_dep.DoesNotExist:
                user = None
            if user is None  :
                return render(request,"application.html",{'data':pro})
            else:
                return HttpResponse("You have One application running")


        if f.pos == 'Dean' or f.pos =='CSEHOD' or f.pos =='EEHOD' or f.pos =='MECHOD':
            try :
                user =  hoddean.objects.get(pro_id = ok)
            except hoddean.DoesNotExist:
                user = None
            if user is None  :
                return render(request,"application.html",{'data':pro})
            else:
                return HttpResponse("You have One application running")

def logout(request,pro):
    return redirect('home')

def show(request, pro):
    ok = pro
    f = login_table.objects.get(id = pro)
    if f.dept_name == 'CSE' and f.pos =='faculty':
        try :
            user =  cse_dep.objects.get(pro_id = ok)
        except cse_dep.DoesNotExist:
            user = None
        if user is None :
            return HttpResponse("You don't have any current running application or appllication has been approved or rejected")
        else:
           try :
            g =  cse_hod.objects.get(id = user.id)
           except cse_hod.DoesNotExist:
            g = None
           if g is None:
               return HttpResponse("pending at HOD")
           else :
               if g.status == 'Rejected':
                  return  HttpResponse("your application is rejected with comment %s" % g.comm)
               else:
                    try :
                         j =  dean.objects.get(id = user.id)
                    except dean.DoesNotExist:
                         j = None
                    if j is None:
                        return HttpResponse("pending at DEAN and your application is accepted at HOD with comment %s" % g.comm)
                    else:
                        if j.status =="Approval":
                            return HttpResponse("Approved by DEAN with comm %s" % j.comm)
                        else:
                            return HttpResponse("Rejected by DEAN with comm %s" % j.comm)



    if f.dept_name == 'EE' and f.pos =='faculty':
        try :
            user =  ee_dep.objects.get(pro_id = ok)
        except ee_dep.DoesNotExist:
            user = None
        if user is None :
            return HttpResponse("You don't have any current running application or appllication has been approved or rejected")
        else:
           try :
            g =  ee_hod.objects.get(id = user.id)
           except ee_hod.DoesNotExist:
            g = None
           if g is None:
               return HttpResponse("pending at HOD")
           else :
               if g.status == 'Rejected':
                  return  HttpResponse("your application is rejected with comment %s" % g.comm)
               else:
                    try :
                         j =  dean.objects.get(id = user.id)
                    except dean.DoesNotExist:
                         j = None
                    if j is None:
                        return HttpResponse("pending at DEAN and your application is accepted at HOD with comment %s" % g.comm)
                    else:
                        if j.status =="Approval":
                            return HttpResponse("Approved by DEAN with comm %s" % j.comm)
                        else:
                            return HttpResponse("Rejected by DEAN with comm %s" % j.comm)

    if f.dept_name == 'MEC' and f.pos =='faculty':
        try :
            user =  mec_dep.objects.get(pro_id = ok)
        except mec_dep.DoesNotExist:
            user = None
        if user is None :
            return HttpResponse("You don't have any current running application or appllication has been approved or rejected")
        else:
           try :
            g =  mec_hod.objects.get(id = user.id)
           except mec_hod.DoesNotExist:
            g = None
           if g is None:
               return HttpResponse("pending at HOD")
           else :
               if g.status == 'Rejected':
                  return  HttpResponse("your application is rejected with comment %s" % g.comm)
               else:
                    try :
                         j =  dean.objects.get(id = user.id)
                    except dean.DoesNotExist:
                         j = None
                    if j is None:
                        return HttpResponse("pending at DEAN and your application is accepted at HOD with comment %s" % g.comm)
                    else:
                        if j.status =="Approval":
                            return HttpResponse("Approved by DEAN with comm %s" % j.comm)
                        else:
                            return HttpResponse("Rejected by DEAN with comm %s" % j.comm)


    if f.pos =='Dean' or f.pos =='CSEHOD' or f.pos == 'EEHOD' or f.pos =='MECHOD':
        try :
            user =  hoddean.objects.get(pro_id = ok)
        except hoddean.DoesNotExist:
            user = None
        if user is None :
            return HttpResponse("You don't have any current running application or appllication has been approved or rejected")
        else:
           try :
            g =  director.objects.get(id = user.id)
           except director.DoesNotExist:
            g = None
           if g is None:
               return HttpResponse("pending at DIRECTOR")
           else :
               if g.status == 'Rejected':
                  return  HttpResponse("your application is rejected with comment %s" % g.comm)
               else:
                   return  HttpResponse("your application is Approved with comment %s" % g.comm)





def status(request, pro):
    if request.method == 'POST':
        f = login_table.objects.get(id = pro)
        #if f.pos == 'CSEHOD' or f.pos =='EEHOD' or f.pos =='MECHOD':
        sta = request.POST['status']
        reason = request.POST['reason']
        idd = request.POST['id']
        f = login_table.objects.get(id = pro)
        if f.pos == 'CSEHOD':
            if cse_hod.objects.filter(id = idd):
                return HttpResponse("You already have marked")
            else:
                g = cse_hod(id = idd, status = sta, comm = reason)
                g.save()
                l = hodapp(app_id = idd, pro_id = pro)
                l.save()
                return HttpResponse("Application marked")
        if f.pos == 'EEHOD':
            if ee_hod.objects.filter(id = idd):
                return HttpResponse("You already have marked")
            else:
                g = ee_hod(id = idd, status = sta, comm = reason)
                g.save()
                l = hodapp(app_id = idd, pro_id = pro)
                l.save()
                return HttpResponse("Application marked")
        if f.pos == 'MECHOD':
            if mec_hod.objects.filter(id = idd):
                return HttpResponse("You already have marked")
            else:
                g = mec_hod(id = idd, status = sta, comm = reason)
                g.save()
                l = hodapp(app_id = idd, pro_id = pro)
                l.save()
                return HttpResponse("Application marked")
        if f.pos == 'Dean':
            if dean.objects.filter(id = idd):
                return HttpResponse("You already have marked")
            else:
                g = dean(id = idd, status = sta, comm = reason)
                g.save()
                l = deanapp(app_id = idd, pro_id = pro)
                l.save()
                return HttpResponse("Application marked")

        if f.pos == 'Director':
            if director.objects.filter(id = idd):
                return HttpResponse("You already have marked")
            else:
                g = director(id = idd, status = sta, comm = reason)
                g.save()
                l = dirapp(app_id = idd, pro_id = pro)
                l.save()
                return HttpResponse("Application marked")


    else:
        f = login_table.objects.get(id = pro)
        if f.pos == 'CSEHOD':
            try:
                user =cse_dep.objects.all()

            except cse_dep.DoesNotExist:
                 user = None

            if user is None:
                return HttpResponse("No pending Application")
            else:
                print(user)
                return render(request,"status.html",{'data':user})

        if f.pos == 'EEHOD':
            try :
                user =  ee_dep.objects.all()
            except ee_dep.DoesNotExist:
                user = None
            if user is None:
                return HttpResponse("No pending Application")
            else:
                #g = ee_dep.objects.raw('SELECT * FROM ee_dep wHERE ee_dep.id NOT EXISTS (SELECT ee_hod.id FROM ee_hod)')
                return render(request,"status.html",{'data':user})

        if f.pos == 'MECHOD':
            try :
                user = mec_dep.objects.all()
            except mec_dep.DoesNotExist:
                user = None
            if user is None:
                return HttpResponse("No pending Application")
            else:
                 #g = mec_dep.objects.raw('SELECT * FROM mec_dep wHERE mec_dep.id NOT EXISTS (SELECT mec_hod.id FROM mec_hod)')
                 return render(request,"status.html",{'data':user})

        if f.pos == 'Dean':
            try :
                user = hod_dean.objects.all()
            except hod_dean.DoesNotExist:
                user = None
            if user is None:
                return HttpResponse("No pending Application")
            else:
                 #g = hod_dean.objects.raw('SELECT * FROM hod_dean wHERE hod_dean.id NOT EXISTS (SELECT dean.id FROM dean)')
                 return render(request,"status.html",{'data':user})

        if f.pos =='Director':
            try :
                user = hoddean.objects.all()
            except hoddean.DoesNotExist:
                user = None
            if user is None:
                print(1)
                return HttpResponse("No pending Application")
            else:
                 #g = hod_dean.objects.raw('SELECT * FROM hod_dean wHERE hod_dean.id NOT EXISTS (SELECT dean.id FROM dean)')
                 return render(request,"status.html",{'data':user})



def changecsehod(request,pro):
        if request.method == 'POST':
            pro_id = request.POST['id']
            pos = request.POST['status']
            if pos =='CSEHOD':
                login_table.objects.filter(pos = 'CSEHOD').update(pos = 'faculty')
                login_table.objects.filter(id = pro_id).update(pos = 'CSEHOD')
                return HttpResponse("done")
            else:
                login_table.objects.filter(pos = 'Dean').update(pos = 'faculty')
                login_table.objects.filter(id = pro_id).update(pos = 'Dean')
                return HttpResponse("done")
        else:
            try :
                p = login_table.objects.filter(dept_name = 'CSE')
            except login_table.DoesNotExist:
                p = None
            if p is None:
                return HttpResponse("No CSE FACULTY")
            else:
                return render(request,"csehod.html",{'data':p})

def changeeehod(request,pro):
        if request.method == 'POST':
            pro_id = request.POST['id']
            pos = request.POST['status']
            if pos =='EEHOD':
                login_table.objects.filter(pos = 'EEHOD').update(pos = 'faculty')
                login_table.objects.filter(id = pro_id).update(pos = 'EEHOD')
                return HttpResponse("done")
            else:
                login_table.objects.filter(pos = 'Dean').update(pos = 'faculty')
                login_table.objects.filter(id = pro_id).update(pos = 'Dean')
                return HttpResponse("done")
        else:
            try :
                p = login_table.objects.filter(dept_name = 'EE')
            except login_table.DoesNotExist:
                p = None
            if p is None:
                return HttpResponse("No EE FACULTY")
            else:
                return render(request,"eehod.html",{'data':p})

def changemechod(request,pro):
        if request.method == 'POST':
            pro_id = request.POST['id']
            pos = request.POST['status']
            if pos =='MECHOD':
                login_table.objects.filter(pos = 'MECHOD').update(pos = 'faculty')
                login_table.objects.filter(id = pro_id).update(pos = 'MECHOD')
                return HttpResponse("done")
            else:
                login_table.objects.filter(pos = 'Dean').update(pos = 'faculty')
                login_table.objects.filter(id = pro_id).update(pos = 'Dean')
                return HttpResponse("done")
        else:
            try :
                p = login_table.objects.filter(dept_name = 'MEC')
            except login_table.DoesNotExist:
                p = None
            if p is None:
                return HttpResponse("No MEC FACULTY")
            else:
                return render(request,"mechod.html",{'data':p})

def changedean(request,pro):
        if request.method == 'POST':
            pro_id = request.POST['id']
            pos = request.POST['status']
            login_table.objects.filter(pos = 'Dean').update(pos = 'faculty')
            login_table.objects.filter(id = pro_id).update(pos = 'Dean')
            return HttpResponse("done")
        else:
            try :
                p = login_table.objects.all()
            except login_table.DoesNotExist:
                p = None
            if p is None:
                return HttpResponse("No FACULTY")
            else:
                return render(request,"changedean.html",{'data':p})
