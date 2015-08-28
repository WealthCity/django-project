__author__ = 'cristian'

from django.contrib import admin
from portfolios.models import ProxyAssetClass, ProxyTicker
from main.models import Firm, Advisor, User
from suit.admin import SortableTabularInline
from suit.admin import SortableModelAdmin


class TickerInline(SortableTabularInline):
    model = ProxyTicker
    sortable = 'ordering'


class AdvisorInline(admin.StackedInline):
    model = Advisor


class AssetClassAdmin(SortableModelAdmin):
    list_display = ('name', 'display_name', 'display_order', 'investment_type', 'super_asset_class')
    inlines = (TickerInline,)
    sortable = 'display_order'


class FirmFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'filter by firm'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'firm'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_id = [[None, "All"]]
        for firm in Firm.objects.all():
            list_id.append([firm.pk, firm.firm_name])

        return list_id

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.

        if self.value() is None:
            return queryset.all()

        return queryset.filter(firm__pk=self.value())


def approve_application(modeladmin, request, queryset):
    queryset.update(is_accepted=True)
approve_application.short_description = "Mark selected advisor applications as approved"


class AdvisorAdmin(admin.ModelAdmin):
    list_display = ('user', 'work_phone', 'is_accepted', 'is_confirmed', 'is_supervisor', 'firm')
    list_filter = ('is_accepted', FirmFilter)
    actions = (approve_application, )

    pass


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    exclude = ('password', )
    pass


class FirmAdmin(admin.ModelAdmin):
    list_display = ('firm_name', )
    inlines = (AdvisorInline,)
    pass

admin.site.register(ProxyAssetClass, AssetClassAdmin)
admin.site.register(Firm, FirmAdmin)
admin.site.register(Advisor, AdvisorAdmin)
admin.site.register(User, UserAdmin)