from simuran.base_class import BaseSimuran


class SingleUnit(BaseSimuran):

    def __init__(self):
        super().__init__()

    def load(self, *args, **kwargs):
        super().load()
        # TODO pass clustering also so NC only load if there is cluster.
        self.underlying = self.loader.load_single_unit(
            self.source_file["Spike"], self.source_file["Clusters"], **kwargs)
