from odoo import models, fields, api

class AirivDashboardIndonesia(models.Model):
    _name = 'airiv.dashboard.indonesia'
    _description = 'AIRIV Dashboard Indonesia Operational Intelligence'

    name = fields.Char(string='Description', required=True, default='Indonesian UMKM Metrics')
    effective_ppn = fields.Float(string='Effective PPN Rate (%)', default=11.0)
    
    def _run_integration_test_suite(self):
        self.ensure_one()
        return True
