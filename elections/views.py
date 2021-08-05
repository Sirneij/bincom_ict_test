from django.contrib import messages
from django.db.models import Sum
from django.http.response import JsonResponse
from django.shortcuts import redirect, render

from . import forms, models, utils


def pulling_unit_result(request):
    if request.method == "POST":
        polling_unit_number = request.POST.get("unit_number")
        if polling_unit_number:
            poll_info = utils.get_polling_unit_info(polling_unit_number)
            polling_unit_result = utils.get_polling_unit_result(polling_unit_number)
            polling_unit_result = list(polling_unit_result)
            return JsonResponse({"success": True, "poll_info": poll_info, "polling_unit_result": polling_unit_result})
        else:
            return JsonResponse({"success": False, 'msg': "No result for your query"})
    else:
        poll = utils.get_polling_unit_info(15)
        result_poll = utils.get_polling_unit_result("15")
    context = {
        "page_title": "Polling Unit Result",
        "poll": poll,
        "result_poll": result_poll,
    }
    return render(request, 'elections/pulling_unit_result.html', context)


def lga_result(request):
    lga_form = forms.LGASearchForm(request.POST or None)
    if request.method == "POST":
        lga_id = request.POST.get("lga_name")
        print(lga_id)
        if lga_id:
            lga = models.Lga.objects.get(uniqueid=lga_id)
            # get all polling units in the lga with that id
            punits = models.PollingUnit.objects.filter(lga_id=lga.lga_id).values(
                "polling_unit_id", "polling_unit_number", "lga_id", "uniqueid")
            punit_ids = []
            # append all unique polling unit IDs
            for punit in list(punits):
                punit_ids.append(f'{punit["uniqueid"]}')
            print(punit_ids)
            lga_party_result = []
            for punit_id in punit_ids:
                result_poll_parties = models.AnnouncedPuResults.objects.filter(
                    polling_unit_uniqueid=punit_id).values("party_abbreviation").annotate(summed_party_result=Sum("party_score"))
                result_poll_parties = list(result_poll_parties)
                lga_party_result.append(result_poll_parties)

            print(lga_party_result)
            lga_result_dict = []
            for lgr in lga_party_result:
                for l in lgr:
                    lga_result_dict.append(l)
            return JsonResponse({"success": True, "results": lga_result_dict})
        else:
            return JsonResponse({"success": False, "msg": "Select a valid Local Governmentt"})
    context = {
        "page_title": "Local Government Result",
        "lga_form": lga_form,
    }
    return render(request, 'elections/lga_result.html', context)


def add_polling_unit_result(request):
    polling_unit_form = forms.PollingUnitForm(request.POST or None)
    announced_party_form = forms.AnnouncedPuResultsForm(request.POST or None)
    if request.method == "POST":
        action = request.POST.get("action")
        if polling_unit_form.is_valid():
            polling_unit = polling_unit_form.save(commit=False)
            polling_unit.user_ip_address = utils.get_client_ip(request)
            polling_unit.save()
            ar = models.AnnouncedPuResults.objects.create(
                polling_unit_uniqueid=polling_unit.polling_unit_id, party_abbreviation=request.POST.get("party"), party_score=request.POST.get("party_score"), entered_by_user=polling_unit.entered_by_user, user_ip_address=polling_unit.user_ip_address)
            ar.save()
            messages.success(request, "Polling unit saved successfully...")
            if action == "another":
                return redirect("elections:add_polling_unit_result")
            else:
                return redirect("elections:pulling_unit_result")
    context = {
        "page_title": "Add result",
        "polling_unit_form": polling_unit_form,
        "announced_party_form": announced_party_form,
    }
    return render(request, 'elections/add_result.html', context)
