<%from clld_markdown_plugin import markdown%>
<%import re%>
<link rel="stylesheet" href="${req.static_url('clld_document_plugin:static/clld-slides.css')}"/>

<style>
#top {
    position: fixed;
    width: 100%;
}
#buffer {
    min-height: 40px
}
</style>


<div class="slides-wrapper">

<div class="slides-nav">
<button class="btn btn-light previous">←</button>
<button class="btn btn-light next">→</button>
</div>

<% tent = "\n" + ctx.description %>
<% delim = "\n## " %>
<% parts = tent.split(delim)[1::] %>

<div id="title" class = "slide active">
<div class="slide-title"></div>
    <div class="slide-content">
        <h1 class="title">${ctx.name}</h1>

% if ctx.meta_data:
<ul class="metadata">
    % for k, v in ctx.meta_data.items():
        <li>${v}</li>
    % endfor
</ul>
%endif

    </div>
</div>

% for (i, part) in enumerate(parts):
    <% title, content = part.split("\n", 1) %>
    <% tag = re.findall("{#(.*?)}", title) %>
    <% title = title.split("{#")[0].strip() %>
    % if len(tag) == 0:
        <% tag = f"slide-{i}" %>
    % else:
        <% tag = tag[0] %>
    % endif
    <div id="${tag}" class="slide"><div class="slide-title"><h2>${title}</h2></div><div class="slide-content">${markdown(request, content)|n}</div></div>


% endfor

</div>

<script src="${req.static_url('clld_document_plugin:static/clld-slides.js')}"></script>
