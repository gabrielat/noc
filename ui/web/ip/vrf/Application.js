//---------------------------------------------------------------------
// ip.vrf application
//---------------------------------------------------------------------
// Copyright (C) 2007-2018 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.ip.vrf.Application");

Ext.define("NOC.ip.vrf.Application", {
    extend: "NOC.core.ModelApplication",
    requires: [
        "NOC.sa.administrativedomain.TreeCombo",
        "NOC.ip.vrf.Model",
        "NOC.ip.vrfgroup.LookupField",
        "NOC.vc.vpnprofile.LookupField",
        "NOC.main.resourcestate.LookupField",
        "NOC.project.project.LookupField",
        "NOC.main.user.LookupField",
        "NOC.main.group.LookupField"
    ],
    model: "NOC.ip.vrf.Model",
    search: true,
    rowClassField: "row_class",

    initComponent: function () {
        var me = this;

        me.cardButton = Ext.create("Ext.button.Button", {
            text: __("Card"),
            glyph: NOC.glyph.eye,
            scope: me,
            handler: me.onCard
        });

        Ext.apply(me, {
            columns: [
                {
                    text: __("Name"),
                    dataIndex: "name"
                },
                {
                    text: __("State"),
                    dataIndex: "state",
                    renderer: NOC.render.Lookup("state")
                },
                {
                    text: __("Group"),
                    dataIndex: "vrf_group",
                    renderer: NOC.render.Lookup("vrf_group")
                },
                {
                    text: __("Profile"),
                    dataIndex: "profile",
                    renderer: NOC.render.Lookup("profile")
                },
                {
                    text: __("Project"),
                    dataIndex: "project",
                    renderer: NOC.render.Lookup("project")
                },
                {
                    text: __("RD"),
                    dataIndex: "rd",
                    width: 100
                },
                {
                    text: __("VPN ID"),
                    dataIndex: "vpn_id",
                    width: 100
                },
                {
                    text: __("IPv4"),
                    dataIndex: "afi_ipv4",
                    renderer: NOC.render.Bool,
                    width: 50
                },
                {
                    text: __("IPv6"),
                    dataIndex: "afi_ipv6",
                    renderer: NOC.render.Bool,
                    width: 50
                },
                {
                    text: __("Description"),
                    dataIndex: "description",
                    flex: 1
                },
                {
                    text: __("Tags"),
                    dataIndex: "tags",
                    renderer: NOC.render.Tags
                }
            ],
            fields: [
                {
                    name: "name",
                    xtype: "textfield",
                    fieldLabel: __("VRF"),
                    allowBlank: false,
                    uiStyle: "medium"
                },
                {
                    name: "profile",
                    xtype: "vc.vpnprofile.LookupField",
                    fieldLabel: __("Profile"),
                    allowBlank: false,
                    uiStyle: "medium"
                },
                {
                    name: "vrf_group",
                    xtype: "ip.vrfgroup.LookupField",
                    fieldLabel: __("VRF Group"),
                    allowBlank: true
                },
               Ext.create('NOC.sa.administrativedomain.TreeCombo', {
                    name: "administrative_domain",
                    fieldLabel: __("Adm. Domain"),
                    allowBlank: true,
                    emptyText: __("Select adm domain..."),
                    labelAlign: "left",
                    labelWidth: 100,
                    listWidth: 1,
                    margin: '0 0 5'
                }),
                {
                    name: "description",
                    xtype: "textarea",
                    fieldLabel: __("Description"),
                    allowBlank: true
                },
                {
                    name: "state",
                    xtype: "statefield",
                    fieldLabel: __("State"),
                    allowBlank: false
                },
                {
                    name: "project",
                    xtype: "project.project.LookupField",
                    fieldLabel: __("Project"),
                    allowBlank: true
                },
                {
                    name: "rd",
                    xtype: "textfield",
                    fieldLabel: __("RD"),
                    allowBlank: true,
                    uiStyle: "medium"
                },
                {
                    name: "vpn_id",
                    xtype: "textfield",
                    fieldLabel: __("VPN ID"),
                    allowBlank: true,
                    uiStyle: "medium"
                },
                {
                    name: "afi_ipv4",
                    xtype: "checkboxfield",
                    boxLabel: __("IPv4"),
                    allowBlank: false
                },
                {
                    name: "afi_ipv6",
                    xtype: "checkboxfield",
                    boxLabel: __("IPv6"),
                    allowBlank: false
                },
                {
                    name: "tt",
                    xtype: "textfield",
                    regexText: /^\d*$/,
                    fieldLabel: __("TT"),
                    allowBlank: true
                },
                {
                    name: "tags",
                    xtype: "tagsfield",
                    fieldLabel: __("Tags"),
                    allowBlank: true
                },
                {
                    name: "allocated_till",
                    xtype: "datefield",
                    startDay: 1,
                    fieldLabel: __("Allocated till"),
                    allowBlank: true
                },
                {
                    name: "direct_permissions",
                    xtype: "gridfield",
                    fieldLabel: __("Permissions"),
                    columns: [
                        {
                            text: __("User"),
                            dataIndex: "user",
                            editor: "main.user.LookupField",
                            renderer: NOC.render.Lookup("user"),
                            width: 100
                        },
                        {
                            text: __("Group"),
                            dataIndex: "group",
                            editor: "main.group.LookupField",
                            renderer: NOC.render.Lookup("group"),
                            width: 150
                        },
                        {
                            text: __("Permission"),
                            dataIndex: "permission",
                            editor: {
                                xtype: "combobox",
                                store: [
                                    ["can_view", "can_view"],
                                    ["can_change", "can_change"],
                                    ["can_create", "can_create"],
                                    ["can_delete", "can_delete"]
                                ]
                            },
                            width: 150
                        }
                    ]
                }
            ],
            formToolbar: [
                me.cardButton
            ]
        });
        me.callParent();
    },
    //
    filters: [
        {
            title: __("By State"),
            name: "state",
            ftype: "lookup",
            lookup: "main.resourcestate"
        },
        {
            title: __("By VRF Group"),
            name: "vrf_group",
            ftype: "lookup",
            lookup: "ip.vrfgroup"
        },
        {
            title: __("By Project"),
            name: "project",
            ftype: "lookup",
            lookup: "project.project"
        },
        {
            title: __("By IPv4"),
            name: "afi_ipv4",
            ftype: "boolean"
        },
        {
            title: __("By IPv6"),
            name: "afi_ipv6",
            ftype: "boolean"
        }
    ],
    //
    onCard: function() {
        var me = this;
        if(me.currentRecord) {
            window.open(
                "/api/card/view/vrf/" + me.currentRecord.get("id") + "/"
            );
        }
    }
});
