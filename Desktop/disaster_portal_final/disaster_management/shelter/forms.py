# shelter/forms.py
from django import forms
from .models import Shelter

class ShelterSearchForm(forms.Form):
    state_name = forms.ChoiceField(choices=[], required=False)
    district_name = forms.ChoiceField(choices=[], required=False)
    taluka_name = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(ShelterSearchForm, self).__init__(*args, **kwargs)
        self.fields['state_name'].choices = self.get_state_choices()
        self.fields['district_name'].choices = self.get_district_choices()
        self.fields['taluka_name'].choices = self.get_taluka_choices()

    def get_state_choices(self):
        states = Shelter.objects.values_list('state_name', flat=True).distinct()
        return [(state, state) for state in states]

    def get_district_choices(self):
        districts = Shelter.objects.values_list('district_name', flat=True).distinct()
        return [(district, district) for district in districts]

    def get_taluka_choices(self):
        talukas = Shelter.objects.values_list('taluka_name', flat=True).distinct()
        return [(taluka, taluka) for taluka in talukas]
