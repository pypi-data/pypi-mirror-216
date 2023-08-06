<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "documents" %>

<link rel="stylesheet" href="${req.static_url('clld_document_plugin:static/clld-document.css')}"/>

% if ctx.kind == "slides":
<%include file="slides.mako"/>
% elif ctx.kind == "chapter":
<%include file="chapter.mako"/>
%endif
