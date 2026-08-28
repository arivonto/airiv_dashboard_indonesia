from odoo import http
from odoo.http import request

class AirivGuestLogin(http.Controller):
    @http.route('/demo', type='http', auth='public', website=True)
    def auto_login_guest(self, **kwargs):
        # Authenticate silently using the guest sandbox credentials
        db_name = request.session.db or 'your_database_name'
        request.session.authenticate(db_name, 'guest@airiv.id', 'explore123')
        
        # Redirect directly to your Command Center action
        return request.redirect('/web#action=1094&model=airiv.dashboard&view_type=kanban')
