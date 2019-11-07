#!/usr/bin/python
import re

def inialise_catalogue():

#Initialising catalogue dicionary, key:item name, value: price.
#e.g.
#Baked Beans => 0.99
#Biscuits => 1.20

    catalogue_dict = {}
    with open('catalogue') as f:
    
        for line in f:
             
            item, price = line.strip().split('\t')
            catalogue_dict[item] = float(price)

    return catalogue_dict



def initialise_offers():

#Initialising offer dictionaries, 2 separately for percentage offer and buy 2 get 1 free offer. 
#e.g. percentage offer
#Sardines => 25
#e.g. buy 2 get 1 free offer, each item's condition into a list
#Baked Beans => [2,1]

    offer_percentage_dict = {}
    offer_get_free_dict = {}
    with open('offers') as f:

        for line in f: 

            if '\t' in line:
                item, offer = line.strip().split('\t')
                percentages = re.match(r"([0-9]+)%", offer)
                buy_free = re.match(r"buy (\d) get (\d) free", offer)
    
                if percentages: 
    
                    percent = int(percentages.group(1))
                    offer_percentage_dict[item] = percent
    
                elif buy_free:
    
                    buy_free = re.findall(r'\d+' , offer) 
                    offer_get_free_dict[item] = buy_free 
    
                else: #Give error messages for unvalid line
    
                    print "WARNING: Unvalid offer syntax: " + line

    return offer_percentage_dict, offer_get_free_dict



def apply_percentage_offers(item,price):

    if item in offer_percentage_dict:

        percentage = offer_percentage_dict[item]
        discounting = price*(float(percentage)/100)
        print " -- " + item + " discounting " + str(percentage) + " % = " + str(discounting)
        return discounting

    else:

        return 0 #the item not in the offer, no discount



def apply_get_free_offers(item,num):

    if item in offer_get_free_dict:

        buy = int(offer_get_free_dict[item][0])
        free = int(offer_get_free_dict[item][1])
        remove_base = num/(buy+free)
        removing = remove_base*free

        if removing > 0:

            print " -- Got free " + str(removing) + " " + item

        return removing 

    else:

        return 0 #the item not in the offer, no discount



def calculate_total_pay(total_payment):

    total = 0
    sub_total = 0
    total_discount = 0

    with open('basket') as f:
    
        for line in f:

            if '\t' in line:
                item, num_raw = line.strip().split('\t')
                
                if item in catalogue_dict:

                    num = int(num_raw)
                    each_price = catalogue_dict[item]
                    sub_total = sub_total + each_price * num #Before discount

                    #Calculating discounts in 2 ways
                    discounting = apply_percentage_offers(item,each_price)
                    free_num = apply_get_free_offers(item,num)
                    paying_num = num - int(free_num)
                    total_discount = total_discount + discounting * paying_num #For percentage offer
                    total_discount = total_discount + each_price * free_num # For buy 2 get 1 free offer

                    #Sum discounted price
                    sum_price = paying_num*(each_price - discounting) 
                    total = total + sum_price

                    print "%s ( %.2f - %.2f ) * ( %d - %d ) = %.2f" % (item, each_price, discounting, num, free_num, sum_price) 
                else:
                    print "WARNING: Item '" + item + "' is not on the catalogue"

    return sub_total, total_discount, total


#Initialising dictionaries
catalogue_dict = inialise_catalogue()
offer_percentage_dict, offer_get_free_dict = initialise_offers()

#Calculation
sub_total, total_discount, total_payment = calculate_total_pay(catalogue_dict)

#Printing result
print "\nBefore discount: %.2f" % (sub_total)
print "Discounted: %.2f" % (total_discount)
print "Total to pay: %.2f" % (total_payment)

