odoo.define('pos_receipt_ean.print_ean', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var core = require('web.core');

    var QWeb = core.qweb;
    var _t = core._t;

    // We do extend the export_for_printing function in the order model
    // So we can include the ean code for printing
    var OrderModelSuper = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function() {
            var data = OrderModelSuper.export_for_printing.call(this);
            data.print_ean_ticket = this.pos.config.print_ean_ticket;
            return data
        },
    });

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function(attr, options) {
            _super_orderline.initialize.apply(this, arguments);
            this.ean13 = options.product.barcode;
            this.code = options.product.default_code;
            //console.log('order model--------'+ options.product.taxes_id.id)
            //console.log('tax',this.get_taxes().options.product.taxes_id.id)
            //console.log(options.orderlines);
            var order = this.pos.get_order();
            var products = _.map(order.get_orderlines(), function (line) {return line.product; });
            console.log(products);
            for(var i =0; i < products.length; i++)
            console.log(products[i].id);

        },
        export_as_JSON: function() {
            var data = _super_orderline.export_as_JSON.call(this);
            data.ean13 = this.ean13;
            data.code = this.code;
            return data;
        },
        export_for_printing: function() {
            var data = _super_orderline.export_for_printing.call(this);
            data.ean13 = this.ean13;
            data.code = this.code;
            return data;
        },
    });
    var _super_PosModel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        get_model: function (_name) {
            var _index = this.models.map(function (e) {
                return e.model;
            }).indexOf(_name);
            if (_index > -1) {
                return this.models[_index];
            }
            return false;
        },
        initialize: function (session, attributes) {
            var self = this;
            var company_model = this.get_model('res.company');
            company_model.fields.push('street','city');

            _super_PosModel.initialize.apply(this, arguments);

        },
        get_config: function () {
            return this.config;
        },

    });
});