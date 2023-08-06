<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "topics" %>

<link rel="stylesheet" href="${req.static_url('clld_document_plugin:static/clld-document.css')}"/>

<table class="table table-nonfluid">
    <tbody>
        <tr>
            <td>Topic:</td>
            <td><b>${ctx.name}</b></td>
        </tr>

% if ctx.references:
        <tr>
            <td>Discussed in:</td>
        <td><ul>
            % for ref in ctx.references:
                <li><a href='/documents/${ref.document.id}#${ref.section}' name='$' >${ref.label}</a</li>
            % endfor
        </ul></td>
        </tr>
% endif

   </tbody>
</table>


        % if ctx.description:
Description: ${ctx.description}
        % endif


