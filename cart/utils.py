import datetime
import simplejson as json


def generate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #20220616233810 + pk
    order_number = current_datetime + str(pk)
    return order_number


def order_total_by_seller(order, sellerProfile_id):
    total_data = json.loads(order.total_data)
    data = total_data.get(str(sellerProfile_id))
    subtotal = 0

    for key, val in data.items():
        subtotal += float(key)
        val = val.replace("'", '"')
        val = json.loads(val)

    grand_total = float(subtotal) 
    context = {
        'subtotal': subtotal,
        'grand_total': grand_total,
    }

    return context