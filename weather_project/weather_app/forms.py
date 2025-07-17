from django import forms

class MyForm(forms.Form):
    my_text_area = forms.CharField(widget=forms.Textarea)