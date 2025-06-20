from django.contrib.admin import AdminSite


class ZooAdminSite(AdminSite):
    site_header = 'Администрирование зоопарка'
    site_title = 'Зоопарк'
    index_title = 'Управление зоопарком'


admin_site = ZooAdminSite(name='zoo_admin')
