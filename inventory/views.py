from django.shortcuts import get_object_or_404, render, redirect
from .models import Inventory
from django.contrib.auth.decorators import login_required
from .forms import AddInventoryForm, UpdateInventoryForm
from django.contrib import messages
from django_pandas.io import read_frame
import plotly
import plotly.express as px
import json

@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    context={
        "title":"Inventory List",
        "inventories": inventories
    }
    return render(request, "inventory/inventory_list.html", context=context)

@login_required
def per_product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': inventory
    }

    return render(request, "inventory/per_product.html", context=context)

@login_required
def add_product(request):
    if request.method == "POST":
        add_form = AddInventoryForm(request.POST)  

        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            new_inventory.sales = float(add_form.cleaned_data['cost_per_item']) * float(add_form.cleaned_data['quantity_sold'])
            new_inventory.save()
            messages.success(request, "Product Added Successfully")
            return redirect("/inventory")
    else:
        add_form = AddInventoryForm()  

    return render(request, "inventory/inventory_add.html", {"form": add_form})

@login_required
def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.success(request, "Inventory Deleted Successfully")
    return redirect("/inventory") 

@login_required
def update_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)

    if request.method == "POST":
        updateForm = UpdateInventoryForm(request.POST, instance=inventory)

        if updateForm.is_valid():
            updated_inventory = updateForm.save(commit=False)
            updated_inventory.sales = float(updated_inventory.cost_per_item) * float(updated_inventory.quantity_sold)
            updated_inventory.save()
            messages.success(request, "Product Updated Successfully")
            return redirect(f"/inventory/per_product/{pk}")
    else:
        updateForm = UpdateInventoryForm(instance=inventory)

    return render(request, "inventory/inventory_update.html", {"form": updateForm})

@login_required
def dashboard(request):
    Inventories = Inventory.objects.all()

    df = read_frame(Inventories)

    sales_graph = df.groupby(by="last_sales", as_index=False, sort=False)['sales'].sum()
    sales_graph = px.line(sales_graph, x = sales_graph.last_sales, y = sales_graph.sales, title="Sale Trend")
    sales_graph = json.dumps(sales_graph, cls=plotly.utils.PlotlyJSONEncoder)

    best_performance_product_df = df.groupby(by="name").sum().sort_values(by="quantity_sold")
    best_performance_product = px.bar(best_performance_product_df,
                                         x = best_performance_product_df.index,
                                         y = best_performance_product_df.quantity_sold,
                                         title="Best Performance Product")
    
    best_performance_product = json.dumps(best_performance_product, cls=plotly.utils.PlotlyJSONEncoder)

    most_product_in_stock_df = df.groupby(by="name").sum().sort_values(by="quantity_in_stock")
    most_product_in_stock = px.pie(most_product_in_stock_df,
                                   names = most_product_in_stock_df.index,
                                   values = most_product_in_stock_df.quantity_in_stock,
                                   title = "Most Product In Stock")

    most_product_in_stock = json.dumps(most_product_in_stock, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        "sales_graph": sales_graph,
        "best_performance_product":best_performance_product,
        "most_product_in_stock":most_product_in_stock
    }

    return render(request, "inventory/dashboard.html", context=context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')