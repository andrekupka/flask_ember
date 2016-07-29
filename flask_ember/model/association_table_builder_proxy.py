class AssociationTableBuilderProxy:
    def __init__(self, table):
        self.table = table

    def add_column(self, column):
        self.table.append_column(column)

    def add_constraint(self, constraint):
        self.table.append_constraint(constraint)
