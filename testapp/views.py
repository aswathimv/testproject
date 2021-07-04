from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from testapp.models import *
# from django.contrib.auth import User
import django.db.models
import datetime
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout
from django.db.models import Q
import json
import base64

# Create your views here.
def first(request):
	return render(request,'login.html')

def newacc(request):
	return render(request,'register.html')

def register(request):
	if request.method=="POST":
		fname=request.POST['fname']
		lname=request.POST['lname']
		email=request.POST['email']
		pwd=request.POST['pwd']
		v=base64.b64encode(pwd.encode("utf-8"))
		add=loginn(fname=fname,email=email,lname=lname,pwd=v)
		add.save()
		return render(request,'login.html')
	else:
		return HttpResponseRedirect('/register/')

def login(request):
	if request.method=="POST":
		email=request.POST['email']
		pwd=request.POST['pwd']
		v=base64.b64encode(pwd.encode("utf-8"))
		check=loginn.objects.all().filter(email=email,pwd=v)
		if check:
			for x in check:
				request.session['loginid']=x.id
			return render(request,'index.html')
		else:
			return render(request,'login.html',{"mssg":"Are you registered ?"})
	else:
		return render(request,'login.html')
def index(request):
	if request.session.has_key('loginid'):
		a=request.session['loginid']
		c=Customer.objects.all().filter(id=a)
		for m in c:
			namee=m.TrdName
		return render(request,'index.html',{'a':namee})
	else:
		return HttpResponseRedirect('/login')

# ----------------------------------------------Customer----------------------------------------------------

def viewcust(request):
	if request.session.has_key('loginid'):
		data=Customer.objects.all()
		item=Items.objects.all()
		a=request.session['loginid']
		c=Customer.objects.all().filter(id=a)
		for m in c:
			namee=m.TrdName
		return render(request,'viewcustomer.html',{'data':data,'item':item,'a':namee})
	else:
		return HttpResponseRedirect('/login')

def addtrad(request):
	if request.session.has_key('loginid'):
		if request.method=="POST":
			trd=request.POST['trdname']
			gstid=request.POST['gstid']
			pin=request.POST['pin']
			place=request.POST['place']
			addr1=request.POST['addr1']
			addr2=request.POST['addr2']
			getvalue=Customer.objects.all().filter(Gstid=gstid)
			if not(getvalue):
				addtrad=Customer(TrdName=trd,Gstid=gstid,Pincode=pin,Place=place,Addr1=addr1,Addr2=addr2)
				addtrad.save()
				cust=Customer.objects.latest('id')			
			else:
				dat={'a':"Trader already registered"}
				return JsonResponse(dat)
			pname = request.POST.getlist('pname')
			qty = request.POST.getlist('qty')
			price = request.POST.getlist('price')
			pdesc = request.POST.getlist('pdesc')
			print("jLj",len(qty))
			print("qty",qty)
			print("name",pname)
			for i in range (1,len(pname)):
				ppname = pname[i]
				qtyy = qty[i]
				print("I=",i)
				print("qty",qtyy)
				print("sdda",ppname)
				pricee = price[i]
				pdescc=pdesc[i]
				idi=Items.objects.get(id=ppname)
				additm=itmcustomer(pid=idi,cid=cust,taxableAmount=pricee,Quantity=qtyy,ProducctDesc=pdescc)
				additm.save()
			dat={'a':"Saved"}
			return JsonResponse(dat)
		else:
			dat={'a':"Error"}
			return JsonResponse(dat)
	else:
		return HttpResponseRedirect('/login')

def editcust(request):
	if request.session.has_key('loginid'):
		if request.method=="GET":
			eid=request.GET['eid']
			data=Customer.objects.all().filter(id=eid)
			item=Items.objects.all()
			itm=itmcustomer.objects.all().filter(cid=eid)
			return render(request,'editcust.html',{'data':data,'item':item,'itm':itm})
	else:
		return HttpResponseRedirect('/login')
def editcustdata(request):
	if request.session.has_key('loginid'):
		if request.method=="POST":
			trd=request.POST['trdname']
			cid=request.POST['cid']
			gstid=request.POST['gstid']
			pin=request.POST['pin']
			place=request.POST['place']
			addr1=request.POST['addr1']
			addr2=request.POST['addr2']
			Customer.objects.all().filter(id=cid).update(TrdName=trd,Gstid=gstid,Pincode=pin,Place=place,Addr1=addr1,Addr2=addr2)		
			pname = request.POST.getlist('pname')
			qty = request.POST.getlist('qty')
			price = request.POST.getlist('price')
			pdesc = request.POST.getlist('pdesc')
			print("jLj",len(qty))
			print("qty",qty)
			print("name",pname)
			for i in range (1,len(pname)):
				ppname = pname[i]
				qtyy = qty[i]
				print("I=",i)
				print("qty",qtyy)
				print("sdda",ppname)
				pricee = price[i]
				pdescc=pdesc[i]
				idi=Items.objects.get(id=ppname)
				cidd=Customer.objects.get(id=cid)
				additm=itmcustomer(pid=idi,cid=cidd,taxableAmount=pricee,Quantity=qtyy,ProducctDesc=pdescc)
				additm.save()
			return HttpResponseRedirect('/viewcust')
		else:
			data=Customer.objects.all()
			item=Items.objects.all()
			return render(request,'viewcustomer.html',{'data':data,'item':item,'error':"Update Unsuccessful"})
	else:
		return HttpResponseRedirect('/login')

def deldat(request):
	if request.session.has_key('loginid'):
		if request.method=="GET":
			print("jii")
			eid=request.GET['did']
			itmcustomer.objects.all().filter(id=eid).delete()
			return HttpResponse()
	else:
		return HttpResponseRedirect('/login')

def delcust(request):
	if request.session.has_key('loginid'):
		if request.method=="GET":
			delid=request.GET['delid']
			data=itmcustomer.objects.all().filter(cid=delid)
			spaa=[]
			for i in data:
				spaa.append(i.id)
				spaa=list(dict.fromkeys(spaa))
				print(spaa)
			Order.objects.all().filter(Q(cid=delid)|Q(iid__in=spaa)).delete()
			itmcustomer.objects.all().filter(cid=delid).delete()
			Customer.objects.all().filter(id=delid).delete()
			return HttpResponse()
	else:
		return HttpResponseRedirect('/login') 

# -----------------------------------------------Items---------------------------------------

def viewitems(request):
	if request.session.has_key('loginid'):
		data=Items.objects.all()
		a=request.session['loginid']
		c=Customer.objects.all().filter(id=a)
		for m in c:
			namee=m.TrdName
		return render(request,'viewitem.html',{'data':data,'a':namee})
	else:
		return HttpResponseRedirect('/login')
		

def additem(request):
	if request.session.has_key('loginid'):
		if request.method=="POST":
			pname=request.POST['pname']
			# pdesc=request.POST['pdesc']
			# qty=request.POST['qty']
			unit=request.POST['unit']
			# price=request.POST['price']
			# additems=Items(ProductName=pname,ProducctDesc=pdesc,taxableAmount=price,QtyUnit=unit,Quantity=qty)
			additems=Items(ProductName=pname,QtyUnit=unit)
			additems.save()
			dat={'a':"Saved",'b':pname,'e':unit}
			return JsonResponse(dat)
		else:
			dat={'a':"Error"}
			return JsonResponse(dat)
	else:
		return HttpResponseRedirect('/login')

def edititem(request):
	if request.session.has_key('loginid'):
		if request.method=="GET":
			eid=request.GET['eid']
			data=Items.objects.all().filter(id=eid)
			return render(request,'edititem.html',{'data':data})
	else:
		return HttpResponseRedirect('/login')

def edititemdata(request):
	if request.session.has_key('loginid'):
		if request.method=="POST":
			pname=request.POST['pname']
			unit=request.POST['unit']
			pid=request.POST['pid']
			additems=Items.objects.all().filter(id=pid).update(ProductName=pname,QtyUnit=unit)
			return HttpResponseRedirect('/viewitems')
		else:
			return HttpResponseRedirect('/viewitems')
	else:
		return HttpResponseRedirect('/login')

def delitemm(request):
	if request.session.has_key('loginid'):
		if request.method=="GET":
			delid=request.GET['delid']
			data=Items.objects.all().filter(id=delid).delete()
			return HttpResponse()
	else:
		return HttpResponseRedirect('/login') 

# ------------------------------------------------Orders---------------------------------------------

def vieworder(request):
	if request.session.has_key('loginid'):
		data=Order.objects.all()
		item=Items.objects.all()
		cust=Customer.objects.all()
		a=request.session['loginid']
		c=Customer.objects.all().filter(id=a)
		for m in c:
			namee=m.TrdName
		return render(request,'vieworder.html',{'data':data,'item':item,'cust':cust,'a':namee})
	else:
		return HttpResponseRedirect('/login')


def selectproduct(request):
	if request.session.has_key('loginid'):
		if request.method=="GET":
			pid=request.GET['pid']
			item=itmcustomer.objects.all().filter(pid=pid)
			spaa=[]
			for i in item:
				spaa.append(i.cid.id)
			print(spaa)
			spaa=list(dict.fromkeys(spaa))
			cust=Customer.objects.all().filter(id__in=spaa)
			custt=list(cust.values())
			print(custt)
			dat={'a':custt}
			return JsonResponse(dat)
	else:
		return HttpResponseRedirect('/login')

def getprice(request):
	if request.session.has_key('loginid'):
		if request.method=="GET":
			ftrd=request.GET['ftrd']
			pid=request.GET['pid']
			cust=itmcustomer.objects.all().filter(cid=ftrd,pid=pid)
			for i in cust:
				price=i.taxableAmount
				qty=i.Quantity
			dat={'a':qty,'b':price}
			return JsonResponse(dat)
	else:
		return HttpResponseRedirect('/login')

def addorder(request):
	if request.session.has_key('loginid'):
		if request.method=="POST":
			pname=request.POST['pname']
			ftrd=request.POST['ftrd']
			ttrd=request.POST['ttrd']
			qty=request.POST['qty']
			price=request.POST['price']
			oth=request.POST['oth']
			vehno=request.POST['vehno']
			vehtyp=request.POST['vehtyp']
			trd=Customer.objects.get(id=ttrd)
			totrd=Customer.objects.all().filter(id=ttrd)
			for j in totrd:
				tocust=j.TrdName
				print(tocust)
			itm=itmcustomer.objects.all().filter(pid=pname,cid=ftrd)
			for i in itm:
				iid=i.id
				ppname=i.pid.ProductName
				fftrd=i.cid.TrdName
			idi=itmcustomer.objects.get(id=iid)
			# additems=Items(ProductName=pname,ProducctDesc=pdesc,taxableAmount=price,QtyUnit=unit,Quantity=qty)
			additems=Order(cid=trd,iid=idi,taxableAmount=price,Quantity=qty,OtherValue=oth,VehicleNo=vehno,VehicleType=vehtyp)
			additems.save()
			dat={'b':ppname,'c':qty,'d':price,'e':fftrd,'f':tocust,'g':vehno}
			return JsonResponse(dat)
		else:
			dat={'a':"Error"}
			return JsonResponse(dat)
	else:
		return HttpResponseRedirect('/login')

def editorder(request):
	if request.session.has_key('loginid'):
		if request.method=="GET":
			eid=request.GET['eid']
			data=Order.objects.all().filter(id=eid)
			for i in data:
				pid=i.iid.pid.id
			data1=Items.objects.all()
			data2=Customer.objects.all()
			data3=itmcustomer.objects.all().filter(pid=pid)
			return render(request,'editorder.html',{'data':data,'data1':data1,'data2':data2,'data3':data3})
	else:
		return HttpResponseRedirect('/login')

def editorderdata(request):
	if request.session.has_key('loginid'):
		if request.method=="POST":
			ftrd=request.POST['ftrd']
			qty=request.POST['qty']
			price=request.POST['price']
			oth=request.POST['oth']
			vehno=request.POST['vehno']
			vehtyp=request.POST['vehtyp']
			oid=request.POST['oid']
			pid=request.POST['pid']
			det=itmcustomer.objects.all().filter(pid=pid,cid=ftrd)
			for i in det:
				idi=i.id
			newiid=itmcustomer.objects.get(id=idi)
			editdet=Order.objects.all().filter(id=oid).update(iid=newiid,taxableAmount=price,Quantity=qty,OtherValue=oth,VehicleNo=vehno,VehicleType=vehtyp)
			return HttpResponseRedirect('/vieworder')
		else:
			return HttpResponseRedirect('/vieworder')
	else:
		return HttpResponseRedirect('/login')

def delorder(request):
	if request.session.has_key('loginid'):
		if request.method=="GET":
			delid=request.GET['delid']
			data=Order.objects.all().filter(id=delid).delete()
			return HttpResponse()
	else:
		return HttpResponseRedirect('/login') 

def downloadfile(request):
	if request.session.has_key('loginid'):
		if request.method=="GET":
			did=request.GET['eid']
			data=Order.objects.all().filter(id=did)
			for i in data:
				fromGstin=["fromGstin",i.iid.cid.Gstid]
				fromTrdName=["fromTrdName",i.iid.cid.TrdName]
				fromAddr1=["fromAddr1",i.iid.cid.Addr1]
				fromAddr2=["fromAddr2",i.iid.cid.Addr2]
				fromPlace=["fromPlace",i.iid.cid.Place]
				fromPincode=["fromPincode",i.iid.cid.Pincode]
				toGstin=["toGstin",i.cid.Gstid]
				toTrdName=["toTrdName",i.cid.TrdName]
				toAddr1=["toAddr1",i.cid.Addr1]
				toAddr2=["toAddr2",i.cid.Addr2]
				toPlace=["toPlace",i.cid.Place]
				toPincode=["toPincode",i.cid.Pincode]
				otherValue=["otherValue",i.OtherValue]
				vehicleNo=["vehicleNo",i.VehicleNo]
				vehicleType=["vehicleType",i.VehicleType]
			ll=[fromGstin,fromTrdName,fromAddr1,fromAddr2,fromPlace,fromPincode,toGstin,toTrdName,toAddr1,toAddr2,toPlace,toPincode,otherValue,vehicleNo,vehicleType]
			lenth=(len(ll))
			with open("order.json", "w") as f:
				for j in range(lenth):
					json.dump(ll[j],f)
				# json.dump(fromTrdName,f)
			f.close()	
			custt=list(data.values())
			print(custt)
			dat={'a':custt}
			return JsonResponse(dat,content_type="application/json")
	else:
		return HttpResponseRedirect('/login') 

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def logoutfun(request):
	if request.session.has_key('loginid'):
		del  request.session['loginid']
	logout(request)
	return HttpResponseRedirect('/')