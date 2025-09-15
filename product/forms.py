from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(help_text="Upload CSV or Excel (.xlsx) file")
    