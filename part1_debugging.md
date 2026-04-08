# Part 1: Code Review & Debugging

## Issues Identified

1. No Input Validation  
The code directly accesses request data without validation.

2. SKU Uniqueness Not Enforced  
Duplicate SKUs can be created.

3. Multiple Database Commits  
Leads to inconsistent data if one operation fails.

4. Incorrect Data Modeling  
Product tied to single warehouse.

5. No Error Handling  
API may crash on failure.

6. Price Not Validated  
Invalid values may be stored.

7. Initial Quantity Not Validated  
Negative or missing values possible.

8. No Optional Field Handling  
All fields assumed mandatory.

---

## Impact in Production

- Application crashes  
- Duplicate SKU issues  
- Partial data creation  
- Poor scalability  
- Bad user experience  
- Incorrect financial data  
- Wrong inventory tracking  

---

## Corrected Code


from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    if data['price'] < 0:
        return jsonify({"error": "Invalid price"}), 400

    if data['initial_quantity'] < 0:
        return jsonify({"error": "Invalid quantity"}), 400

    try:
        existing_product = Product.query.filter_by(sku=data['sku']).first()
        if existing_product:
            return jsonify({"error": "SKU exists"}), 400

        with db.session.begin():
            product = Product(
                name=data['name'],
                sku=data['sku'],
                price=data['price']
            )
            db.session.add(product)
            db.session.flush()

            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=data['initial_quantity']
            )
            db.session.add(inventory)

        return jsonify({"message": "Created", "product_id": product.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
