
import os
import pandas as pd

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from .models import Product

REQUIRED_COLUMNS = {'sku', 'name', 'price'}  



def home(request):
    return render(request, 'products/home.html')
def _read_file(file_path):
    lower = file_path.lower()
    if lower.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif lower.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")
    return df

def _validate_columns(df):
    cols = {c.strip().lower() for c in df.columns}
    missing = REQUIRED_COLUMNS - cols
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            try:
                
                ext = uploaded_file.name.lower().split('.')[-1]
                if ext not in ['csv', 'xls', 'xlsx']:
                    messages.error(request, "File format should be CSV or Excel type.")
                    fs.delete(filename)
                    return render(request, 'products/upload.html', {'form': form})

                df = _read_file(file_path)
                df.columns = [c.strip().lower() for c in df.columns]
                _validate_columns(df)

                created = 0
                updated = 0
                skipped = 0

                for _, row in df.iterrows():
                    sku = str(row.get('sku', '')).strip()
                    name = str(row.get('name', '')).strip()
                    if not sku or not name:
                        skipped += 1
                        continue
                    try:
                        price = float(row.get('price', 0)) if not pd.isna(row.get('price')) else 0.0
                    except Exception:
                        price = 0.0
                    try:
                        quantity = int(row.get('quantity', 0)) if not pd.isna(row.get('quantity')) else 0
                    except Exception:
                        quantity = 0

                    defaults = {
                        'name': name,
                        'description': str(row.get('description', '') or ''),
                        'category': str(row.get('category', '') or ''),
                        'price': price,
                        'quantity': quantity,
                    }

                    obj, created_flag = Product.objects.update_or_create(sku=sku, defaults=defaults)
                    if created_flag:
                        created += 1
                    else:
                        updated += 1

                messages.success(request, f'Import finished: created={created}, updated={updated}, skipped={skipped}')
                try:
                    fs.delete(filename)
                except Exception:
                    pass
                return redirect('products:upload_success')
            except Exception as e:
                messages.error(request, f'Error processing file: {e}')
                try:
                    fs.delete(filename)
                except Exception:
                    pass
                return render(request, 'products/upload.html', {'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'products/upload.html', {'form': form})

def upload_success(request):
    return render(request, 'products/sucess.html')
