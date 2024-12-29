from .models import District

def get_district_choices(state_id):
    return [(district.id, district.name) for district in District.objects.filter(state_id=state_id)]
