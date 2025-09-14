from django import forms

class ProductUploadForm(forms.Form):
    file = forms.FileField(help_text="Upload CSV or Excel (.xlsx) file")
    