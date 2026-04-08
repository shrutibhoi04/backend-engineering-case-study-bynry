from flask import jsonify
from datetime import datetime, timedelta
from sqlalchemy.sql import func

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):

    try:
        alerts = []
        recent_days = 30
        recent_date = datetime.utcnow() - timedelta(days=recent_days)

        products = Product.query.filter_by(company_id=company_id).all()

        for product in products:

            inventories = Inventory.query.filter_by(product_id=product.id).all()

            for inv in inventories:

                total_sales = db.session.query(func.sum(Sales.quantity_sold))\
                    .filter(
                        Sales.product_id == product.id,
                        Sales.warehouse_id == inv.warehouse_id,
                        Sales.sale_date >= recent_date
                    ).scalar() or 0

                if total_sales == 0:
                    continue

                avg_daily_sales = total_sales / recent_days

                if avg_daily_sales == 0:
                    continue

                threshold = product.low_stock_threshold or 10

                if inv.quantity < threshold:

                    days_until_stockout = int(inv.quantity / avg_daily_sales)

                    warehouse = Warehouse.query.get(inv.warehouse_id)

                    supplier = db.session.query(Supplier)\
                        .join(Product_Suppliers, Supplier.id == Product_Suppliers.supplier_id)\
                        .filter(Product_Suppliers.product_id == product.id)\
                        .first()

                    alerts.append({
                        "product_id": product.id,
                        "product_name": product.name,
                        "sku": product.sku,
                        "warehouse_id": warehouse.id if warehouse else None,
                        "warehouse_name": warehouse.name if warehouse else None,
                        "current_stock": inv.quantity,
                        "threshold": threshold,
                        "days_until_stockout": days_until_stockout,
                        "supplier": {
                            "id": supplier.id if supplier else None,
                            "name": supplier.name if supplier else None,
                            "contact_email": supplier.contact_email if supplier else None
                        }
                    })

        return jsonify({
            "alerts": alerts,
            "total_alerts": len(alerts)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
