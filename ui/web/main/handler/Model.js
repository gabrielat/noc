//---------------------------------------------------------------------
// main.handler Model
//---------------------------------------------------------------------
// Copyright (C) 2007-2019 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.main.handler.Model");

Ext.define("NOC.main.handler.Model", {
    extend: "Ext.data.Model",
    rest_url: "/main/handler/",

    fields: [
        {
            name: "id",
            type: "string"
        },
        {
            name: "handler",
            type: "string"
        },
        {
            name: "name",
            type: "string"
        },
        {
            name: "description",
            type: "string"
        },
        {
            name: "allow_config_filter",
            type: "boolean"
        },
        {
            name: "allow_config_validation",
            type: "boolean"
        },
        {
            name: "allow_config_diff",
            type: "boolean"
        },
        {
            name: "allow_config_diff_filter",
            type: "boolean"
        },
        {
            name: "allow_housekeeping",
            type: "boolean"
        },
        {
            name: "allow_resolver",
            type: "boolean"
        },
        {
            name: "allow_threshold",
            type: "boolean"
        }
    ]
});
