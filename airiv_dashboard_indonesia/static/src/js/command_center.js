/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class AirivCommandCenter extends Component {
    static template = "airiv_dashboard_indonesia.CommandCenterView";
    
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            metrics: {},
            ai_insight: "Loading Gemini AI insights...",
            loading: true
        });

        onWillStart(async () => {
            await this.fetchMetrics();
            await this.fetchAiInsights();
        });
    }

    async fetchMetrics() {
        this.state.metrics = await this.orm.call("airiv.command.center", "get_indonesian_metrics", []);
    }

    async fetchAiInsights() {
        const response = await this.orm.call("airiv.command.center", "query_gemini_insights", ["Analyze daily UMKM metrics"]);
        this.state.ai_insight = response.response;
        this.state.loading = false;
    }
}

registry.category("actions").add("airiv_dashboard_indonesia.CommandCenter", AirivCommandCenter);
