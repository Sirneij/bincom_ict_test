from django.contrib import admin

from . import models


@admin.register(models.Agentname)
class AgentnameAdmin(admin.ModelAdmin):
    list_display = ('name_id', 'firstname', 'lastname', 'pollingunit_uniqueid')


@admin.register(models.AnnouncedLgaResults)
class AnnouncedLgaResultsAdmin(admin.ModelAdmin):
    list_display = ('result_id', 'lga_name',
                    'party_abbreviation', 'party_score')


@admin.register(models.AnnouncedPuResults)
class AnnouncedPuResultsAdmin(admin.ModelAdmin):
    list_display = ('result_id', 'polling_unit_uniqueid',
                    'party_abbreviation', 'party_score')
    search_fields = ['polling_unit_uniqueid']
    sortable_by = ['party_abbreviation']


@admin.register(models.AnnouncedStateResults)
class AnnouncedStateResultsAdmin(admin.ModelAdmin):
    list_display = ('result_id', 'state_name',
                    'party_abbreviation', 'party_score')


@admin.register(models.AnnouncedWardResults)
class AnnouncedWardResultsAdmin(admin.ModelAdmin):
    list_display = ('result_id', 'ward_name',
                    'party_abbreviation', 'party_score')


@admin.register(models.Lga)
class LgaAdmin(admin.ModelAdmin):
    list_display = ('uniqueid', 'lga_id',
                    'lga_name', 'state_id',)


@admin.register(models.Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('partyid', 'partyname',)


@admin.register(models.PollingUnit)
class PollingUnitAdmin(admin.ModelAdmin):
    list_display = ('polling_unit_id', 'ward_id', 'lga_id', 'uniquewardid',
                    'polling_unit_number', 'polling_unit_name', 'polling_unit_description')
    search_fields = ['polling_unit_number']
