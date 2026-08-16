from django.db import migrations, models


def remove_duplicate_pending_alerts(apps, schema_editor):
    StockAlert = apps.get_model('inventory', 'StockAlert')
    seen = set()
    for alert in StockAlert.objects.filter(notified=False).order_by('id'):
        key = (alert.variant_id, alert.email.lower())
        if key in seen:
            alert.delete()
        else:
            seen.add(key)


class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_duplicate_pending_alerts, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='stockalert',
            constraint=models.UniqueConstraint(
                condition=models.Q(notified=False),
                fields=('variant', 'email'),
                name='unique_pending_stock_alert',
            ),
        ),
    ]
