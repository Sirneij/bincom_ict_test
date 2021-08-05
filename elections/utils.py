from . import models


def get_client_ip(request):
    X_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if X_forwarded_for:
        ip = X_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_polling_unit_info(number):
    print(models.PollingUnit.objects.get(uniqueid=15).polling_unit_number)
    poll = models.PollingUnit.objects.filter(uniqueid=number).values(
        "polling_unit_number", "polling_unit_name", "polling_unit_description", "lga_id", "polling_unit_id", "uniqueid")
    lgas = []
    states = []
    for p in poll:
        lga = models.Lga.objects.get(lga_id=p["lga_id"])
        state = models.States.objects.get(state_id=lga.state_id)
        lga_dict = {"lga_name": lga.lga_name}
        state_dict = {"state_name": state.state_name}
        lgas.append(lga_dict)
        states.append(state_dict)
    poll = list(poll)
    for i in range(len(poll)):
        poll[i]["lga_name"] = lgas[i]['lga_name']
        poll[i]['state_name'] = states[i]['state_name']

    return poll


def get_polling_unit_result(punit_number):
    result_poll = models.AnnouncedPuResults.objects.filter(
        polling_unit_uniqueid=punit_number).values("party_abbreviation", "party_score").order_by("party_abbreviation")

    return result_poll
