var httpRequest = new XMLHttpRequest();
httpRequest.open("GET", "/main/desktop/settings/", false);
httpRequest.send();
if (httpRequest.status === 200) {
    var setup = JSON.parse(httpRequest.responseText);
    console.log("!!!");
    console.log("!!! Running NOC desktop");
    console.log("!!!");
    // Initialize loader
    Ext.BLANK_IMAGE_URL = "/ui/web/img/s.gif";
    // Ext.namespace("NOC");
    NOC = {};
    NOC.settings = {
        systemId: setup.system_uuid ? setup.system_uuid : null,
        brand: setup.brand,
        installation_name: setup.installation_name,
        preview_theme: setup.preview_theme,
        language: setup.language,
        logo_url: setup.logo_url,
        logo_width: setup.logo_width,
        logo_height: setup.logo_height,
        branding_color: setup.branding_color,
        branding_background_color: setup.branding_background_color,
        enable_search: setup.enable_search,
        gitlab_url: setup.gitlab_url,
        collections: {
            allow_sharing: setup.collections.allow_sharing,
            project_id: setup.collections.project_id
        },
        gis: {
            base: {
                "enable_osm": setup.gis.base.enable_osm,
                "enable_google_sat": setup.gis.base.enable_google_sat,
                "enable_google_roadmap": setup.gis.base.enable_google_roadmap
            }
        },
        traceExtJSEvents: setup.traceExtJSEvents,
        helpUrl: setup.helpUrl,
        helpBranch: setup.helpBranch,
        helpLanguage: setup.helpLanguage,
        timezone: setup.timezone,
        enable_remote_system_last_extract_info: setup.enable_remote_system_last_extract_info,
        enableHelp: setup.helpUrl && setup.helpUrl !== "",
    };
    NOC.templates = {};
}
