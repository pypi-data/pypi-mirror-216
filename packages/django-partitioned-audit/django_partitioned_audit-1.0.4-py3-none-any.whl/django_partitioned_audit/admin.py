from django.contrib import admin


class TriggerAuditEntryAdmin(admin.ModelAdmin):
    list_display = ("audit_entry_created", "object_table", "audit_operation")
    list_filter = ("object_table", "audit_operation")

    def save_form(self, request, form, change):
        raise NotImplementedError()

    def save_formset(self, request, form, formset, change):
        raise NotImplementedError()

    def save_model(self, request, obj, form, change):
        raise NotImplementedError()

    def save_related(self, request, form, formsets, change):
        raise NotImplementedError()

    def delete_view(self, request, object_id, extra_context=None):
        raise NotImplementedError()

    def delete_model(self, request, obj):
        raise NotImplementedError()

    def delete_queryset(self, request, queryset):
        raise NotImplementedError()

    # FIXME: add other methods to make Admin RO
    # TODO: maybe this is not required if we change permissions in DB
    # TODO: probably multi-db hints might be a more secure and transparent way
    # https://docs.djangoproject.com/en/3.0/topics/db/multi-db/#topics-db-multi-db-hints
