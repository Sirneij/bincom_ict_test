from django import forms
from django.db.models import fields

from . import models

LGA_CHOICE = []
lGAS = models.Lga.objects.all()
for lga in lGAS:
    lga_list = (lga.uniqueid, lga.lga_name)
    LGA_CHOICE.append(lga_list)

PARTY_CHOICE = []
PARTIES = models.Party.objects.all()
for p in PARTIES:
    party_list = (p.partyid, p.partyname)
    PARTY_CHOICE.append(party_list)


class LGASearchForm(forms.Form):
    lga_name = forms.ChoiceField(choices=LGA_CHOICE)

    def __init__(self, *args, **kwargs):
        super(LGASearchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-select"


class PollingUnitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PollingUnitForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = models.PollingUnit
        exclude = ['uniqueid', 'date_entered', 'user_ip_address']


class AnnouncedPuResultsForm(forms.Form):
    party = forms.ChoiceField(
        choices=PARTY_CHOICE, widget=forms.Select(attrs={"class": "form-select"}))
    party_score = forms.ChoiceField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
