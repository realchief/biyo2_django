/**
 * Created by Konstantin Oficerov.
 *
 * This module is supposed to save Orders, order items and order modifiers.
 * It also responsible for any of elements behaviour and UI.
 */


;(function($, document){

    $.fn.serializeObject = function()
    {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

//    $('#order-part input:not(.span1):not(.span2):not(#id_discount_orders), #order-part select').addClass('span12');
    var datepickerConfig = {/*Fill on if it is necessary*/};
    $('[name$="date"]').datetimepicker(datepickerConfig);

    var ErrorManager = function(bound){
        this.form = $(bound);
    };
    ErrorManager.fn = ErrorManager.prototype;
    ErrorManager.fn.renderErrors = function(JSON_loads){
        var key, error_field;
        for(key in JSON_loads){
            error_field = this.form.find('[name="'+key+'"]');
            $('<span class="help-inline error-text">'+ JSON_loads[key] +'</span>').insertAfter(error_field);
            error_field.parent().addClass('error');
        }
    };
    ErrorManager.fn.clear = function(){
        this.form.find('.control-group.error').removeClass('error');
        this.form.find('span.help-inline.error-text').remove();
    };


    var FieldManager = function(sources, destinations, src_field_selectors, dest_field_selectors, options){
        this.options = options || {fn: {default: function(){return 0;}}};
        this.sources = sources;
        this.destinations = destinations;
        this.src_selectors  = src_field_selectors;
        this.dest_selectors = dest_field_selectors;
    };

    FieldManager.fn = FieldManager.prototype;

    FieldManager.fn.populate = function(){
        (function(self){
            var tmp_res = {};
            var _ref1 = self.dest_selectors.length;
            $.each(self.sources, function(ind1, src){
                $.each(self.src_selectors, function(ind2, sel){
                    if(ind2 < _ref1){
                        if (tmp_res[self.dest_selectors[ind2]] === undefined || tmp_res[self.dest_selectors[ind2]] === null){
                            tmp_res[self.dest_selectors[ind2]] = 0;
                        }
                        var fn = self.options.fn[sel] || self.options.fn.default;
                        tmp_res[self.dest_selectors[ind2]] += fn.call(null, src.form.find(sel).val(), src);
                    }
                });
            });
            $.each(self.destinations, function(ind1, dest){
                for(var sel in tmp_res){
                    dest.form.find(sel).val(tmp_res[sel]);
                }
                dest.changeValue();
            });

        })(this);
    };


    var OrderForm = function(){
        this.preloader = $('#order-preloader');
        this.processing = new $.Deferred();
        this.processing.resolve();  // Just to get into with the first iteration ...
        this.instance = null;
        this.instance_input = $('#id_order_id');  //TODO: perhaps obsolete
        this.form_selector = '#add-order-form';
        this.form = $(this.form_selector);
        this.baseURI = '/terminalapi';
        this.errorManager = new ErrorManager($(this.form_selector));
        this.discount_button = this.form.find('#id_select_discount');
        this.save_close_button = this.form.find('#btn_close');
        this.cancel_button = this.form.find('#btn_cancel');
        this.hold_button = this.form.find('#btn_hold');
        this.refund_button = this.form.find('#btn_refund');
        this.payments = null;
        this.customerPrices = {};
        this.initialize();
    };

    OrderForm.fn = OrderForm.prototype;

    OrderForm.fn.initialize = function(){

        (function(self){
            $.each(self.form.find('select, input, textarea'), function(index, field) {
                if(field.id === "id_discount_orders"){
                    $(field).on('keydown', function(){
                        $(this).data({key: true});
                    });
                    $(field).on('change', function(){
                        if($(this).data('key')){
                            form.discount = null;
                            form.discount_button.next().find('.icon-ok').hide();
                        }
                        $(this).data({key: false});
                    });
                }

                $(field).on('change', function(){
                    if(this.id === "id_customer_id"){
                        if(this.value){
                            self.current_customer = Number(this.value);
                            //self.loadSpecialPrices();
                            $('.pay-with-account', '#payment-part').show();
                        } else {
                            self.current_customer = null;
                            $('.pay-with-account', '#payment-part').hide();
                        }
                        if(self.formset && self.formset.forms.length){
                            $.each(self.formset.forms, function(_i1, form){
                                form.adjustPrice();
                                form.changeValue();
                            })
                        }
                    }
                    self.changeValue();
                })
            });
            // TODO: Uncomment it later - it is necessary and working part!
            //form.discount_button.on('click', function(){
            //    form.attachDiscounts();
            //});
            var actionButtonCallbackWrap = function (fn, forbid_redirect) {
                $("#screen_locker").fadeIn(300);
                fn();
                self.createOrUpdate(self.serialize(), function(data){
                    if(!forbid_redirect){
                        window.location = "/orders";
                    }else{
                        $("#screen_locker").fadeOut(300);
                    }
                    if (data.status == 3) {
                        self.enableRefund();
                    }
                });
                return false;
            };

            self.close_order = function(){
                self.form.find("#id_close_date").val((new Date).toISOString().replace(/\..*/, ""));
                self.form.find("#id_status").val(3);
                self.form.find("#id_emp_close_id").val($(this).parent().data('user'));
            };

            self.save_close_button.on('click', function(){
                return actionButtonCallbackWrap(function(){
                    self.form.find("#id_status").val(1);
                }, $(this).data('close'));
            });

            self.cancel_button.on('click', function(){
                return actionButtonCallbackWrap(function(){
                    self.close_order();
                    self.form.find("#id_status").val(4);
                });
            });

            self.hold_button.on('click', function(){
                return actionButtonCallbackWrap(function(){
                    self.form.find("#id_hold_date").val((new Date).toISOString().replace(/\..*/, ""));
                    var status = Number(self.form.find("#id_status").val());
                    self.form.find("#id_status").val(status % 2 + 1);
                    self.form.find("#id_status").val();
                    self.hold_button.toggleClass("active");
                }, true);
            });

            self.refund_button.on('click', function(){
                $("#screen_locker").fadeIn(300);
                self.payments.refundAll().done(function(){
                    return actionButtonCallbackWrap(function(){
                        self.form.find("#id_status").val(5);
                    });
                }).fail(function(){
                    $("#screen_locker").fadeOut(300);
                    self.form.prepend($("<div class='alert alert-primary payment-error'><button class='close' data-dismiss='alert'><i class='icon-remove'></i></button><p>Server failed to process transactions.<br/>Please, try again later.</p></div>"))
                });
                return false;
            });

            self.enableRefund = function () {
                self.refund_button.parent().show();
                self.save_close_button.parent().hide();
            }

        })(this);
    };


    OrderForm.fn.serialize = function(){
        var res = $(this.form_selector).serializeObject();
        res.open_date = (res.open_date || '').replace(' ', "T");
        res.close_date = (res.close_date || '').replace(' ', "T");
        res.hold_date = (res.hold_date || '').replace(' ', "T");
        res.customer = res.customer_id;
        for(var key in res){
            if(!res[key]){
                delete res[key];
            }
        }

        return res;
    };

    OrderForm.fn.showPreloader = function(){
        this.preloader.show();
    };

    OrderForm.fn.hidePreloader = function(){
        this.preloader.hide();
    };

    OrderForm.fn.calculateDiscount = function(selector_discount, selector_price){
        var result;
        if(this.discount){
            if(this.discount.type === 1){
                result = Number(this.form.find(selector_price).val()) *  this.discount.value / 100.0;
            } else if (this.discount.type === 2) {
                result = this.discount.value;
            }
        } else {
            result = Number(this.form.find(selector_discount).val() || 0);
        }
        return (result > Number(this.form.find(selector_price).val())) ? 0 : result.toFixed(2);
    };

    OrderForm.fn.attachDiscounts = function(){
        (function(self){
            var dropdown = self.discount_button.next();
            var showDiscounts = function(){
                $.each(self.discounts, function(i, discount){
                    if(!discount.archived){
                        dropdown.append(self.generateDiscountRow(discount));
                    }
                });

                dropdown.find('li>a').on('click', function(e){
                    self.discount = $(this).data();
                    dropdown.find('.icon-ok').hide();
                    $(this).find('.icon-ok').show();
                    var field = self.form.find('#id_discount_orders');
                    field.val(self.calculateDiscount('#id_discount_orders', '#id_subtotal'));
                    field.trigger('change');
                    $(this).prop('active', true);
                    e.preventDefault();
                });

            };
            if(!self.discounts){
                $.ajax({
                    url: self.baseURI + '/sync/discount',
                    type: 'GET',
                    dataType: 'json',
                    success: function(data){
                        self.discounts = data.results;
                        $('li.li-preloader').remove();
                        showDiscounts();
                    },
                    error: function(){
                        console.error("Failed to load discounts: ", arguments);
                    }
                })
            } else if (dropdown.find('li.li-preloader').length || !dropdown.find('li').length) {
                $('li.li-preloader').remove();
                showDiscounts();
            }
        })(this);
    };

    OrderForm.fn.generateDiscountRow = function(discount){
        var row = $('<a href="#" class="row-fluid" style="width: inherit;"></a>');
        row.append($('<div class="span7">'+ discount.name +'</div>'));
        row.append($('<div class="span4">'+ discount.value +
            (function(){
                if(discount.type == '1'){
                    return '%'
                }else if(discount.type == '2'){
                    return '$'
                }else{
                    return ''
                }
            })() +'</div>'));
        row.append($("<i class='icon-ok' style='display: none;'></i>"));
        row.wrap("<li role='menuitem'></li>");
        row.data(discount);
        return row.parent();
    };

    OrderForm.fn.createOrUpdate = function(data, callback){
        data["terminal_id"]="-1";
        (function(self){
            self.processing.done(function(){
                var uri, method;
                self.processing = new $.Deferred();

                if(self.instance){
                    uri = self.baseURI + '/update/order/' + self.instance;
                    method = 'PUT';
                } else {
                    uri = self.baseURI + '/add/order';
                    method = 'POST';
                }
                self.showPreloader();
                self.errorManager.clear();
                return $.ajax({
                    url: uri,
                    type: method,
                    data: JSON.stringify(data),
                    contentType: "application/json",
                    success: callback,
                    error: function(XHR){
                        console.error('Error occurred while sending request to ' + uri, arguments);
                        try{
                            self.errorManager.renderErrors(JSON.parse(XHR.responseText))
                        } catch (e){
                            $('<div class="alert alert-error alert-block">Unidentified server error. ' +
                                'Please, make sure that connection is established and repeat the request.</div>').insertBefore(
                                $(self.form_selector)
                            );
                        }
                    },
                    complete: function(){
                        self.hidePreloader();
                        self.processing.resolve();
                    }
                });
            });
        })(this);
    };

    OrderForm.fn.recalculate = function(){

        var subtotal = Number(this.form.find('#id_subtotal').val() || 0);
        var tax_total = Number(this.form.find('#id_tax_total').val() || 0);
        var discount = this.calculateDiscount('#id_discount_orders', '#id_subtotal');
        this.form.find('#id_discount_orders').val(discount);
        var total = subtotal + tax_total - discount;
        var paid = 0;
        if(this.payments){
            paid = this.payments.payments.reduce(function(prev, cur){
                return prev + cur.amount_paid || 0.0;
            }, 0.0);
        }
        this.form.find("#id_grand_total").val(total);
        this.form.find("#id_balance_remaining").val(total - paid);
        $('#subtotal').text(subtotal.toFixed(2));
        $('#taxes').text(tax_total.toFixed(2));
        $('#discounts').text(discount);
        $('#total h3').text(total.toFixed(2));
        $('#balance_remaining h3').text((total - paid).toFixed(2));
        $('#total').parent().show();
        if(this.payments && this.payments.form){
            this.payments.form.find("#id_amount").trigger('change');
        }
        if(total - paid <= 0 && total !== 0){
            this.close_order();
        }
    };

    OrderForm.fn.changeValue = function(initial){
        (function(self){
            self.recalculate();
            self.createOrUpdate(self.serialize(), function(data){
                if(!self.instance){
                    // console.log('Add Items Formset');
                    $.ajax({
                        url: 'items',
                        type: 'GET',
                        data: {order: data.id},
                        success: function(data){
                            data.id = null;
                            self.formset = new OrderItemsFormset(data, {parent: self});
                            if (initial) {
                                $('#add-order-item-btn').click();
                            }
                        },
                        error: function(){console.log(arguments)},
                        complete: function(){console.log(arguments)}
                    });
                }
                if (data && data.id) {
                    self.instance = data.id;
                    self.instance_input.val(data.id);
                }
                self.payments = self.payments || new PaymentHandler(self);
                $('#order-add-new-title').hide();
                $('#order-edit-title').show();
                $('#order-number').text(data.number);

                if(data.status == 3){
                    self.enableRefund();
                }
            })
        })(this);
    };

    var OrderModifier = function(data, form, parent){
        this.form = $(form);
        this.data = data;
        this.formset = parent;
        this.instance = this.form.find('#id_instance_id').val();
        var _form;
        if(this.form[0].tagName !== "FORM"){
            _form = this.form.find('form');
        } else {
            _form = this.form;
        }
        if(data){
            _form.find('[name$="group_id"]').val(data.group);
            _form.find('[name$="cost"]').val(data.cost);
            _form.find('[name$="price"]').val(data.price);
            _form.find('[name$="oryginal_id"]').val(data.id);
            _form.find('[name$="item_id"]').val(data.item);
            _form.find('[name$="name"]').val(data.name);

        }
        this.serialize = function(){
            return _form.serializeObject();
        };
        (function(self){
            self.form.find('select, input').on('change', function(){
                self.save()
            });
            self.form.find('.remove-modifier').on('click', function(){
                var void_status = self.form.find('[name$="void_status"]');
                void_status.val('true');
                void_status.trigger('change');
            });
        })(this);
    };

    OrderModifier.fn = OrderModifier.prototype;
    OrderModifier.fn.save = function(){
        var url = "/terminalapi", method;

        if(this.instance){
            url += "/update/order/item/modifier/" + this.instance;
            method = "PUT";
        } else {
            url += "/add/order/item/modifier";
            method = "POST";
        }
        this.formset.showPreloader();
        this.form.removeClass("alert-success alert-error alert-block");
        (function(self){
            $.ajax({
                url: url,
                type: method,
                data: JSON.stringify(self.serialize()),
                contentType: "application/json",
                success: function(data){
                    self.instance = data.id;
                    self.void_status = data.void_status;
                    self.name = data.name;
                    $(self.form).addClass("alert-success alert-block");
                    if(data.void_status){
                        try{
                            self.form.fadeOut(500).promise().done(self.form.remove);
                        } catch (ex) {
                            console.info("fail form removing while success: ", {exception: ex});
                        }
                    }
                    $(self.form).find("h4+h3.price-cost").text("$" + data.price.toFixed(2));
                    self.formset.ancestor.ancestor.data_manager.populate();
                    self.formset.ancestor.changeValue();
                    self.formset.lookupModifiers();
                },
                error: function(){
                    console.error('Failed to send request at '+ url, arguments);
                    $(self.form).addClass("alert-error alert-block");
                },
                complete: function(){
                    self.formset.hidePreloader();
                }
            });
        })(this);
    };

    var OrderModifierForm = function(product, parent){
        this.modal = $('#modifier-modal');
        this.product = product;
        this.ancestor = parent;
        this.modifiers = [];
        this.initialize();
    };

    OrderModifierForm.fn = OrderModifierForm.prototype;

    OrderModifierForm.fn.initialize = function(){
        (function(self){
            var common_template = self.modal.find("#template").children().first();
            self.modifier_group_template = common_template.find("#choice_section #modifier-template>div");
            self.modifier_item_template = common_template.find("#choice_section .modifier-item");
            self.order_modifier_template = common_template.find("#attachment_section #modifier-template>form");
            self.html_template = common_template.clone();
            self.html_template.find("#modifier-template").remove();
            $.each(self.product.modifier_groups, function(_i1, group){
                if(group.modifiers.length && !group.archived){
                    var accordion_grp = self.modifier_group_template.clone();
                    accordion_grp.find('a.accordion-toggle').attr('href', "#collapse_" + _i1).text(group.name);
                    accordion_grp.find('.accordion-body').attr('id', "collapse_" + _i1);
                    accordion_grp.find('.modifier-item').remove();
                    $.each(group.modifiers, function(_i2, modifier){
                        if(modifier.active && !modifier.archived){
                            var modifier_item = self.modifier_item_template.clone();
                            modifier_item.find(".add-modifier").on('click', function(){
                                self.addForm($.extend(modifier, {group: group.id, item: self.ancestor.instance}));
                            });
                            modifier_item.find(".modifier-name").text(modifier.name);
                            modifier_item.find(".modifier-price").text("$" + modifier.price.toFixed(2));
                            modifier_item.find(".modifier-cost").text("$" + modifier.cost.toFixed(2));
                            accordion_grp.find(".accordion-inner").append(modifier_item);
                        }
                    });
                    self.html_template.find("#choice_section .accordion").append(accordion_grp);
                }
            });
            self.ancestor.form.find(".modifiers_list").children().remove();
            // TODO: If there are existed ordermodifiers render them  as groups above;

        })(this);
    };

    OrderModifierForm.fn.showPreloader = function(){
        this.modal.find('.modifier-preloader').show();
    };

    OrderModifierForm.fn.hidePreloader = function(){
        this.modal.find('.modifier-preloader').hide();
    };

    OrderModifierForm.fn.showModal = function(){
        (function(self){
            self.modal.find('.modal-body').append(self.html_template);
            self.modal.modal('show');
            self.modal.on('hidden', function(e){
                if($(e.target).is($(this))){
                    self.html_template.detach();
                }
            })
        })(this);
    };

    OrderModifierForm.fn.addForm = function(data){
        data = data || {};
        (function(self){
            var form = self.order_modifier_template.clone();

            var modifier = new OrderModifier(data, form, self);
            self.modifiers.push(modifier);
            self.html_template.find('#attachment_section').append(form);
            modifier.save();
        })(this)
    };

    OrderModifierForm.fn.lookupModifiers = function(){
        (function(self){
            var modifiers_list = self.ancestor.form.find(".modifiers_list");
            modifiers_list.children().remove();
            if(self.modifiers.length){
                var ul = $("<ul class='well nav nav-stacked'></ul>");
                var active_modifiers = 0;
                $.each(self.modifiers, function(_i1, modifier){
                    if(!modifier.void_status){
                        active_modifiers++;
                        ul.append($('<li><a>'+ modifier.name +'<span class="pull-right label label-default"> $'+ modifier.data.price.toFixed(2) +'</span></a></li>'));
                    }
                });
                if (active_modifiers > 0) {
                    modifiers_list.append(ul);
                }
            }
        })(this);
    };

    var OrderItemForm = function(table_row, ancestor){
            this.form = $(table_row);
            this.fields = this.form.find('input, select');
            this.instance = this.form.find('input[name$="instance_id"]').val();
            this.processing = new $.Deferred();
            this.processing.resolve();  // Just to get into within first operation...
            this.remove_button = this.form.find('a.order-item-remove');
            this.add_modifier_button = this.form.find('a.order-item-modify');
            this.discount_button = this.form.find('a.add-discount');
            this.ancestor = ancestor;
            this.discount = null;
            this.modifierFormset = null;
            this.products_list = this.form.find('#products_list');
            this.chosen_product = null;
            this.initialize();
        };
        OrderItemForm.fn = OrderItemForm.prototype;
        OrderItemForm.fn.initialize = function(){
            (function(self){
                var liWithProducts = function(partial){
                    var res = $([]);
                    $.each(self.ancestor.products, function(i, prod){
                        prodname = prod.name;
                        if (prod.barcode && prod.barcode > 0)
                            prodname = prod.name+" - "+prod.barcode;
                        if(prodname.toLowerCase().indexOf(partial.toLowerCase()) !== -1){
                            var li = $('<li></li>');
                            li.append($("<a>"+prodname+"</a>"));
                            li.data(prod);
                            li.find('a').on('click', function(){
                                var data = $(this).parent().data();
                                self.chosen_product = data;
                                self.form.find("#id_product").val(data.id);
                                self.adjustPrice();
                                self.form.find("#id_cost").val(data.cost);

                                self.form.find("#id_name").val(data.name);
                                self.form.find("#id_name").blur();

                                self.form.find("a.add-modifier").remove();
                                if(data.modifier_groups && data.modifier_groups.length && data.modifier_groups.reduce(
                                    function(prev, curr){
                                        if(curr.archived) {
                                            return prev + 0;
                                        }
                                        return prev + curr.modifiers.reduce(function(prev, curr){
                                            return prev + ((curr.active && !curr.archived) ? 1 : 0);
                                        }, 0);
                                    }, 0)){
                                    var add_modifier = $("<a class='glyphicons show_big_thumbnails close add-modifier'><i></i></a>");
                                    add_modifier.insertBefore(self.form.find("#id_name"));
                                    var formset = self.modifierFormset;
                                    
                                    if(!formset || formset.product.id !== data.id){
                                        if(formset){
                                            $.each(formset.modifiers, function(_i1, m_form){
                                                m_form.form.find('.remove-modifier').trigger('click');
                                            });
                                        }

                                        self.modifierFormset = formset = new OrderModifierForm(data, self);
                                    }

                                    add_modifier.on('click', function(){
                                        formset.showModal();
                                    });

                                    formset.showModal();  // Customer request - honestly, IMHO it is not really convenient way...
                                } else {
                                    if(self.modifierFormset){
                                        $.each(self.modifierFormset.modifiers, function(_i1, m_form){
                                            m_form.form.find('.remove-modifier').trigger('click');
                                        });
                                        self.modifierFormset = null;
                                        self.form.find(".modifiers_list").children().remove();
                                    }
                                }
                                self.changeValue();
                            });
                            res = res.add(li);
                        }
                    });
                    return res;

                };

                $.each(self.fields, function(i, field){
                    if(field.id === "id_discount"){
                        $(field).on('keydown', function(){
                            $(this).data({key: true});
                        })
                    }
                    if(field.id === "id_name"){
                        var temp_name;
                        $(field).on('focus', function(){
                            temp_name = $(field).val();
                            self.products_list.show();
                            ul.html(liWithProducts($(field).val()));
                        });
                        $(field).on('blur', function(e){
                            if(!$(field).val()){
                                $(field).val(temp_name);
                            }
                            self.products_list.delay(200).fadeOut(300).promise(
                                self.products_list.hide
                            );
                        });

                        var navigate = {
                            down: function(){
                                var active = self.products_list.find("li.active");
                                var next = active.next();
                                self.products_list.find("li").removeClass("active");
                                if(!active.length || !next.length){
                                    self.products_list.find("li").first().addClass("active");
                                    return;
                                }
                                next.addClass("active");
                                return;
                            },
                            up: function(){
                                var active = self.products_list.find("li.active");
                                var prev = active.prev();
                                self.products_list.find("li").removeClass("active");
                                if(!active.length || !prev.length){
                                    self.products_list.find("li").last().addClass("active");
                                    return;
                                }
                                prev.addClass("active");
                                return;
                            },
                            tab: function(){
                                var active = self.products_list.find("li.active");
                                if(!active.length){
                                    active = self.products_list.find("li").first();
                                }
                                active.find('a').trigger('click');
                            },
                            submit: function(){
                                var active = self.products_list.find("li.active");
                                if(active.length){
                                    active.find('a').trigger('click');
                                }
                            }

                        };

                        $(field).on('keydown', function(e){
                            switch(e.keyCode){
                                case 38:
                                    //button up
                                    e.preventDefault();
                                    navigate.up();
                                break;
                                case 40:
                                    //button up
                                    e.preventDefault();
                                    navigate.down();
                                break;
                                case 9:
                                    //Tab button (to finish autocomplete)
                                    e.preventDefault();
                                    navigate.tab();
                                break;
                                case 13:
                                    //Enter button
                                    e.preventDefault();
                                    navigate.submit();
                                break;
                                case 27:
                                    $(this).blur();
                                break;
                            }
                        });
                        var ul = self.products_list.find("ul");
                        $(field).on('input propertychange paste', function(){
                            ul.html(liWithProducts($(field).val()));
                        });
                    }
                    $(field).on('change', function(){
                        if (this.id === "id_discount") {
                            if ($(this).data('key')) {
                                self.discount = null;
                                self.discount_button.next().find('.icon-ok').hide();
                            }
                            $(this).data({key: false});
                        }
                        if(this.id !== "id_name"){
                            self.changeValue();
                        }
                    });
                });



                self.discount_button.on('click', function(){
                    self.attachDiscounts();
                });
                self.remove_button.on('click', function(){
                    var void_status = self.form.find("#id_void_status");
                    if(!self.instance){
                        self.destroy();
                    } else if($(void_status).length){
                        $(void_status).val(1);
                        $(void_status).trigger('change');
                    }
                });
            })(this);

        };

        OrderItemForm.fn.attachDiscounts = function(){
            (function(self){
                var dropdown = self.discount_button.next();
                var showDiscounts = function(){
                    $.each(self.ancestor.order_form.discounts, function(i, discount){
                        if(!discount.archived){
                            dropdown.append(self.ancestor.order_form.generateDiscountRow(discount));
                        }
                    });

                    dropdown.find('li>a').on('click', function(e){
                        self.discount = $(this).data();
                        dropdown.find('.icon-ok').hide();
                        $(this).find('.icon-ok').show();
                        var field = self.form.find('#id_discount');
                        field.val(OrderForm.fn.calculateDiscount.call(self, '#id_discount', '#id_price'));
                        e.preventDefault();
                        self.changeValue();
                    });

                };
                if(!self.ancestor.order_form.discounts){
                    $.ajax({
                        url: '/terminalapi/sync/discount',
                        type: 'GET',
                        dataType: 'json',
                        success: function(data){
                            self.ancestor.order_form.discounts = data.results;
                            $('li.li-preloader').remove();
                            showDiscounts();
                        },
                        error: function(){
                            console.error("Failed to load discounts: ", arguments);
                        }
                    })
                } else if (dropdown.find('li.li-preloader').length || !dropdown.find('li').length ) {
                    $('li.li-preloader').remove();
                    showDiscounts();
                }
            })(this);
        };

        OrderItemForm.fn.serialize = function(){
            var result = {};
            $.each(this.fields, function(index, field){
                var name = $(field).attr('name');
                var value = $(field).val() + '';  // Let's make this string;
                if(name.indexOf("id_") === 0){  // Starts with id_
                    name = name.replace("id_", "");
                }
                result[name] = value;
            });
            return result;
        };

        OrderItemForm.fn.changeValue = function(){
            (function(self){
                self.form.find('#id_discount').val(OrderForm.fn.calculateDiscount.call(self, '#id_discount', '#id_price'));
                self.form.find('.price-label').text('$' + Number(self.form.find('#id_price').val()).toFixed(2));

                self.createOrUpdate(self.serialize(), function(data){
                    if(data && data.id && !self.instance){
                        self.instance = data.id;
                        self.form.find('#id_instance_id').val(data.id);
                    }
                    self.form.attr('class', 'success');
                    if(data.void_status){
                        self.destroy();
                    }
                    self.ancestor.data_manager.populate();
                    var subtotal = Number(self.form.find("#id_price").val());
                    if(self.modifierFormset){
                        subtotal += self.modifierFormset.modifiers.reduce(function(accum, m_form){
                            if(m_form.form.find("#id_void_status").val() != 'true'){
                                return accum + m_form.data.price;
                            }
                            return 0;
                        }, .0);
                        self.modifierFormset.lookupModifiers();
                    } else {
                        self.form.find(".modifiers_list").children().remove();
                    }
                    self.form.find('.item-subtotal').text("$" + (data.quantity * (subtotal - data.discount)).toFixed(2));   // TODO: Should discount to be multiplied too?
                });
            })(this);
        };

        OrderItemForm.fn.destroy = function(){
            (function(self){
                self.form.fadeOut(500).promise().done(self.form.remove);
                self.ancestor.forms = $.map(self.ancestor.forms, function(val, ind){
                    if(val !== self){
                        return [val];
                    }
                });
            })(this);
        };

        OrderItemForm.fn.adjustPrice = function(){
            if(this.chosen_product){
                (function(self){
                    var data = self.chosen_product;
                    var final_price = data.price;
                    if(self.ancestor.order_form.current_customer && data.special_prices.length){
                        for(var _i1 = 0; _i1 < data.special_prices.length; _i1 += 1){
                            if(data.special_prices[_i1].group.customers.indexOf(self.ancestor.order_form.current_customer) !== -1){
                                final_price = data.special_prices[_i1].price;
                                break;
                            }
                        }
                    }
                    self.form.find("#id_price").val(final_price);

                    var tax = 0.0;
                    if(data.tax_status === 0 && data.tax_rate_id){
                        var queried_tax = $.map(self.ancestor.taxrates, function(val, ind){
                            if(val.id === data.tax_rate_id){
                                return [val];
                            }
                        });
                        if(queried_tax.length){
                            tax = queried_tax[0].rate * final_price / 100.0;
                        }
                    }
                    self.form.find("#id_tax").val(tax.toFixed(2));
                })(this);
            }
        };

        OrderItemForm.fn.createOrUpdate = function(data, callback){
            (function(self){
                self.processing.done(function(){
                    self.processing = new $.Deferred();
                    var url='/terminalapi/', method;
                    if(self.instance){
                        url += 'update/order/item/' + self.instance;
                        method = 'PUT';
                    } else {
                        url += 'add/order/item';
                        method = 'POST';
                    }
                    self.form.attr('class', 'warning');
                    $.ajax({
                        url: url,
                        type: method,
                        data: JSON.stringify(data),
                        contentType: "application/json",
                        success: callback,
                        error: function(){
                            console.error('Error occurred while sending request to ' + url, arguments);
                            self.form.attr('class', 'error');
                        },
                        complete: function(){
                            self.processing.resolve();
                        }
                    });
                });
            })(this);
        };

    var OrderItemsFormset = function(html_fragment, options){
        options = options || {};
        html_fragment = $(html_fragment);
        this.ancor = $('#order-items-part');
        this.order_form = options.parent;
        this.formset = html_fragment.find('#order-items-formset');
        this.add_button = html_fragment.find('#add-order-item-btn');
        this.forms = [];
        this.FormFactory = OrderItemForm;
        this.data_manager = new FieldManager(
            this.forms,
            [this.order_form],
            ["#id_discount", "#id_tax", "#id_price"],
            ["#id_discount_total", "#id_tax_total", "#id_subtotal"],
            {
                fn: {
                    default: function(val, item){
                        val = parseFloat(Number(val).toFixed(5));
                        var qty = Number(item.form.find('#id_quantity').val());
                        return qty * val * (Number(item.form.find('#id_void_status').val()) ? 0 : 1) * (item.instance ? 1 : 0);
                    },
                    "#id_price": function(val, item){
                        val = Number(val);
                        if(item.modifierFormset){
                            for(var _key in item.modifierFormset.modifiers){
                                var modifier = item.modifierFormset.modifiers[_key];
                                if(modifier.form.find("#id_void_status").val() !== 'true'){
                                    val += Number(modifier.form.find("#id_price").val());
                                }
                            }
                        }

                        var qty = Number(item.form.find('#id_quantity').val());
                        var discount = Number(item.form.find('#id_discount').val());
                        val = qty * (val - discount) * (Number(item.form.find('#id_void_status').val()) ? 0 : 1);
                        return val;
                    }
                }
            }
        );
        this.products = [];
        this.taxrates = [];
        this.initialize(html_fragment);
    };
    OrderItemsFormset.fn = OrderItemsFormset.prototype;
    OrderItemsFormset.fn.initialize = function(html_fragment){
        var html_form_template = html_fragment.find("#order-item-template");
        var html_forms = html_fragment.find('tr[id^="order-item-"]:not(#order-item-template)');
        
        (function(self){$.each(
            html_forms,
            function(index, value){
                self.forms.push(new self.FormFactory(
                    $(value),
                    self
                ));
            }
        )})(this);
        this.addForm(html_form_template); // initialize carrying function;
        (function (self) {
            self.add_button.on('click', function () {
                self.formset.find('tbody').append(self.addForm());
            });
        })(this);
        this.ancor.append(html_fragment);
        (function (self) {
            $.ajax({
                url: "/terminalapi/sync/taxrates",
                type: 'GET',
                dataType: 'json',
                success: function (data) {
                    self.taxrates = data.results;
                    localStorage.setItem("taxrates", JSON.stringify(data.results));
                },
                error: function () {
                    self.taxrates = localStorage.getItem("taxrates") || [];
                }
            });
            $.ajax({
                url: "/terminalapi/sync/products/advanced",
                type: 'GET',
                dataType: 'json',
                success: function (data) {
                    self.products = data.results;
                    localStorage.setItem("products", JSON.stringify(data.results));
                },
                error: function () {
                    self.products = localStorage.getItem("products") || [];
                }
            });
        })(this);
    };

    OrderItemsFormset.fn.addForm = function(html_template){
        (function(self){
            self.addForm = function(){
                var form = $(html_template).clone();
                form.removeAttr('style');
                form.attr('id', 'order-item-' + self.forms.length);
                self.forms.push(new self.FormFactory(
                    form,
                    self
                ));
                return form;
            };
        })(this);
    };

    var PaymentHandler = function(order){
        this.payments = [];
        this.order = order || {};
        this.initialize();
    };

    PaymentHandler.fn = PaymentHandler.prototype;

    PaymentHandler.fn.initialize = function(){
        (function(self){
            self.button = $("<button class='btn btn-large btn-primary pull-right glyphicons shopping_cart large'><i></i>Checkout</button>");
            var loadTemplate = function(){
                return $.ajax({
                    url: '/order/add/payment',
                    type: "GET",
                    data: {order: self.order.instance},
                    success: function(data){
                        self.template = data;
                    },
                    error: function(){
                        console.error("Couldn't load template for payments:", arguments);
                    }
                });
            };
            self.account_payment = null;
            self.button.on('click', function(){
                var initializeForm = function(){
                    self.form = $(self.template + "");  // just to make copy.
                    self.lazyInit();
                    self.form.hide();
                    self.check_number = null;
                    $("#payment-part").append($(self.form));
                    // $(self.form).hide().appendTo("#payment-part").slideDown();
                    // $(self.form).hide().appendTo("#payment-part").delay(100).slideDown();
                    self.form.slideDown();
                    if (!self.order.current_customer) {
                        // not allow to pay by account if customer is not selected
                        $('.pay-with-account', '#payment-part').hide();
                    } else {
                        $('.pay-with-account', '#payment-part').show();
                    }
                    if (self.account_payment) {
                        // disable button if already have account payment
                        $('.pay-with-account', '#payment-part')
                            .addClass('pay-with-account-disabled').addClass('disabled')
                            .removeClass('pay-with-account')
                            // .data('toggle', 'tooltip')
                            .attr('title', 'Already paid by account')
                            // .tooltip('hide')
                            ;
                    }
                };


                if(!self.template){
                    loadTemplate().done(function(){
                        initializeForm();
                    });
                } else {
                    if(!self.form){
                        initializeForm();
                    } else {
                        if(self.form.css("display") === "none"){
                            self.form.slideDown();
                        } else {
                            self.form.slideUp();
                        }
                    }

                }
            });
            self.button.wrap("<div class='row-fluid'></div>").parent().appendTo($("#payment-part"))
        })(this);
    };

    PaymentHandler.fn.lazyInit = function(){
        (function(self){
            self.form.on("submit", function(e){
                e.preventDefault();
                e.stopPropagation();
                return false;
            });
            self.form.find("#id_amount").on('change', function(){
                $(this).val((Number(this.value) || 0.0).toFixed(2));
                var to_pay = Math.min(Number(this.value), Number(self.order.form.find("#id_balance_remaining").val()));
                var change_remaining = Math.max(Number(this.value) - to_pay, 0.0);
                self.form.find("#id_amount_paid").val(to_pay);
                self.form.find("#id_change_amount").val(change_remaining).trigger('change');
                self.form.find("#id-change-amount-label").text(change_remaining.toFixed(2));

            });

            self.form.find("#id_change_amount").on('change', function(){
                self.form.find("#id-change-amount-label").text(Number(this.value).toFixed(2));
            });

            self.form.find(".currency-btn").on('click', function(){
                var cur = Number($(this).data('value'));
                var amount_field = self.form.find("#id_amount");
                amount_field.val(Number(amount_field.val()) + cur);
                amount_field.trigger('change');
            });

            self.form.find("#id-pay-with-cash").on('click', function(){
                var amount_input = self.form.find("#id_amount")
                remaining = Number(self.order.form.find("#id_balance_remaining").val());
                if(!Number(amount_input.val())){
                    // if value is 0 - set the balance
                    amount_input.val(remaining).trigger('change');
                }
                if(Number(amount_input.val())){
                    self.button.hide("slide", {direction: "right"});
                    self.form.hide("slide", {direction: "left" }).promise().done(function(){
                        $("#id-processing-panel").show("slide", {direction: "right"});
                    });
                    self.payWithCash();
                } else {
                    amount_input.effect( "shake" );
                }
            });
            self.form.find(".pay-with-account").on('click', function(){
                var amount_input = self.form.find("#id_amount");
                if (!self.account_payment) {
                    self.button.hide("slide", {direction: "right"});
                    self.form.hide("slide", {direction: "left" }).promise().done(function(){
                        $("#id-processing-panel").show("slide", {direction: "right"});
                    });
                    self.payWithAccount();
                } else {
                    $(this).effect( "shake" );
                }
            });
            self.form.find(".pay-with-check").on('click', function(){
                var amount_input = self.form.find("#id_amount");
                remaining = Number(self.order.form.find("#id_balance_remaining").val());
                if(!Number(amount_input.val())){
                    // if value is 0 - set the balance
                    amount_input.val(remaining).trigger('change');
                }
                var modaltpl = $('.checkpay-modal');
                $('.text-error', '.checkpay-modal').html('');
                $('.pay-amount', '.checkpay-modal').html(amount_input.val());
                self.check_number = null;
                modaltpl.modal('show');
                // if (true) {
                //     self.button.hide("slide", {direction: "right"});
                //     self.form.hide("slide", {direction: "left" }).promise().done(function(){
                //         $("#id-processing-panel").show("slide", {direction: "right"});
                //         self.payWithCheck();
                //     });
                // } else {
                //     $(this).effect( "shake" );
                // }
            });
            self.form.find(".checkpay-btn").on('click', function(){
                self.check_number = $(this).closest('.checkpay-modal').find('input.check-no').val();
                if (self.check_number && self.check_number.toString().length > 5) {
                    $('.checkpay-modal').modal('hide');
                    self.button.hide("slide", {direction: "right"});
                    self.form.hide("slide", {direction: "left" }).promise().done(function(){
                        $("#id-processing-panel").show("slide", {direction: "right"});
                    });
                    self.payWithCheck();
                } else {
                    $('.text-error', '.checkpay-modal').html('Invalid check number!');
                }
            });
            self.form.find("#id-pay-with-credit").tooltip({container: "body"});  // TODO: Turn on later...
        })(this);
    };

    PaymentHandler.fn.serialize = function(){
        return this.form.serializeObject();
    };

    PaymentHandler.fn.payWithCash = function(){
        (function(self){
            self.form.find(".payment-error").remove();
            self.form.find("#id_payment_type").val("Cash");
            self.form.find("#id_payment_form").val("CASH");
            self.form.find("#id_processor_response").val("APPROVAL");
            self.addPayment().done(function(data){
                self.form.remove();
                self.form = null;
                $("#id-processing-panel").hide("slide", {direction: "left"}).promise().done(function(){
                    var success_label = $('<div class="well"><h3 style="text-align: center;" class="alert-success well">Payment has been apporved.</h3></div>');
                    var removeLabel = function(){
                        if(success_label){
                            success_label.hide("slide", {direction: "left"}).promise().done(function(){
                                success_label.remove();
                                success_label = null;
                                self.button.show("slide", {direction: "right"});
                            });
                        }
                    };
                    success_label.on('click', removeLabel);
                    success_label.insertAfter($("#id-processing-panel"));
                    success_label.show("slide", {direction: "right"});
                    self.order.changeValue();
                    setTimeout(removeLabel, 2000);
                    remaining = Number(self.order.form.find("#id_balance_remaining").val());
                    if (remaining <= 0) {
                        window.location = "/orders";
                    }
                });
            }).fail(function(){
                $("#id-processing-panel").hide("slide", {direction: "right"}).promise().done(function(){
                    self.button.show("slide", {direction: "right"});
                    self.form.show("slide", {direction: "left" });
                    self.form.append($("<div class='alert alert-primary well payment-error'> Server failed to process request.<br/>Please, try again later. </div>"))
                });
            })
        })(this);
    };

    PaymentHandler.fn.payWithCheck = function(){
        (function(self){
            self.form.find(".payment-error").remove();
            self.form.find("#id_payment_type").val("Check");
            self.form.find("#id_payment_form").val("CHECK");
            self.form.find("#id_processor_response").val("APPROVAL");
            // newdata = {amount: 0.0, amount_paid: 0.0, tips: 0.0, change_amount: 0.0};
            var newdata = {check_number: self.check_number};
            self.addPayment(newdata).done(function(data){
                self.form.remove();
                self.form = null;
                $("#id-processing-panel").hide("slide", {direction: "left"}).promise().done(function(){
                    var success_label = $('<div class="well"><h3 style="text-align: center;" class="alert-success well">Payment has been apporved.</h3></div>');
                    var removeLabel = function(){
                        if(success_label){
                            success_label.hide("slide", {direction: "left"}).promise().done(function(){
                                success_label.remove();
                                success_label = null;
                                self.button.show("slide", {direction: "right"});
                            });
                        }
                    };
                    success_label.on('click', removeLabel);
                    success_label.insertAfter($("#id-processing-panel"));
                    success_label.show("slide", {direction: "right"});
                    self.order.changeValue();
                    setTimeout(removeLabel, 2000);
                    remaining = Number(self.order.form.find("#id_balance_remaining").val());
                    if (remaining <= 0) {
                        window.location = "/orders";
                    }
                });
            }).fail(function(){
                $("#id-processing-panel").hide("slide", {direction: "right"}).promise().done(function(){
                    self.button.show("slide", {direction: "right"});
                    self.form.show("slide", {direction: "left" });
                    self.form.append($("<div class='alert alert-primary well payment-error'> Server failed to process request.<br/>Please, try again later. </div>"))
                });
            })
        })(this);
    };

    PaymentHandler.fn.payWithAccount = function(){
        (function(self){
            self.form.find(".payment-error").remove();
            self.form.find("#id_payment_type").val("Account");
            self.form.find("#id_payment_form").val("ACCOUNT");
            self.form.find("#id_processor_response").val("ACCOUNT");
            var newdata = {amount: 0.0, amount_paid: 0.0, tips: 0.0, change_amount: 0.0};
            self.addPayment(newdata).done(function(data){
                self.account_payment = true;
                self.form.remove();
                self.form = null;
                $("#id-processing-panel").hide("slide", {direction: "left"}).promise().done(function(){
                    var success_label = $('<div class="well"><h3 style="text-align: center;" class="alert-success well">Payment has been apporved.</h3></div>');
                    var removeLabel = function(){
                        if(success_label){
                            success_label.hide("slide", {direction: "left"}).promise().done(function(){
                                success_label.remove();
                                success_label = null;
                                self.button.show("slide", {direction: "right"});
                            });
                        }
                    };
                    success_label.on('click', removeLabel);
                    success_label.insertAfter($("#id-processing-panel"));
                    success_label.show("slide", {direction: "right"});
                    self.order.changeValue();
                    setTimeout(removeLabel, 2000);
                    self.order.hold_button.trigger('click');
                    window.location = "/orders";
                });
            }).fail(function(){
                $("#id-processing-panel").hide("slide", {direction: "right"}).promise().done(function(){
                    self.button.show("slide", {direction: "right"});
                    self.form.show("slide", {direction: "left" });
                    self.form.append($("<div class='alert alert-primary well payment-error'> Server failed to process request.<br/>Please, try again later. </div>"))
                });
            })
        })(this);
    };

    PaymentHandler.fn.addPayment = function(newdata){
        var self = this;  // not a good way ... change on closure.
        var data = self.serialize();
        data.payment_date = (new Date()).toISOString();
        data["terminal_id"]="-1";
        data.transaction_type = 1;
        for(var field in data){
            if(data[field] === null || data[field] == undefined || (data[field].length !== undefined && data[field].length === 0)){
                delete data[field];
            }
        }
        if (newdata) {
            // Override some values if needed
            for (var field in newdata) {
                data[field] = newdata[field];
            }
        }
        return $.ajax({
            url: "/terminalapi/add/payments",
            data: JSON.stringify(data),
            type: "POST",
            contentType: "application/json",
            success: function(data){
                self.payments.push(data);
                self.order.recalculate();
            },
            error: function(){
                console.error("Transaction aborted: ", arguments);
            }
        });
    };

    PaymentHandler.fn.refundAll = function(){
        var promise = new $.Deferred();
        var payments = Array.prototype.slice.call(this.payments);
        (function(self){
            var recursiveCallback = function(){
                var payment = payments.shift();
                if(!payment){
                    self.payments = [];
                    promise.resolve();
                    return null;
                }
                payment.transaction_type = 3;  // Return;
                return $.ajax({
                    url: "/terminalapi/update/payments/" + payment.id,
                    type: "PUT",
                    contentType: "application/json",
                    success: recursiveCallback,
                    data: JSON.stringify(payment),
                    error: function(){
                        console.error("Failed to refund payment!: ", arguments);
                        promise.reject();
                    }
                });
            };
            recursiveCallback();
        })(this);
        return promise;
    };

    var form = new OrderForm();

    form.changeValue(true);  // Initial saving.

})(jQuery, window.document);
