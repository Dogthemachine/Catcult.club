import json
import requests

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from django.utils.dateformat import format


class Command(BaseCommand):
    help = 'Import directories.'

    def handle(self, *args, **options):
        from apps.orders.models import NovaPoshtaCities, NovaPoshtaWarehouses, NovaPoshtaRegions

        print(timezone.now())

        import_items = 0
        j = json.loads(
            '{"modelName": "Address", "calledMethod": "getAreas", "apiKey":"%s"}' % settings.NOVA_POSHTA_API)
        r = requests.post('https://api.novaposhta.ua/v2.0/json/', json=j, headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            NovaPoshtaRegions.objects.all().delete()
            for region in json.loads(r.text)['data']:
                nova_poshta_region = NovaPoshtaRegions(
                    description_ru=region.get('DescriptionRu', None),
                    description_uk=region.get('Description', None),
                    ref=region.get('Ref', None),
                    areasenter_ref=region.get('AreasCenter', None),
                )
                nova_poshta_region.save()
                import_items += 1
        else:
            print('Ошибка %s при запросе областей у Новой почты' % r.status_code)
        print(timezone.now(), 'Проимпортировано %s областей' % import_items)

        import_items = 0
        j = json.loads(
            '{"modelName": "AddressGeneral", "calledMethod": "getCities", "apiKey":"%s"}' % settings.NOVA_POSHTA_API)
        r = requests.post('https://api.novaposhta.ua/v2.0/json/', json=j, headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            NovaPoshtaCities.objects.all().delete()
            for city in json.loads(r.text)['data']:
                region = None
                try:
                    region = NovaPoshtaRegions.objects.get(ref=city.get('Area'))
                except:
                    print('Не найдена область %s в справочнике Новой почты.' % city.get('AreaDescription', '-нет-'))
                nova_poshta_city = NovaPoshtaCities(
                    description_ru=city.get('DescriptionRu', None),
                    description_uk=city.get('Description', None),
                    ref=city.get('Ref', None),
                    novaposhtaregions=region,
                    settlement_type_description=city.get('SettlementTypeDescription', None),
                    settlement_type_description_ru=city.get('SettlementTypeDescriptionRu', None),
                    area_description=city.get('AreaDescription', None),
                    area_description_ru=city.get('AreaDescription', None),
                )
                nova_poshta_city.save()
                import_items += 1
        else:
            print('Ошибка %s при запросе городов у Новой почты' % r.status_code)
        print(timezone.now(), 'Проимпортировано %s городов' % import_items)

        import_items = 0
        j = json.loads(
            '{"modelName": "AddressGeneral", "calledMethod": "getWarehouses", "apiKey":"%s"}' % settings.NOVA_POSHTA_API)
        r = requests.post('https://api.novaposhta.ua/v2.0/json/', json=j, headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            NovaPoshtaWarehouses.objects.all().delete()
            for warehouse in json.loads(r.text)['data']:
                city = None
                try:
                    city = NovaPoshtaCities.objects.get(ref=warehouse.get('CityRef'))
                except:
                    print('Не найден город %s в справочнике Новой почты.' % warehouse.get('CityRef', '-нет-'))
                if city:
                    nova_poshta_warehouse = NovaPoshtaWarehouses(
                        description_ru=warehouse.get('DescriptionRu', None),
                        description_uk=warehouse.get('Description', None),
                        number=warehouse.get('Number', None),
                        ref=warehouse.get('Ref', None),
                        novaposhtacities=city,
                    )
                    nova_poshta_warehouse.save()
                    import_items += 1

        else:
            print('Ошибка %s при запросе отделений у Новой почты' % r.status_code)
        print(timezone.now(), 'Проимпортировано %s складов' % import_items)
