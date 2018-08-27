
# 'Insititutionnalisés'
#     a='Sécurisés'
#     b='Génériques aigus'
#         c='Hospitaliers'
#         d='Non hospitaliers'
#     e='Non aigus'
#         m='Hospitaliers H'
#             f='Durée limitée (H)'
#                 g='Soutien 24sur 24'
#                 h='Soutien quotidien'
#             i='Sejour durée indéfinie (H)'
#                 g='Soutien 24 sur 24'
#                 h='Soutien quotidien'
#          n='Non hospitaliers'
#             j='Durée limitée (NH)'
#                  g='Soutien 24 sur 24'
#                 'Soutien quotidien'
#                 l='Soutien léger'
#             k='Sejour durée indéfinie (NH)'
#                  g='Soutien 24 sur 24'
#                 'Soutien quotidien'
#                 'Soutien léger'

CHOIX_INSTITUT = {
    'z': {'name': 'Institutionnalisés', 'choices': ['a','b','e']},
    'a': {'name': 'Sécurisés', 'choices':[] },
    'b': {'name': 'Génériques aigus', 'choices':['c','d'] },
        'c': {'name': 'Hospitaliers', 'choices':[] },
        'd': {'name': 'Non hospitaliers', 'choices':[] },
    'e': {'name': 'Non aigus', 'choices':['m','n'] },
        'm': {'name': 'Hospitaliers (H)', 'choices': ['f', 'i'] },
            'f': {'name': 'Durée limitée (H)', 'choices':['g','h']},
                'g': {'name': 'Soutien 24h sur 24', 'choices': [] },
                'h': {'name': 'Soutien quotidien', 'choices': [] },
            'i': {'name': 'Sejour durée indéfinie (H)', 'choices':['g','h'] },
        'n': {'name': 'Non hospitaliers (NH)', 'choices': ['j', 'k'] },
            'j': {'name': 'Durée limitée (NH)', 'choices':['g','h','l'] },
            'k': {'name': 'Sejour durée indéfinie (NH)', 'choices':['g','h','l'] },
                'l': {'name': 'Soutien léger', 'choices':[] },
    }

CHOIX_FINAL = {
    'za': 'SECURE- BRANCH R1',
    'zbc': 'ACUTE-HOSPITAL- BRANCH R2',
    'zbd': 'ACUTE-NON-HOSPITAL- BRANCH R3',
    'zemfg': 'HOSPITAL-TIME LIMITED-24 HOUR SUPPORT- BRANCH R4',
    'zemfh': 'HOSPITAL-TIME LIMITED-DAILY SUPPORT - BRANCH R5',
    'zemig': 'HOSPITAL-INDEFINITE STAY-24 HOUR SUPPORT- BRANCH R6',
    'zemih': 'HOSPITAL-INDEFINITE STAY-DAILY SUPPORT - BRANCH R7',
    'zenjg': 'NON-HOSPITAL-TIME LIMITED STAY-24 HOUR SUPPORT- BRANCH R8',
    'zenjh': 'NON-HOSPITAL-TIME LIMITED-DAILY SUPPORT - BRANCH R9',
    'zenjl': 'NON-HOSPITAL-TIME LIMITED-LOWER SUPPORT - BRANCH R10',
    'zenkg': 'NON-HOSPITAL-INDEFINITE STAY-24 HOUR SUPPORT- BRANCH R11',
    'zenkh': 'NON-HOSPITAL-INDEFINITE STAY-DAILY SUPPORT - BRANCH R12',
    'zenkl': 'NON-HOSPITAL-INDEFINITE STAY-LOWER SUPPORT - BRANCH R13',
}

EXPLICATIONS = {
    'z': "Facilities which provide beds overnight for patients for a purpose related to the clinical and social management of their mental illnesses - patients are not intended to sleep there solely because they have no home or are unable to reach home",
    'a': "Beds to which patients are admitted because they are considered by clinicians to be too dangerous to themselves or others to be managed adequately on the usual catchment area admission wards, or because of a specific legal judgement which states that for reasons of safety they must go to this particular facility rather than to the local generic facilities. <br />NB Beds to which compulsory admissions can be made should not automatically be categorised as secure beds - it is possible for a patient to be compulsorily admitted to a generic acute facility. Only beds specifically intended to provide a greater level of security than those to which patients from the catchment area are routinely admitted should be classified as secure.",
    'b': "Facilities where <br />(i) patients are admitted because of a deterioration in their mental state, behaviour or social functioning which is related to psychiatric disorder; <br />(ii) admission usually available within 24 hours; <br />(iii) patients usually retain their own accommodation.",
    'm': "Residential facilities which are located within the grounds of an institution classified under national or local laws as a hospital.",
    'c': "Residential facilities which are located within the grounds of an institution classified under national or local laws as a hospital.",
    'n': "All residential facilities located outside hospital grounds.",
    'd': "All residential facilities located outside hospital grounds.",
    'e': "All residential facilities which do not satisfy the criteria for acute or secure facilities.",
    'f': "Time-limited: These are facilities where a fixed maximum period of residence is routinely specified. A facility should be classified as time-limited if a maximum length of stay is fixed for at least 80% of those entering the facility.",
    'j': "These are facilities where a fixed maximum period of residence is routinely specified. A facility should be classified as time-limited if a maximum length of stay is fixed for at least 80% of those entering the facility.",
    'k': "Residential facilities which do not fulfil the above criteria for ‘time-limited’ services.",
    'i': "Residential facilities which do not fulfil the above criteria for ‘time-limited’ services.",
    'g': "Facilities where there are staff present within the facility 24 hours a day, with responsibilities relating to the monitoring and clinical and social care of the patient (i.e. domestic or security staff are not included).",
    'l': " Facilities where the patient resides for some purpose related to the management of his/her mental illness and where there is a direct link between residing in the facility and some support from staff, but where staff are regularly present fewer than five days per week.",
    'h': "---",
}



