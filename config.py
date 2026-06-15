# Configuration for BacteReason

# Common bacterial pathogens in the training data (AMR Portal-derived).
SPECIES_LIST = [
    "Acinetobacter baumannii",
    "Campylobacter coli",
    "Campylobacter jejuni",
    "Enterococcus faecalis",
    "Enterococcus faecium",
    "Escherichia coli",
    "Klebsiella pneumoniae",
    "Mycobacterium tuberculosis",
    "Neisseria gonorrhoeae",
    "Pseudomonas aeruginosa",
    "Salmonella enterica",
    "Staphylococcus aureus",
    "Streptococcus pneumoniae",
]

# Antibiotics covered in the training data, grouped by class.
# Used for both the phenotype profile builder and the target dropdown.
ANTIBIOTICS_BY_CLASS = {
    "Penicillins": [
        "ampicillin", "amoxicillin-clavulanic acid", "ampicillin-sulbactam",
        "piperacillin", "piperacillin-tazobactam", "penicillin",
    ],
    "Cephalosporins": [
        "cefazolin", "cephalothin", "cefuroxime", "cefoxitin", "cefotetan",
        "cefotaxime", "cefpodoxime", "ceftazidime", "ceftriaxone", "cefepime",
        "cefiderocol", "ceftolozane-tazobactam", "ceftazidime-avibactam",
        "cefotaxime-clavulanic acid", "ceftazidime-clavulanic acid", "ceftiofur",
    ],
    "Carbapenems": [
        "ertapenem", "imipenem", "meropenem", "doripenem",
        "imipenem-relebactam", "meropenem-vaborbactam",
    ],
    "Monobactams": [
        "aztreonam",
    ],
    "Aminoglycosides": [
        "amikacin", "gentamicin", "tobramycin", "streptomycin", "plazomicin",
        "kanamycin", "neomycin", "netilmicin", "spectinomycin",
    ],
    "Fluoroquinolones": [
        "ciprofloxacin", "levofloxacin", "moxifloxacin", "nalidixic acid",
        "ofloxacin", "norfloxacin",
    ],
    "Tetracyclines": [
        "tetracycline", "doxycycline", "minocycline", "tigecycline", "eravacycline",
    ],
    "Macrolides": [
        "azithromycin", "erythromycin", "clarithromycin", "telithromycin", "clindamycin",
    ],
    "Phenicols": [
        "chloramphenicol", "florfenicol",
    ],
    "Glycopeptides": [
        "vancomycin",
    ],
    "Oxazolidinones": [
        "linezolid",
    ],
    "Folate inhibitors": [
        "trimethoprim", "sulfisoxazole", "sulfamethoxazole",
        "trimethoprim-sulfamethoxazole",
    ],
    "Polymyxins": [
        "colistin", "polymyxin B",
    ],
    "Other": [
        "nitrofurantoin", "fosfomycin", "rifampin",
        "isoniazid", "pyrazinamide", "ethambutol",
    ],
}

# Flat sorted list for dropdowns.
ANTIBIOTIC_LIST = sorted({ab for abs_ in ANTIBIOTICS_BY_CLASS.values() for ab in abs_})

# Demo phenotype profile prefilled on page load.
EXAMPLE_PROFILE = {
    "species": "Salmonella enterica",
    "biosample": "SAMN04224378",
    "target_antibiotic": "amoxicillin-clavulanic acid",
    "measurements": [
        ("trimethoprim-sulfamethoxazole", "susceptible", "<= 0.125/2.4 mg/L"),
        ("amikacin", "susceptible", "== 2 mg/L"),
        ("kanamycin", "susceptible", "<= 8 mg/L"),
        ("streptomycin", "resistant", "> 64 mg/L"),
    ],
}