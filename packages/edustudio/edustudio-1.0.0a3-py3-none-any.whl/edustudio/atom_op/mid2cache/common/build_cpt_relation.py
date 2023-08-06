from .base_mid2cache import BaseMid2Cache

class M2C_BuildCptRelation(BaseMid2Cache):
    default_cfg = {
        'relation_type': 'rcd_transition',
        'threshold': 0.5
    }

    def process(self, **kwargs):
        pass

