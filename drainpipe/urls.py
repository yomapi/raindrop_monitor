from django.urls import path


from drainpipe.views import find_drainpipe_data_with_limit


urlpatterns = [path("<district_code>", find_drainpipe_data_with_limit)]
