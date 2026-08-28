/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class AirivExecutiveDashboard extends Component {
    static template = "airiv_dashboard_indonesia.ExecutiveDashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.refreshTimer = null;
        this.previousConfirmedCount = null;

        this.state = useState({
            currentFilter: "30d",
            autoRefreshInterval: 30,
            soundEnabled: true,
            recentSaleAlert: null,
            lastUpdated: new Date().toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit", second: "2-digit" }) + " WIB",
            metrics: {
                company_name: "AIRIV.id",
                active_filter: "30d",
                filter_label: "Last 30 Days",
                total_sales_count: 0,
                confirmed_sales_count: 0,
                total_revenue_formatted: "Rp 0",
                invoice_count: 0,
                total_invoiced_formatted: "Rp 0",
                avg_deal_size: "Rp 0",
                top_products: [],
                plugins: [],
                forex: {
                    usd_mid: "Rp 16.250",
                    usd_buy: "Rp 16.180",
                    usd_sell: "Rp 16.320",
                    eur_mid: "Rp 17.650",
                    eur_buy: "Rp 17.580",
                    eur_sell: "Rp 17.720",
                    source: "Bank Indonesia JISDOR & Interbank Spot",
                    updated_at: "WIB"
                },
                inventory_alerts: {
                    total_alerts: 0,
                    out_of_stock_count: 0,
                    low_stock_count: 0,
                    items: []
                },
                ar_aging: {
                    total_ar_formatted: "Rp 0",
                    bucket_current_formatted: "Rp 0",
                    bucket_30_60_formatted: "Rp 0",
                    bucket_60_plus_formatted: "Rp 0",
                    bucket_current_pct: 0,
                    bucket_30_60_pct: 0,
                    bucket_60_plus_pct: 0,
                    open_invoice_count: 0,
                    top_debtors: []
                },
                tax_compliance: {
                    taxable_base_formatted: "Rp 0",
                    total_ppn_formatted: "Rp 0",
                    compliance_rate: 100,
                    missing_npwp_count: 0,
                    total_invoices_audited: 0,
                    statutory_rate: "12%",
                    effective_rate: "11% (DPP Nilai Lain)"
                },
                tri_gateway: {
                    total_settled_formatted: "Rp 0",
                    total_fees_formatted: "Rp 0",
                    total_net_formatted: "Rp 0",
                    tx_count: 0,
                    midtrans_vol_formatted: "Rp 0",
                    xendit_vol_formatted: "Rp 0",
                    paypal_vol_formatted: "Rp 0",
                    recent_feed: []
                },
                shipping_radar: {
                    total_active: 0,
                    in_transit_count: 0,
                    pending_pickup_count: 0,
                    delivered_count: 0,
                    returned_count: 0,
                    cod_escrow_held_formatted: "Rp 0",
                    cod_disbursed_formatted: "Rp 0",
                    cod_pending_count: 0,
                    jne_pct: 0,
                    jnt_pct: 0,
                    sicepat_pct: 0,
                    instant_pct: 0,
                    recent_shipments: []
                },
                treasury: {
                    total_ap_formatted: "Rp 0",
                    net_working_capital_formatted: "Rp 0",
                    net_working_capital_positive: true,
                    bucket_current_formatted: "Rp 0",
                    bucket_30_60_formatted: "Rp 0",
                    bucket_60_plus_formatted: "Rp 0",
                    bucket_current_pct: 0,
                    bucket_30_60_pct: 0,
                    bucket_60_plus_pct: 0,
                    open_bills_count: 0,
                    top_vendors: []
                },
                import_pib: {
                    fob_usd_formatted: "$0",
                    cif_idr_formatted: "Rp 0",
                    bea_masuk_formatted: "Rp 0",
                    ppn_impor_formatted: "Rp 0",
                    pph_22_impor_formatted: "Rp 0",
                    total_pib_tax_formatted: "Rp 0",
                    total_landed_idr_formatted: "Rp 0",
                    landed_multiplier: 1.21,
                    active_po_count: 0
                }
            },
            isLoading: false
        });

        onWillStart(async () => {
            await this.loadDashboardData(this.state.currentFilter);
            this.setAutoRefresh(this.state.autoRefreshInterval);
        });

        onWillUnmount(() => {
            this._clearAutoRefreshTimer();
        });
    }

    get hasStockAlerts() {
        return Boolean(this.state.metrics.inventory_alerts && this.state.metrics.inventory_alerts.total_alerts > 0);
    }

    get stockAlertCount() {
        return (this.state.metrics.inventory_alerts && this.state.metrics.inventory_alerts.total_alerts) || 0;
    }

    get conversionPercentage() {
        const total = this.state.metrics.total_sales_count || 0;
        const confirmed = this.state.metrics.confirmed_sales_count || 0;
        if (total === 0) return 0;
        return Math.round((confirmed / total) * 100);
    }

    _playExecutiveChime() {
        if (!this.state.soundEnabled) return;
        try {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (!AudioCtx) return;
            const ctx = new AudioCtx();
            const now = ctx.currentTime;

            const osc1 = ctx.createOscillator();
            const gain1 = ctx.createGain();
            osc1.type = "sine";
            osc1.frequency.setValueAtTime(659.25, now);
            gain1.gain.setValueAtTime(0.18, now);
            gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
            osc1.connect(gain1);
            gain1.connect(ctx.destination);
            osc1.start(now);
            osc1.stop(now + 0.35);

            const osc2 = ctx.createOscillator();
            const gain2 = ctx.createGain();
            osc2.type = "sine";
            osc2.frequency.setValueAtTime(880.00, now + 0.12);
            gain2.gain.setValueAtTime(0.22, now + 0.12);
            gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.65);
            osc2.connect(gain2);
            gain2.connect(ctx.destination);
            osc2.start(now + 0.12);
            osc2.stop(now + 0.65);

            const osc3 = ctx.createOscillator();
            const gain3 = ctx.createGain();
            osc3.type = "triangle";
            osc3.frequency.setValueAtTime(1108.73, now + 0.25);
            gain3.gain.setValueAtTime(0.15, now + 0.25);
            gain3.gain.exponentialRampToValueAtTime(0.001, now + 0.85);
            osc3.connect(gain3);
            gain3.connect(ctx.destination);
            osc3.start(now + 0.25);
            osc3.stop(now + 0.85);
        } catch (e) {
            console.warn("Audio chime error:", e);
        }
    }

    _clearAutoRefreshTimer() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
        }
    }

    setAutoRefresh(seconds) {
        const intervalSec = Number(seconds);
        this.state.autoRefreshInterval = intervalSec;
        this._clearAutoRefreshTimer();

        if (intervalSec > 0) {
            this.refreshTimer = setInterval(async () => {
                await this.loadDashboardData(this.state.currentFilter, true);
            }, intervalSec * 1000);
        }
    }

    toggleSound() {
        this.state.soundEnabled = !this.state.soundEnabled;
        if (this.state.soundEnabled) {
            this._playExecutiveChime();
        }
    }

    dismissSaleAlert() {
        this.state.recentSaleAlert = null;
    }

    openVendorBills() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Hutang Usaha (Vendor Bills)",
            res_model: "account.move",
            domain: [["move_type", "=", "in_invoice"], ["state", "=", "posted"], ["payment_state", "in", ["not_paid", "partial"]]],
            views: [[false, "list"], [false, "form"]],
            target: "current"
        });
    }

    openPurchaseOrders() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Vendor Bills & Import Expenses",
            res_model: "account.move",
            domain: [["move_type", "=", "in_invoice"]],
            views: [[false, "list"], [false, "form"]],
            target: "current"
        });
    }

    openShippingHub() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Logistics & Courier Hub",
            res_model: "airiv.shipping.tracker",
            views: [[false, "list"], [false, "form"]],
            target: "current"
        });
    }

    trackResi(trackingUrl) {
        if (trackingUrl) {
            window.open(trackingUrl, "_blank");
        }
    }

    openPartnerForm(partnerId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "res.partner",
            res_id: partnerId,
            views: [[false, "form"]],
            target: "current"
        });
    }

    openGatewayTransactions() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Tri-Gateway Payment Feeds",
            res_model: "airiv.gateway.transaction",
            views: [[false, "list"], [false, "form"]],
            target: "current"
        });
    }

    openCustomerInvoices(filterType = "all") {
        const domain = [["move_type", "=", "out_invoice"]];
        if (filterType === "unpaid") {
            domain.push(["payment_state", "in", ["not_paid", "partial"]]);
            domain.push(["state", "=", "posted"]);
        }
        this.action.doAction({
            type: "ir.actions.act_window",
            name: filterType === "unpaid" ? "Piutang Usaha (Unpaid Invoices)" : "Customer Invoices",
            res_model: "account.move",
            domain: domain,
            views: [[false, "list"], [false, "form"]],
            target: "current"
        });
    }

    sendWhatsAppReminder(debtor) {
        if (!debtor.phone) {
            this.notification.add(`No phone number available for ${debtor.name}`, { type: "warning" });
            return;
        }
        const text = encodeURIComponent(
            `Halo ${debtor.name},\n\nKami dari *${this.state.metrics.company_name}* menginformasikan bahwa terdapat tagihan outstanding sebesar *${debtor.total_due_formatted}* yang telah melewati jatuh tempo.\n\nMohon konfirmasi kesiapan pembayaran melalui rekening Virtual Account / transfer bank kami. Terima kasih atas kerja samanya.\n\n_Salam hormat, Finance Team._`
        );
        window.open(`https://wa.me/${debtor.phone}?text=${text}`, "_blank");
    }

    openProductForm(productId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "product.product",
            res_id: productId,
            views: [[false, "form"]],
            target: "current"
        });
    }

    openInventoryReplenishment() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Replenishment Rules",
            res_model: "stock.warehouse.orderpoint",
            views: [[false, "list"], [false, "form"]],
            target: "current"
        });
    }

    async loadDashboardData(filterKey = "30d", isBackground = false) {
        if (!isBackground) {
            this.state.isLoading = true;
        }
        try {
            const data = await this.orm.call(
                "airiv.dashboard.plugin",
                "get_dashboard_metrics",
                [filterKey]
            );
            if (data) {
                if (this.previousConfirmedCount !== null && data.confirmed_sales_count > this.previousConfirmedCount) {
                    const newOrders = data.confirmed_sales_count - this.previousConfirmedCount;
                    this._playExecutiveChime();
                    this.state.recentSaleAlert = {
                        count: newOrders,
                        total_revenue: data.total_revenue_formatted,
                        time: new Date().toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" }) + " WIB"
                    };

                    this.notification.add(
                        `New Sales Order Confirmed! Total Revenue: ${data.total_revenue_formatted}`,
                        {
                            title: "AIRIV Command Center Telemetry",
                            type: "success",
                            sticky: false
                        }
                    );
                }

                this.previousConfirmedCount = data.confirmed_sales_count;
                this.state.metrics = Object.assign({}, this.state.metrics, data);
                this.state.lastUpdated = new Date().toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit", second: "2-digit" }) + " WIB";
            }
        } catch (error) {
            console.error("AIRIV Dashboard telemetry error:", error);
        } finally {
            this.state.isLoading = false;
        }
    }

    async setDateFilter(filterKey) {
        if (this.state.currentFilter === filterKey && !this.state.isLoading) return;
        this.state.currentFilter = filterKey;
        await this.loadDashboardData(filterKey);
    }

    exportExcel() {
        const filter = encodeURIComponent(this.state.currentFilter);
        window.location.href = `/airiv_dashboard/export_excel?date_filter=${filter}`;
    }

    exportPdf() {
        const filter = encodeURIComponent(this.state.currentFilter);
        window.open(`/airiv_dashboard/export_pdf?date_filter=${filter}`, '_blank');
    }

    async _onRefresh() {
        await this.loadDashboardData(this.state.currentFilter);
    }
}

registry.category("actions").add("airiv_dashboard_indonesia.ExecutiveDashboard", AirivExecutiveDashboard);
