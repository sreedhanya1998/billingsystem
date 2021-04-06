from django.shortcuts import render,redirect
from .forms import BillPurchaseForm,OrderCreateForm,OrderlineForm,Dateform
from django.views.generic import TemplateView
from django.db.models import Sum
from .models import Purchase,Order,OrderLines,Item
from .forms import Registrationform,Loginform
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
# Create your views here.
class create_bill(TemplateView):
    form_class=BillPurchaseForm
    template_name="billing/billcreate.html"
    context={}
    def get(self,request,*args,**kwargs):
        form=self.form_class
        self.context["form"]=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list")
        return render(request, self.template_name, self.context)
class purchase_list(TemplateView):
    model=Purchase
    template_name = "billing/purchaseitem.html"
    context={}
    def get(self,request,*args,**kwargs):
       item=self.model.objects.all()
       self.context["item"]=item
       return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
            return redirect("item")
class purchase_view(TemplateView):
    model=Purchase
    template_name = "billing/billview.html"
    context = {}
    def get(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        item=self.model.objects.get(id=id)
        self.context["item"]=item
        return render(request,self.template_name,self.context)
class purchase_edit(TemplateView):
    model=Purchase
    form_class=BillPurchaseForm
    template_name = "billing/billedit.html"
    context={}
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        item=self.model.objects.get(id=id)
        form=self.form_class(instance=item)
        self.context["item"]=item
        self.context["form"]=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        item=self.model.objects.get(id=id)
        form=self.form_class(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect("list")
class purchase_delete(TemplateView):
    model=Purchase
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        item=self.model.objects.get(id=id)
        item.delete()
        return redirect("list")
class Ordercreate(TemplateView):
    model=Order
    form_class=OrderCreateForm
    template_name = "billing/billorder.html"
    context={}
    def get(self,request,*args,**kwargs):
        order=self.model.objects.last()
        if order:
            last_billnumber=order.billnumber
            list=int(last_billnumber.split('-')[1])+1
            billnumber='klyn-'+str(list)
        else:
            billnumber="klyn-1000"
        form=self.form_class(initial={"billnumber":billnumber})
        self.context["form"]=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            billnumber=form.cleaned_data.get("billnumber")
            form.save()
            return redirect("orderline",billnumber=billnumber)
class Orderline(TemplateView):
    model=OrderLines
    form_class=OrderlineForm
    template_name ="billing/orderlist.html"
    context={}
    def get(self,request,*args,**kwargs):
        billnum=kwargs.get("billnumber")
        print(billnum)
        form=self.form_class(initial={"bill_number":billnum})
        self.context["form"]=form
        self.context["items"] = self.model.objects.filter(bill_number__billnumber=billnum)
        total = OrderLines.objects.filter(bill_number__billnumber=billnum).aggregate(Sum('amount'))
        self.context["total"]=total["amount__sum"]
        self.context["billnum"]=billnum
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            bill_number=form.cleaned_data.get("bill_number")
            p_qty=form.cleaned_data.get("product_qty")
            product_name=form.cleaned_data.get("product_name")#rice
            order=Order.objects.get( billnumber=bill_number)
            product=Purchase.objects.get(item_name__item_name=product_name)
            prdt=Item.objects.get(item_name=product_name)
            amount = p_qty *product.selling_price
            print(amount)
            orderline=self.model(bill_number=order,product_qty=p_qty,product_name=prdt,amount=amount)
            orderline.save()
            return redirect("orderline",billnumber=order)
class Billgenerate(TemplateView):
    model=Order
    def get(self,request,*args,**kwargs):
        billnum=kwargs.get("billnumber")
        order=self.model.objects.get(billnumber=billnum)
        total = OrderLines.objects.filter(bill_number__billnumber=billnum).aggregate(Sum('amount'))
        total=total["amount__sum"]
        Order.bill_total=total
        order.save()
        print("bill saved")
        return redirect("order")
class Registration(TemplateView):
    model=User
    form_class=Registrationform
    template_name = "billing/registration.html"
    context={}
    def get(self,request,*args,**kwargs):
        form=self.form_class
        self.context["form"]=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"billing/login.html")
        else:
            form = self.form_class(request.POST)
            self.context["form"]=form
            return render(request, self.template_name, self.context)
class loginView(TemplateView):
    form_class=Loginform
    template_name = "billing/login.html"
    context={}
    def get(self,request,*args,**kwargs):
        form=self.form_class
        self.context["form"]=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(username=uname,password=pwd)
            if user is not None:
                login(request,user)
                return redirect("order")
            else:
                form = self.form_class(request.POST)
                self.context["form"]=form
                return render(request,self.template_name,self.context)
class Datewise(TemplateView):
    template_name = 'billing/home.html'
    context={}
    def get(self,request,*args,**kwargs):
        form=Dateform()
        date=form.cleaned_data.get("date")
        date_amount=Purchase.objects.filter(date=date)
        self.context["total"] = date_amount["amount__sum"]
        return render(request,self.template_name,self.context)
