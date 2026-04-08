
---

#`part2_database_design.md`

```md
# Part 2: Database Design

## Tables

### Companies
- id (PK)
- name
- created_at

### Warehouses
- id (PK)
- company_id (FK)
- name
- location

### Products
- id (PK)
- company_id (FK)
- name
- sku (UNIQUE)
- price
- product_type

### Inventory
- id (PK)
- product_id (FK)
- warehouse_id (FK)
- quantity
- UNIQUE(product_id, warehouse_id)

### Inventory History
- id (PK)
- product_id
- warehouse_id
- change_type
- quantity_changed
- created_at

### Suppliers
- id (PK)
- name
- contact_email

### Product_Suppliers
- product_id (FK)
- supplier_id (FK)

### Product Bundles
- bundle_product_id
- child_product_id
- quantity

### Sales
- id (PK)
- product_id
- warehouse_id
- quantity_sold
- sale_date

---

## Missing Requirements

- Multiple suppliers support?
- Threshold definition?
- Recent sales duration?
- Bundle behavior?
- Real-time vs batch updates?
- Warehouse transfers?
- Backorder support?
- Supplier scope?

---

## Design Decisions

- Separate Inventory → multi-warehouse support  
- Unique SKU → consistency  
- History table → tracking  
- Many-to-many suppliers → flexibility  
- Bundles → composite products  

---

## Scalability

- Normalized schema  
- Multi-tenant support  
- Efficient queries  
