import click
from models import Category, Supplier, Product
from database import get_db, get_categories, get_suppliers, get_products, add_product

@click.group()
def cli():
    pass

@cli.command()
@click.option("--category_id", type=int, help="Filter by category ID")
@click.option("--supplier_id", type=int, help="Filter by supplier ID")
def generate_report(category_id, supplier_id):
    with get_db() as db:
        categories = get_categories(db)
        suppliers = get_suppliers(db)
        products = get_products(db)

        click.echo("Categories:")
        for category in categories:
            click.echo(f"{category.id}. {category.name}")

        click.echo("\nSuppliers:")
        for supplier in suppliers:
            click.echo(f"{supplier.id}. {supplier.name}")

        click.echo("\nProducts:")
        filtered_products = products
        if category_id is not None:
            filtered_products = [p for p in filtered_products if p.category_id == category_id]
        if supplier_id is not None:
            filtered_products = [p for p in filtered_products if p.supplier_id == supplier_id]

        for product in filtered_products:
            click.echo(f"{product.id}. {product.name}, Stock: {product.quantity_in_stock}, Price: {product.unit_price}")

@cli.command()
def update_stock():
    with get_db() as db:
        products = get_products(db)

        # Logic to update stock levels
        # ask the user for a product ID and update its stock
        product_id = click.prompt("Enter the product ID to update stock", type=int)
        selected_product = next((product for product in products if product.id == product_id), None)

        if selected_product:
            new_stock = click.prompt("Enter the new stock level", type=int)
            selected_product.quantity_in_stock = new_stock
            db.commit()
            click.echo(f"Stock level for {selected_product.name} updated to {new_stock}")
        else:
            click.echo(f"Product with ID {product_id} not found.")

@cli.command()
def add_product():
    with get_db() as db:
        categories = get_categories(db)
        suppliers = get_suppliers(db)

        # ask the user for product details and add to the database
        click.echo("Add a new product:")
        name = click.prompt("Product Name")
        color = click.prompt("Color")
        size = click.prompt("Size")
        quantity = click.prompt("Quantity in Stock", type=int)
        price = click.prompt("Unit Price", type=float)

        # Display available categories for the user to choose
        click.echo("\nAvailable Categories:")
        for category in categories:
            click.echo(f"{category.id}. {category.name}")
        category_id = click.prompt("Select a Category (Enter the Category ID)", type=int)

        # Display available suppliers for the user to choose
        click.echo("\nAvailable Suppliers:")
        for supplier in suppliers:
            click.echo(f"{supplier.id}. {supplier.name}")
        supplier_id = click.prompt("Select a Supplier (Enter the Supplier ID)", type=int)

        new_product = add_product(db, name, color, size, quantity, price, category_id, supplier_id)
        click.echo(f"New product added: {new_product.name}")

@cli.command()
def optimize_inventory():
    with get_db() as db:
        products = get_products(db)

        #  Sort products by quantity_in_stock
        sorted_products = sorted(products, key=lambda x: x.quantity_in_stock, reverse=True)

        click.echo("Optimized Inventory:")
        for product in sorted_products:
            click.echo(f"{product.name}, Stock: {product.quantity_in_stock}, Price: {product.unit_price}")

if __name__ == '__main__':
    cli()
