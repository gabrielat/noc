//---------------------------------------------------------------------
// sa.administrativedomain application
//---------------------------------------------------------------------
// Copyright (C) 2007-2017 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.sa.administrativedomain.Application");

Ext.define("NOC.sa.administrativedomain.Application", {
    extend: "NOC.core.ModelApplication",
    requires: [
        "NOC.core.TagsField",
        "NOC.core.combotree.ComboTree",
        "NOC.sa.administrativedomain.Model",
        "NOC.main.pool.LookupField",
        "NOC.main.remotesystem.LookupField"
    ],
    model: "NOC.sa.administrativedomain.Model",
    search: true,
    helpId: "reference-administrative-domain",
    columns: [
        {
            text: __("Name"),
            dataIndex: "name",
            width: 150
        },
        {
            text: __("Parent"),
            dataIndex: "parent",
            renderer: NOC.render.Lookup("parent"),
            width: 150,
            hidden: true
        },
        {
            text: __("Pool"),
            dataIndex: "default_pool",
            renderer: NOC.render.Lookup("default_pool"),
            width: 150
        },
        {
            text: __("Objects"),
            dataIndex: "object_count",
            width: 50,
            align: "right",
            sortable: false
        },
        {
            text: __("Description"),
            dataIndex: "description",
            flex: true
        }
    ],
    fields: [
        {
            name: "name",
            xtype: "textfield",
            fieldLabel: __("Name"),
            allowBlank: false
        },
        {
            xtype: "noc.core.combotree",
            restUrl: "/sa/administrativedomain/",
            name: "parent",
            fieldLabel: __("Parent"),
            allowBlank: true
        },
        {
            name: "description",
            xtype: "textfield",
            fieldLabel: __("Description"),
            allowBlank: true
        },
        {
            name: "default_pool",
            xtype: "main.pool.LookupField",
            fieldLabel: __("Pool"),
            allowBlank: true
        },
        {
            xtype: "fieldset",
            layout: "hbox",
            title: __("Integration"),
            defaults: {
                padding: 4,
                labelAlign: "right"
            },
            items: [
                {
                    name: "remote_system",
                    xtype: "main.remotesystem.LookupField",
                    fieldLabel: __("Remote System"),
                    allowBlank: true
                },
                {
                    name: "remote_id",
                    xtype: "textfield",
                    fieldLabel: __("Remote ID"),
                    allowBlank: true,
                    uiStyle: "medium"
                },
                {
                    name: "bi_id",
                    xtype: "displayfield",
                    fieldLabel: __("BI ID"),
                    allowBlank: true,
                    uiStyle: "medium"
                }
            ]
        },
        {
            name: "tags",
            xtype: "tagsfield",
            fieldLabel: __("Tags"),
            allowBlank: true,
            uiStyle: "extra"
        }
    ],

    filters: [
        {
            title: __("By Adm. Domain"),
            name: "parent",
            ftype: "tree",
            lookup: "sa.administrativedomain"
        }
    ],
    levelFilter: {
        icon: NOC.glyph.level_down,
        color: NOC.colors.level_down,
        filter: 'parent',
        tooltip: __('Parent filter')
    }
});
