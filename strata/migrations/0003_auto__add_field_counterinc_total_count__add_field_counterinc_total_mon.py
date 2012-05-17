# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CounterInc.total_count'
        db.add_column('strata_counterinc', 'total_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'CounterInc.total_money'
        db.add_column('strata_counterinc', 'total_money',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=32, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CounterInc.total_count'
        db.delete_column('strata_counterinc', 'total_count')

        # Deleting field 'CounterInc.total_money'
        db.delete_column('strata_counterinc', 'total_money')


    models = {
        'strata.counter': {
            'Meta': {'ordering': "['name']", 'object_name': 'Counter'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '32', 'decimal_places': '2', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'})
        },
        'strata.counterinc': {
            'Meta': {'object_name': 'CounterInc'},
            'counter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['strata.Counter']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'total_count': ('django.db.models.fields.IntegerField', [], {}),
            'total_money': ('django.db.models.fields.DecimalField', [], {'max_digits': '32', 'decimal_places': '2'})
        }
    }

    complete_apps = ['strata']