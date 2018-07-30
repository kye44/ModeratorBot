from paypalrestsdk import paypal

def NewPayment():
	# Create payment object
	payment = Payment({
	  "intent": "sale",

	  # Set payment method
	  "payer": {
	    "payment_method": "paypal"
	  },

	  # Set redirect urls
	  "redirect_urls": {
	    "return_url": "http://localhost:3000/process",
	    "cancel_url": "http://localhost:3000/cancel"
	  },

	  # Set transaction object
	  "transactions": [{
	    "amount": {
	      "total": "10.00",
	      "currency": "USD"
	    },
	    "description": "payment description"
	  }]
	})