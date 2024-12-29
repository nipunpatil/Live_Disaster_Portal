# shelter/views.py
from django.shortcuts import render
from .models import Shelter
from .forms import ShelterSearchForm
# shelter/views.py
from django.shortcuts import render, get_object_or_404
from .models import Shelter
from .forms import ShelterSearchForm

# shelter/views.py
from django.shortcuts import render, get_object_or_404
from .models import Shelter
from .forms import ShelterSearchForm

def shelter_detail(request, shelter_id):
    shelter = get_object_or_404(Shelter, sr_no=shelter_id)
    return render(request, 'shelter/shelter_detail.html', {'shelter': shelter})

def shelter_search(request):
    form = ShelterSearchForm()
    shelters = []

    if request.method == 'GET':
        form = ShelterSearchForm(request.GET)
        if form.is_valid():
            state_name = form.cleaned_data.get('state_name')
            district_name = form.cleaned_data.get('district_name')
            taluka_name = form.cleaned_data.get('taluka_name')

            # Filter shelters based on the search criteria
            filters = {}
            if state_name:
                filters['state_name'] = state_name
            if district_name:
                filters['district_name'] = district_name
            if taluka_name:
                filters['taluka_name'] = taluka_name
            
            shelters = Shelter.objects.filter(**filters)

    return render(request, 'shelter/shelter_search.html', {'form': form, 'shelters': shelters})
