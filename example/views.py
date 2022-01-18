from xml.dom import ValidationErr
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date


# Create your views here

@api_view(['POST'])
def calculateDeliveryFee(request):
	points={"cart_value":"int","delivery_distance":"int","number_of_items":"int","time":"time"}
	for key in points:
		temp = validator(request,key,points[key])
		if (type(temp) != type(None)):
			return temp
	cartval = int(request.POST.get("cart_value"))
	distance = int(request.POST.get("delivery_distance"))
	items = int(request.POST.get("number_of_items"))
	time = request.POST.get("time")
    
	return Response({
		'delivery_fee': main(cartval, distance, items, time) 
	})
def validator(request,field, datatype):
	data=request.POST.get(field)
	if (datatype == "int"):
		try:
			data=int(data)
			if (data<0):
				raise ValidationError(_('Invalid value'), code='invalid')
		except:
			print("error")
			return Response({
				'error': ("Send valid "+field+" value")  
				}, status=status.HTTP_400_BAD_REQUEST)
	


def fridayRush(t):
	#a mathematical algorithm to calculate the weekday of a date by Arthur Benjamin
	a=t.split("T")
	date=a[0]
	t=a[1][:-1]

	datecodes=(0,3,3,6,1,4,6,2,5,0,3,5) #date codes corresponds to each month of a year
	date=date.split("-")
	digits=int(date[0][4 - 2:])-1
	calc=(int(date[2])+datecodes[int(date[1])-1]+digits + digits//4)
	if (((int(date[0]) % 4) == 0) and int(date[1])>2):
		calc+=1
	calc %= 7

	#calc   monday,tuesday,wednesday,thursday,friday,saturday,sunday -> 1,2,3,4,5,6,0 respectively

	if (calc==5): #if it is friday
		t=t.split(":")
		for i in range(len(t)):
			t[i]=int(t[i])
		if (t[0]>=15 and t[0]<19 or (t[0]==19 and t[1]==0 and t[2]==0)):
			return True # It is friday rush
	return False


def delivery_fee_calculator(distance):
	delivery = 200
	if (distance > 1000):
		distance -= 1000
		temp = distance//500
		distance = distance%500
		delivery += (temp*100)
		if (distance != 0):
			delivery += 100
	return delivery

def items_surcharge(items):
	if (items > 4):
		items-=4
		return items*50
	return 0

def main(cartval, distance, items, time):
	surcharge = 0

	if (cartval >= 10000):
		print("delivery fee 0")
		return 0 #!!!!!!!!!!!!!!!!!!

	if (cartval < 1000):
		valSurcharge = 1000-cartval
	
	delivery = delivery_fee_calculator(distance)

	itemSurcharge = items_surcharge(items)

	fees = valSurcharge + delivery + itemSurcharge
	if fridayRush(time):
		fees *= 1.1
		print("it is friday rush")

	if (fees > 1500):
		fees = 1500
	print("The delivery fee is {:4.2f} euros.".format(fees/100))
	return fees


	

