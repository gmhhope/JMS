'''
A place to store some prototype or experimental code, 
which may be garbage or useful in someway elsewhere.
'''

# obsolete; should use khipu
dev_common_adducts = {
    # mass diff, modification
    # not using (intensity ratio constraint), but it can be documented or learned
    'pos': [
        (1.0078, 'H'),
        (21.9820, 'Na/H'), # Na replacing H
        (10.991, 'Na/H, double charged'),
        (18.0106, '+H2O'), 
        (18.033823, '+NH4'),
        (37.9559, '39K/H'),
        (39.9540, '41K/H'),
        (41.026549, 'Acetonitrile'),
    ],
    'neg': [
        (1.0078, 'H'),
        (22.9893, 'Na'),
        (20.97474706646, '+Na-2H'),
        (18.0106, 'H2O'), 
        (34.9689, '35Cl'),
        (36.9659, '37Cl'),
        (40.01926853323, '+ACN-H'),
        (44.998201, 'COOH'),
        (59.013295, 'CH3COO'),
    ],
}

# obsolete; should use khipu
dev_seed_empCpd_patterns = {
    'pos': [(1.003355, '13C/12C', (0, 0.8)), (1.0078, 'H'), (21.9820, 'Na/H'), ],
    'neg': [(1.003355, '13C/12C', (0, 0.8)), (1.0078, 'H'), (20.97474706646, '+Na-2H'), (34.9689, '35Cl')],
}


#----------------------------------------------------------------------------------------
class empiricalCompound:
    '''
    Simple class, following exampe in metDataModel.
    A template is:
            {
            "neutral_formula_mass": 268.08077, 
            "neutral_formula": C10H12N4O5,
            "alternative_formulas": [],
            "interim_id": C10H12N4O5_268.08077,
            "identity": [
                    {'compounds': ['HMDB0000195'], 'names': ['Inosine'], 'score': 0.6, 'probability': null},
                    {'compounds': ['HMDB0000195', 'HMDB0000481'], 'names': ['Inosine', 'Allopurinol riboside'], 'score': 0.1, 'probability': null},
                    {'compounds': ['HMDB0000481'], 'names': ['Allopurinol riboside'], 'score': 0.1, 'probability': null},
                    {'compounds': ['HMDB0003040''], 'names': ['Arabinosylhypoxanthine'], 'score': 0.05, 'probability': null},
                    ],
            "MS1_pseudo_Spectra": [
                    {'id_number': 'FT1705', 'mz': 269.0878, 'rtime': 99.90, 'charged_formula': '', 'ion_relation': 'M+H[1+]'},
                    {'id_number': 'FT1876', 'mz': 291.0697, 'rtime': 99.53, 'charged_formula': '', 'ion_relation': 'M+Na[1+]'},
                    {'id_number': 'FT1721', 'mz': 270.0912, 'rtime': 99.91, 'charged_formula': '', 'ion_relation': 'M(C13)+H[1+]'},
                    {'id_number': 'FT1993', 'mz': 307.0436, 'rtime': 99.79, 'charged_formula': '', 'ion_relation': 'M+K[1+]'},
                    ],
            "MS2_Spectra": ['AZ0000711', 'AZ0002101'],
            "Database_referred": ["Azimuth", "HMDB", "MONA"],
            }
    '''
    def __init__(self):
        self.id = id                            # e.g. 'E00001234'
        self.interim_id = ''
        self.neutral_formula_mass = None
        self.neutral_formula = ''
        self.charged_formula = ''
        self.charge = None
        self.Database_referred = []
        self.MS1_pseudo_Spectra = []            # list of features that belong to this empCpd
        self.MS2_Spectra = []                   # MS2 identifiers can be universal (e.g. hashed ids)
        self.identity = self.annotation = []    # see desired serialize() output; also in README

    def read_json_model(self, jmodel):
        self.interim_id = jmodel['interim_id']
        self.neutral_formula_mass = jmodel['neutral_formula_mass'] = jmodel['neutral_mono_mass']
        self.neutral_formula = jmodel['neutral_formula']
        self.Database_referred = jmodel['Database_referred']
        self.identity = jmodel['identity']
        self.MS1_pseudo_Spectra  = jmodel['MS1_pseudo_Spectra']
        self.MS2_Spectra = jmodel['MS2_Spectra']    

    def serialize(self):
        features = []
        for peak in self.MS1_pseudo_Spectra:
                features.append(        # this is given as example; one may need to modify the mapping variable names
                   {"id_number": peak['id'], "mz": peak['mz'], "rtime": peak['rtime'], "charged_formula": "",  "ion_relation": peak['ion_relation'],}
                )
        return {'interim_id': self.interim_id, 
                'neutral_formula_mass': self.neutral_formula_mass,
                'neutral_formula': self.neutral_formula,
                'Database_referred': self.Database_referred,
                'identity': self.write_identity(),
                'MS1_pseudo_Spectra': features,
                'MS2_Spectra': self.MS2_Spectra,
                }


