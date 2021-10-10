from django.contrib import admin


from table.models import (login_table, login_time, num_of_leaves, cur_running,
                              app_status, cse_dep, ee_dep, mec_dep, hoddean,
                              cse_hod, mec_hod, ee_hod, hod_dean, director, dean, hodapp, deanapp, dirapp)

admin.site.register(login_table)
admin.site.register(login_time)
admin.site.register(num_of_leaves)
admin.site.register(cur_running)
admin.site.register(app_status)
admin.site.register(cse_dep)
admin.site.register(ee_dep)
admin.site.register(mec_dep)
admin.site.register(hoddean)
admin.site.register(cse_hod)
admin.site.register(mec_hod)
admin.site.register(ee_hod)
admin.site.register(hod_dean)
admin.site.register(director)
admin.site.register(dean)
admin.site.register(hodapp)
admin.site.register(deanapp)
admin.site.register(dirapp)

