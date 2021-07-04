from django.urls import path
from testapp import views


urlpatterns=[
			path('',views.first),
			path('newacc/',views.newacc),
			path('login/',views.login),
			path('register/',views.register),
			path('viewcust/',views.viewcust),
			path('addtrad/',views.addtrad),
			path('viewitems/',views.viewitems),
			path('vieworder/',views.vieworder),
			path('additem/',views.additem),
			path('delitemm/',views.delitemm),
			path('selectproduct/',views.selectproduct),
			path('getprice/',views.getprice),
			path('addorder/',views.addorder),
			path('index/',views.index),
			path('edititem/',views.edititem),
			path('edititemdata/',views.edititemdata),
			path('delorder/',views.delorder),
			path('editorder/',views.editorder),
			path('editorderdata/',views.editorderdata),
			path('downloadfile/',views.downloadfile),
			path('delcust/',views.delcust),
			path('deldat/',views.deldat),
			path('editcust/',views.editcust),
			path('editcustdata/',views.editcustdata),
			path('logoutfun/',views.logoutfun),
			]