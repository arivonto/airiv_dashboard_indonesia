/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class ExecutiveDashboard extends Component {
    static template = "airiv_dashboard_indonesia.ExecutiveDashboard";
}

registry.category("actions").add("airiv_dashboard_indonesia.ExecutiveDashboard", ExecutiveDashboard);
