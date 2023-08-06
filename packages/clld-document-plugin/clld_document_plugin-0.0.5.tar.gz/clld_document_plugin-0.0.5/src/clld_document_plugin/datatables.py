from clld.web.datatables.base import Col
from clld.web.datatables.base import DataTable
from clld.web.datatables.base import LinkCol


class Documents(DataTable):
    def col_defs(self):
        return [LinkCol(self, "order")]


class Topics(DataTable):
    def col_defs(self):
        return [
            LinkCol(self, "name"),
            Col(self, "description"),
        ]
