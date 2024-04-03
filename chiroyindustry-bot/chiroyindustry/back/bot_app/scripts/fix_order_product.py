# fix_orderproduct.py
from bot_app.models import Order, OrderProduct


def run():
    # Step 1: Identify the problematic row
    # Replace '146' with the actual primary key value causing the issue
    problematic_row_pk = '146'

    # Step 2: Verify the existence of the referenced order
    order_id_to_update = '62220'  # Replace with the noted order_id value

    try:
        order = Order.objects.get(pk=order_id_to_update)
    except Order.DoesNotExist:
        # If the order does not exist, you may want to handle this case
        print(f"Order with id {order_id_to_update} does not exist.")
        return

    # Step 3: Update 'order_id' in the problematic row
    # Replace '146' with the actual primary key value causing the issue
    # Replace 'correct_order_id' with the correct order ID
    correct_order_id = order.id  # Assuming you want to use the ID of the existing order

    try:
        order_product = OrderProduct.objects.get(pk=problematic_row_pk)
        order_product.order_id = correct_order_id
        order_product.save()
        print(f"Successfully updated 'order_id' for OrderProduct with pk {problematic_row_pk}")
    except OrderProduct.DoesNotExist:
        print(f"OrderProduct with pk {problematic_row_pk} does not exist.")
        print("Fixing order product...")

if __name__ == "__main__":
    run()
