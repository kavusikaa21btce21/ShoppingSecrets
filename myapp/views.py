from django.shortcuts import render ,redirect
from .models import User,Product,Wishlist,Cart,Transaction

# Create your views here.
def index(request):
	return render(request,'index.html')

def shop(request):
	products=Product.objects.all()	
	return render(request,'product.html',{'products':products})

def contact(request):
	return render(request,'contact.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
		  	if request.POST['password']==request.POST['cpassword']:
		  		User.objects.create(
					    usertype=request.POST['usertype'],
			       		fname=request.POST['fname'],
			       		lname=request.POST['lname'],
			       		email=request.POST['email'],
			       		mobile=request.POST['mobile'],
			       		address=request.POST['address'],
			       		password=request.POST['password']
			        )
		  		msg="User Sign up Successfully"
		  		return render(request,'login.html',{'msg':msg})
		  	else:
		  		msg="Password & Confirm password Does not Matched"
		  		return render(request,'signup.html'),{'msg':msg}
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			print("1")
			user=User.objects.get(email=request.POST['email'],password=request.POST['password'])
			if user.usertype=="user":
				print("2")
				request.session['email']=user.email
				request.session['fname']=user.fname
				wishlists=Wishlist.objects.filter(user=user)
				request.session['wishlist_count']=len(wishlists)
				carts=Cart.objects.filter(user=user)
				request.session['cart_count']=len(carts)
				return render(request,'index.html')
			else:
				print("3")
				request.session['email']=user.email
				request.session['fname']=user.fname
				return render(request,'seller_index.html')
		except:
			msg="Email or Password is incorrect"
			return render(request,'login.html'),{'msg':msg}
	else:
		return render(request,'login.html')		

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return render(request,'login.html')	
	except:
		return render(request,'login.html')	

def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New Password and Confirm New Password Does Not Matched"
				return render (request,'change_password.html',{'msg':msg})
		else:
			msg="Old Password Does Not Matched"
			return render (request,'change_password.html',{'msg':msg})
	else:
		return render (request,'change_password.html')

def seller_change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New Password and Confirm New Password Does Not Matched"
				return render (request,'seller_change_password.html',{'msg':msg})
		else:
			msg="Old Password Does Not Matched"
			return render (request,'seller_change_password.html',{'msg':msg})
	else:
		return render (request,'seller_change_password.html')
		

def seller_add_product(request):
    seller=User.objects.get(email=request.session['email'])
    if request.method=='POST':
    	Product.objects.create(
    		    seller=seller,
    		    product_category=request.POST['product_category'],
    		    product_name=request.POST['product_name'],
    		    product_price=request.POST['product_price'],
    		    product_desc=request.POST['product_desc'],
    		    product_image=request.FILES['product_image']

    		)
    	msg="Product Added Successfully"
    	return render(request,'seller_add_product.html',{'msg':msg})
    else:
    	return render(request,'seller_add_product.html')

def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller_view_product.html',{'products':products})


def seller_product_detail(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller_product_detail.html',{'product':product})

def product_details(request,pk):
	wishlist_flag=False
	cart_flag=False
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	try:
		Wishlist.objects.get(user=user,product=product)
		wishlist_flag=True
	except:
		pass
	try:
		Cart.objects.get(user=user,product=product)
		cart_flag=True
	except:
		pass
	return render(request,'product_details.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

def seller_edit_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_desc=request.POST['product_desc']
		product.product_category=request.POST['product_category']
		try:
			product.product_image=request.FILES['product_image']
		except:
			pass

		product.save()
		msg="Product Updated Successfully"
		return render(request,'seller_edit_product.html',{'product':product,'msg':msg})
	else:
		return render(request,'seller_edit_product.html',{'product':product})

def seller_delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller_view_product')

def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request,'wishlist.html',{'wishlists':wishlists})

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(user=user,product=product)
	return redirect('wishlist')

def remove_from_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')

def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user)
	for i in carts:
		net_price=net_price+i.total_price
	request.session['cart_count']=len(carts)
	return render(request,'cart.html',{'carts':carts,'net_price':net_price})

def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(user=user,product=product,product_qty=1,product_price=product.product_price,total_price=product.product_price)
	return redirect('cart')

def remove_from_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(user=user,product=product)
	cart.delete()
	return redirect('cart')

def change_qty(request):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(pk=int(request.POST['cid']))
	cart.product_qty=int(request.POST['product_qty'])
	cart.total_price=int(request.POST['product_qty'])*cart.product_price
	cart.save()
	return redirect('cart')









