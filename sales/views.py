from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Sale
from .forms import SaleForm


# This is so the user can only see their own sales listings
@login_required
def sales_list(request):
    """
    List all sales for the logged-in user
    """
    sales = Sale.objects.filter(user=request.user)  # Filter by the logged-in user
    return render(request, "sales/sales_list.html", {"sales": sales})


# View details of a single sale
def sale_detail(request, sale_id):
    """
    View details of a single sale listing
    """
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, "sales/sale_detail.html", {"sale": sale})


# Create a new sale
@login_required
def sale_create(request):
    """
    Create a new sale listing and save it to the database
    """
    if request.method == "POST":
        form = SaleForm(request.POST, request.FILES)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            sale.save()
            return redirect("sales_list")
    else:
        form = SaleForm()
    return render(request, "sales/sale_form.html", {"form": form})


# Update an existing sale
@login_required
def sale_update(request, sale_id):
    """
    Update an existing sale listing ie. change the details of a sale
    """
    sale = get_object_or_404(Sale, id=sale_id, user=request.user)
    if request.method == "POST":
        form = SaleForm(request.POST, request.FILES, instance=sale)
        if form.is_valid():
            form.save()
            return redirect("sales_list")
    else:
        form = SaleForm(instance=sale)
    return render(request, "sales/sale_form.html", {"form": form})


# Delete a sale
@login_required
def sale_delete(request, sale_id):
    """
    Delete a sale listing from the database and redirect to the sales list of the user
    """
    sale = get_object_or_404(Sale, id=sale_id, user=request.user)
    if request.method == "POST":
        sale.delete()
        return redirect("sales_list")
    return render(request, "sales/sale_confirm_delete.html", {"sale": sale})
