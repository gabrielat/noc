//---------------------------------------------------------------------
// ip.ipam.prefix form
//---------------------------------------------------------------------
// Copyright (C) 2007-2019 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.ip.ipam.view.forms.prefix.PrefixAddressListsController");

Ext.define("NOC.ip.ipam.view.forms.prefix.PrefixAddressListsController", {
    extend: "Ext.app.ViewController",
    alias: "controller.ip.ipam.list.prefixAddress",
    onShowFreePrefixes: function(button) {
        this.showFree(button, "prefix", this.filterByFree);
    },
    onShowFreeAddresses: function(button) {
        this.showFree(button, "address", this.filterByFree);
    },
    onBookmarkToggle: function(view, rowIndex, colIndex, item, e, record) {
        Ext.Ajax.request({
            url: "/ip/ipam/" + record.id + "/toggle_bookmark/",
            method: "GET",
            success: function(response) {
                var result = Ext.decode(response.responseText);
                record.set("has_bookmark", result.has_bookmark);
            }
        });
    },
    onEditPrefix: function(view, rowIndex, colIndex, item, e, record) {
        if(record.get("isFree")) {
            this.fireViewEvent("ipIPAMPrefixFormNew", {prefix: record.get("name")});
        } else {
            this.fireViewEvent("ipIPAMPrefixFormEdit", {id: record.id});
        }
    },
    onViewPrefixContents: function(view, record, item, idx, evt) {
        this.fireViewEvent("ipIPAMViewPrefixContents", {id: record.id});
    },
    onOpenCard: function(view, rowIndex, colIndex, item, e, record) {
        window.open("/api/card/view/prefix/" + record.id + "/");
    },
    onViewAddresses: function(view, record, item, idx, evt) {
        if(evt.getTarget(".address-view")) {
            if(record.get("isFree")) {
                this.fireViewEvent("ipIPAMAddressFormNew", {address: record.get("address")});
            } else {
                this.fireViewEvent("ipIPAMAddressFormEdit", {id: record.id});
            }
        }
    },
    onVRFListOpen: function() {
        this.fireViewEvent("ipIPAMVRFListOpen");
    },
    onNavigationClick: function(event, el) {
        var id = el.className.replace("breadcrumb nav-", "");
        this.fireViewEvent("ipIPAMViewPrefixContents", {id: id});
    },
    onSelectBookmark: function(combo, record) {
        this.fireViewEvent("ipIPAMViewPrefixContents", {id: record.id});
    },
    onQuickJump: function(field, key) {
        if(key.getKey() === Ext.EventObject.ENTER) {
            var vrf_id = this.getViewModel().get("prefix.vrf"),
                afi = this.getViewModel().get("prefix.afi");
            Ext.Ajax.request({
                url: "/ip/ipam/" + vrf_id + "/" + afi + "/quickjump/",
                method: "POST",
                scope: this,
                jsonData: {
                    jump: field.getValue()
                },
                success: function(response) {
                    var result = Ext.decode(response.responseText);
                    this.fireViewEvent("ipIPAMViewPrefixContents", {id: result.id});
                },
                failure: function(r) {
                    var msg = r.responseText || r.statusText;
                    NOC.error(msg);
                }
            });
        }
    },
    showFree: function(button, name, filter) {
        var store = this.getView().down("[itemId=ipam-" + name + "-grid]").getStore();
        var me = this;
        button.setDisabled(true);
        console.log(true);
        var task = new Ext.util.DelayedTask(function() {
            button.setDisabled(false)
        }, me);
        task.delay(2000);
        // var task = Ext.TaskManager.start({
        //     run: function(){
        //         // button.setDisabled(false);
        //         console.log(false);
        //     },
        //     interval: 2000,
        //     repeat: 1
        // });
        // if(store.isFiltered()) {
        //     button.setText(__("Hide Free") + " " + __(Ext.String.capitalize(name)));
        //     store.clearFilter();
        // } else {
        //     button.setText(__("Show Free") + " " + __(Ext.String.capitalize(name)));
        //     store.addFilter(filter);
        // }
        // button.setDisabled(false);
        // console.log(false);
    },
    filterByFree: function(record) {
        return !record.data.isFree;
    }
});
