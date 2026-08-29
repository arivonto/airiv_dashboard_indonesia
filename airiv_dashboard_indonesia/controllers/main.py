from odoo import http
from odoo.http import request

class AirivDemoController(http.Controller):

    @http.route('/demo', type='http', auth='none', website=True)
    def airiv_demo_dashboard(self, **kwargs):
        installed_modules = []
        try:
            domain = [('name', 'like', 'airiv_'), ('state', '=', 'installed')]
            modules = request.env['ir.module.module'].sudo().search(domain)
            for m in modules:
                installed_modules.append({
                    'name': m.shortdesc or m.name,
                    'technical_name': m.name,
                    'version': m.installed_version or '18.0.1.0.0',
                    'summary': m.summary or 'Indonesian UMKM Localization Module'
                })
        except Exception:
            pass

        plugin_cards_html = ""
        for mod in installed_modules:
            plugin_cards_html += f"""
            <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs hover:shadow-md transition-shadow flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-xs font-semibold px-2.5 py-1 bg-emerald-50 text-emerald-700 rounded-md border border-emerald-100">{mod.get('version', '18.0.1.0.0')}</span>
                        <span class="text-xs font-mono text-slate-400">{mod.get('technical_name')}</span>
                    </div>
                    <h3 class="font-bold text-slate-900 text-base mb-1">{mod.get('name')}</h3>
                    <p class="text-xs text-slate-600 leading-relaxed mb-4">{mod.get('summary')}</p>
                </div>
                <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
                    <span class="text-xs font-medium text-emerald-600 flex items-center gap-1.5">
                        <span class="h-2 w-2 rounded-full bg-emerald-500"></span> Active
                    </span>
                    <span class="text-xs font-semibold text-blue-600 bg-blue-50 px-2 py-0.5 rounded">LGPL-3</span>
                </div>
            </div>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Airiv Command Center - Executive Dashboard &amp; Plugins</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-slate-50 font-sans text-slate-900 antialiased min-h-screen flex flex-col">
            <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                        <div class="h-3.5 w-3.5 bg-emerald-500 rounded-full animate-pulse"></div>
                        <span class="font-bold text-slate-800 text-lg tracking-tight">Airiv Command Center</span>
                    </div>
                    <a href="/web" class="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-sm font-medium rounded-lg shadow-sm transition-colors">ERP Workspace Login</a>
                </div>
            </header>
            <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div class="bg-gradient-to-r from-slate-900 to-slate-800 rounded-2xl p-6 sm:p-8 text-white shadow-lg mb-8">
                    <h1 class="text-2xl sm:text-3xl font-bold tracking-tight mb-2">Executive Governance &amp; Compliance Hub</h1>
                    <p class="text-slate-300 text-sm sm:text-base leading-relaxed">High-performance enterprise command center tailored for Indonesian SMEs and UMKM.</p>
                </div>
                <div class="mb-8">
                    <div class="flex items-center justify-between mb-6">
                        <h2 class="text-xl font-bold text-slate-900">Installed Indonesian Localization Plugins</h2>
                        <span class="px-3 py-1 bg-slate-200 text-slate-700 text-xs font-semibold rounded-full">{len(installed_modules)} Modules Active</span>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {plugin_cards_html}
                    </div>
                </div>
            </main>
        </body>
        </html>
        """
        return request.make_response(html_content, [('Content-Type', 'text/html; charset=utf-8')])
