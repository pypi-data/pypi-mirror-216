<%from clld_markdown_plugin import markdown%>
<link rel="stylesheet" href="${req.static_url('clld_document_plugin:static/clld-chapter.css')}"/>

<style>
#top {
    position: fixed;
    width: 100%;
}
#buffer {
    min-height: 40px
}
</style>

<div id="buffer">
</div>


% if ctx.chapter_no:
    <% no_str = f" number={ctx.chapter_no}"%>
% else:
    <% no_str = ""%>
% endif

<article class="span7">
<h1${no_str}>${ctx.name}</h1>

${markdown(request, ctx.description)|n}


</article>


<div id="docnav" class="span4">
    <div id="toc" class="well well-small">
    </div>
    <div class="pagination">
        <ul>
            % if ctx.preceding:
                <li><a class="page-link" href="${request.resource_url(ctx.preceding)}">←${ctx.preceding}</a></li>
            % endif
            % if ctx.following:
                <li><a class="page-link" href="${request.resource_url(ctx.following[0])}">${ctx.following[0]}→</a></li>
            % endif
        </ul>
    </div>
</div>


<script src="${req.static_url('clld_document_plugin:static/clld-document.js')}">
</script>
<script>
    numberSections()
    numberExamples()
    numberCaptions()
    resolveCrossrefs()
</script>
