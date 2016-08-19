#!/usr/bin/env python


data_path = 'Neulaw/'
include_always = ['codebook.html']
datasets = {}

datasets['hc'] = {
    'name': "Harris County, TX",
    'source': "hc.csv",
    'fields': {
        'case.date': "Case Date",
        'case.status': "Case Status Code",
        'case.bond': "Case Bond Amount Set",
        'case.code': "Current Offense Code",
        'case.literal': "Current Offense Code Literal",
        'case.degree': "Level and Degree of Current Offense",
        'case.statetrn': "Unique State Level Case Identifier",
        'def.uid': "Defendant's Unique System Person ID (SPN number)",
        'def.race': "Defendant Race",
        'def.gender': "Defendant Gender",
        'def.dob': "Defendant Date of Birth",
        'def.height': "Defendant Height",
        'def.weight': "Defendant Weight",
        'def.citizenship': "Citizenship",
        'att.literal': "Attorney Connection to the Case Literal",
        'off.date': "Date of the Offense",
        'off.bond': "Bond Amount at Time of Offense/Arrest",
        'off.code': "Offense Code at Time of Offense/Arrest",
        'off.literal': "Offense Literal at Time of Offense/Arrest",
        'off.degree': "Offense Literal at Time of Offense/Arrest",
        'gj.date': "Date of Grand Jury Action",
        'gj.status': "Defendant Status at Time of Grand Jury Action",
        'gj.action': "Grand Jury Action Code",
        'gj.courtnr': "Grand Jury Court",
        'gj.offcode': "Offense at Time of Grand Jury Action",
        'gj.offliteral': "Grand Jury Offense Code Literal",
        'gj.offdegree': "Level and Degree of Grand Jury Offense",
        'gj.bond': "Bond Amount at time of Grand Jury Action",
        'disp.date': "Disposition Date",
        'disp.plea': "Disposition Plea",
        'disp.literal': "Disposition Literal",
        'calc.age': "Calculated Age",
        'calc.race': "Calculated Race",
        'calc.gender': "Calculated Gender",
        'calc.casenr': "Calculated Case Number",
        'calc.broad': "Calculated Broad Crime Category",
        'calc.detailed': "Calculated Detailed Crime Category",
        'calc.disp': "Calculated Disposition",
        'calc.year': "Calculated Year"
    },
    'fields_of_interest': [
        'calc.year',
        'calc.gender',
        'calc.race',
        'calc.broad',
        'calc.disp'
    ],
    'additional_files': [
        'HC crime codes - Dispositions.csv',
        'HC crime codes - Offenses.csv',
    ],
    'description': """
    Harris County, TX, is the 3rd most populous county in the
    United States and is the county seat of Houston, TX. It consists of 3.1
    million records, spanning from 1977 to April, 2012. The data contains 61
    variables and was obtained from the Harris County District Clerk's Office
    in September, 2013.
    """
}

datasets['mdc'] = {
    'name': "Miami Dade County, FL",
    'source': "mdc.csv",
    'fields': {
        'arrest.date': "Arrest Date",
        'case.date': "Case Date",
        'case.closed': "Case Closed",
        'def.race': "Defendant Race",
        'def.gender': "Defendant Gender",
        'def.dob': "Defendant Date of Birth",
        'case.nr': "Case Number",
        'case.status': "Case Status",
        'arrest.code': "Arrest Code",
        'case.code': "Case Code",
        'disp.code': "Disposition Code",
        'disp.plea': "Disposition Plea",
        'case.trialtype': "Case Trial Type",
        'disp.literal': "Disposition Literal",
        'calc.age': "Calculated Age",
        'calc.race': "Calculated Race",
        'calc.gender': "Calculated Gender",
        'calc.broad': "Broad Crime Category",
        'calc.detailed': "Detailed Crime Category",
        'calc.disp': "Calculated Disposition",
        'calc.year': "Calculated Year"
    },
    'fields_of_interest': [
        'calc.year',
        'def.gender',
        'calc.race',
        'calc.broad',
        'calc.disp'
    ],
    'additional_files': [
        'MDC crime codes - Dispositions.csv',
        'MDC crime codes - Offenses.csv',
    ],
    'description': """
    Miami-Dade County, FL, is the 7th most populous county in the United States
    and is the county seat of Miami, FL. It consists of 5.7 million records
    spanning from 1971 to 2012. The data contains 30 variables and was obtained
    from Miami-Dade County Clerks Criminal Justice Information System on
    December 3, 2013.
    """
}

datasets['nyc'] = {
    'name': "New York City, NY",
    'source': "nyc.csv",
    'fields': {
        'arrest.county': "Arrest County",
        'off.month': "Offense Month",
        'off.year': "Offense Year",
        'arrest.month': "Arrest Month",
        'arrest.year': "Arrest Year",
        'arrest.charge': "Top Arrest Charge",
        'def.gender': "Defendant Gender",
        'def.age': "Defendant Age",
        'def.race': "Defendant Race",
        'disp.month': "Disposition Month",
        'disp.year': "Disposition Year",
        'disp.county': "Disposition County",
        'disp.charge': "Disposition Charge",
        'disp.type': "Disposition Type",
        'calc.broad': "Broad Crime Category",
        'calc.detailed': "Detailed Crime Category",
        'calc.disp': "Calculated Disposition",
        'calc.year': "Calculated Year",
        'calc.race': "Calculated Race"
    },
    'fields_of_interest': [
        'calc.year',
        'def.gender',
        'calc.race',
        'calc.broad',
        'calc.disp'
    ],
    'additional_files': [
        'NYC crime codes - Dispositions.csv',
        'NYC crime codes - Offenses.csv',
    ],
    'description': """
    New York City, NY, is the most populous city in the United States. It
    consists of 9.8 million records spanning from 1977 to 2013. The data
    contains 20 variables and was obtained from New York State Division of
    Criminal Justice Services in 2013. It currently only contains the most
    serious charge in a given arrest and does not yet contain identifiers.
    """
}
