from django import forms
import connect
from connect import Database

class CarAddForm(forms.Form):
    db = Database()
    producer = forms.CharField()
    model = forms.CharField()
    car_class = forms.CharField()
    drive = forms.CharField()
    engine = forms.ChoiceField(choices=db.engine_choices())
    interior = forms.ChoiceField(choices=db.interior_choices())
    body = forms.ChoiceField(choices=db.body_choices())
    cost = forms.IntegerField()
