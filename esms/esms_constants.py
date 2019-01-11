import yaml

CHOIXFR = {}
CHOIXEN = {}

with open('esms/arbreen.yml', encoding='utf8') as entree:
    CHOIXEN = yaml.load(entree)

with open('esms/arbrefr.yml', encoding='utf8') as entree:
    CHOIXFR = yaml.load(entree)

CHOIX = (
    ('za', 'Residential services: Branch R1'),
    ('zbc', 'Residential services: Branch R2'),
    ('zbd', 'Residential services: Branch R3'),
    ('zemfg', 'Residential services: Branch R4'),
    ('zemfh', 'Residential services: Branch R5'),
    ('zemig', 'Residential services: Branch R6'),
    ('zemih', 'Residential services: Branch R7'),
    ('zenjg', 'Residential services: Branch R8'),
    ('zenjh', 'Residential services: Branch R9'),
    ('zenjl', 'Residential services: Branch R10'),
    ('zenkg', 'Residential services: Branch R11'),
    ('zenkh', 'Residential services: Branch R12'),
    ('zenkl', 'Residential services: Branch R13'),
    ('op',  'Day & Structured Activity Services: Branch D1'),
    ('oqrs', 'Day & Structured Activity Services: Branch D2'),
    ('oqrt', 'Day & Structured Activity Services: Branch D3'),
    ('oqru', 'Day & Structured Activity Services: Branch D4'),
    ('oqrv', 'Day & Structured Activity Services: Branch D5'),
    ('oqws', 'Day & Structured Activity Services: Branch D6'),
    ('oqwt', 'Day & Structured Activity Services: Branch D7'),
    ('oqwu', 'Day & Structured Activity Services: Branch D8'),
    ('oqwv', 'Day & Structured Activity Services: Branch D9'),
    ('xy13', 'Out-Patient & Community Services: Branch O1'),
    ('xy14', 'Out-Patient & Community Services: Branch O2'),
    ('xy23', 'Out-Patient & Community Services: Branch O3'),
    ('xy24', 'Out-Patient & Community Services: Branch O4'),
    ('x568', 'Out-Patient & Community Services: Branch O5'),
    ('x569', 'Out-Patient & Community Services: Branch O6'),
    ('x560', 'Out-Patient & Community Services: Branch 07'),
    ('x578', 'Out-Patient & Community Services: Branch O8'),
    ('x579', 'Out-Patient & Community Services: Branch O9'),
    ('x570', 'Out-Patient & Community Services: Branch O10'),
    ('qq', 'Self-Help & Other Non-Professional Services: Branch S1'),
    ('rr', 'Soutien & Ecoute Téléphonique: Branch T1'),
    ('ss', 'Soutien ou Répit pour Familles ou Proches: Branch F1'),
    )

CHOIX_FINAL = dict(CHOIX)

EXPLICATIONSFR = {
    'z': "Structures proposant des lits pour la nuit à des patients dans un but en rapport avec la prise en charge clinique et sociale de leur maladie mentale ; l'intention n'est pas que les patients dorment dans ces structures pour la seule raison qu'ils n'ont pas de domicile ou qu'ils ne sont pas en mesure de rentrer chez eux.<br /><b>La plupart des structures institutionnalisées devraient n'être classables que dans l'une de ces branches, bien qu'il puisse parfois être nécessaire de classer une structure dans plusieurs branches - p.ex. un foyer qui compte à la fois des lits clairement destinés aux patients admis en situation de crise et des lits auxquels les patients sont admis de manière planifiée pour une période indéfinie. <br />En revanche, une structure ne peut pas à la fois être classée comme une structure de séjour à durée limitée et une structure de séjour à durée indéfinie, ou comme une structure hospitalière et une structure non hospitalière. <br />Les catégories soutien 24 h/24, soutien quotidien et soutien léger s'excluent aussi mutuellement.</b>",
    'a': "Lits destinés aux patients considérés par les cliniciens comme trop dangereux pour eux-mêmes ou pour les autres pour pouvoir être pris en charge de manière adéquate dans les services d'hospitalisation habituels de la zone de recrutement ou en raison d'une décision de justice spécifique stipulant que pour des raisons de sécurité, ces patients doivent être admis dans telle structure particulière plutôt que dans des structures génériques locales. N.B. : les lits pouvant faire l'objet d'une hospitalisation autoritaire ne doivent pas nécessairement être classés comme des lits sécurisés ; ainsi, un patient pourra bénéficier d'une hospitalisation autoritaire dans une structure de soins génériques aigus. Seuls les lits spécifiquement destinés à procurer un niveau de sécurité plus grand que celui des lits auxquels peuvent être admis les patients de la zone de recrutement considérée doivent être classés comme sécurisés.",
    'b': "Structures dans lesquelles : <br />(i) les patients sont admis en raison d'une dégradation de leur état mental, de leur comportement ou de leur fonctionnement social, en rapport avec un trouble psychiatrique ;<br />(ii) l'admission est généralement possible dans un délai de 24 heures ;<br />(iii) les patients gardent généralement leur propre résidence.",
    'm': "Structures institutionnalisées situées dans le territoire d'une institution classée comme un hôpital aux termes de la loi nationale ou locale.",
    'c': "Structures institutionnalisées situées dans le territoire d'une institution classée comme un hôpital aux termes de la loi nationale ou locale.",
    'n': "Toutes les structures institutionnalisées situées en dehors du territoire d'un hôpital.",
    'd': "Toutes les structures institutionnalisées situées en dehors du territoire d'un hôpital.",
    'e': "Toutes les structures institutionnalisées ne répondant pas aux critères des structures pour soins aigus ou sécurisés.",
    'f': "Il s'agit des structures pour lesquelles une période maximale de séjour est généralement spécifiée. Une structure doit être classée comme étant à durée limitée si la durée maximale du séjour est fixée pour au moins 80 % des personnes admises dans cette structure.",
    'j': "Il s'agit des structures pour lesquelles une période maximale de séjour est généralement spécifiée. Une structure doit être classée comme étant à durée limitée si la durée maximale du séjour est fixée pour au moins 80 % des personnes admises dans cette structure.",
    'k': "Structures institutionnalisées qui ne remplissent pas les critères de 'durée limitée' énoncés ci-dessus.",
    'i': "Structures institutionnalisées qui ne remplissent pas les critères de 'durée limitée' énoncés ci-dessus.",
    'g': "Structures dans lesquelles des personnels sont présents 24 heures sur 24, chargés du suivi et de la prise en charge clinique et sociale du patient (c'est-à-dire que le personnel de service et de sécurité n'est pas inclus).",
    'h': "Structures dans lesquelles des membres du personnel sont régulièrement présents sur site au moins cinq jours par semaine pendant une partie de la journée et qui sont chargés du suivi et de la prise en charge clinique et sociale du patient.",
    'l': "Structures dans lesquelles le patient réside pour une raison en rapport avec la prise en charge de sa maladie mentale et dans lesquelles il existe un lien direct entre le séjour dans la structure et un soutien du personnel, mais où celui-ci est généralement présent moins de cinq jours par semaine.",
    'o': "Il s'agit de structures <br />(i) qui sont normalement accessibles à plusieurs patients en même temps (plutôt que la délivrance de services à des personnes une par une) ; <br />(ii) qui proposent une certaine combinaison entre un traitement pour des problèmes liés à la maladie mentale, une activité structurée, un contact social et/ou un soutien ; <br />(iii) qui ont des heures d'ouverture régulières au cours desquelles elles sont normalement accessibles ; et <br />(iv) qui prévoient que les patients restent dans la structure considérée au-delà des périodes au cours desquelles ils sont en contact direct avec le personnel (c'est-à-dire que le service n'est pas simplement basé sur des consultations programmées du patient auprès du personnel de la structure, le patient quittant la structure immédiatement après la consultation).",
    'p': "Structures dans lesquelles  <br />(i) les patients sont généralement admis en raison d'une dégradation de leur état mental, de leur comportement ou de leur fonctionnement social, en rapport avec un trouble psychiatrique ;  <br />(ii) le programme se fixe pour objectif de corriger cette dégradation ;  <br />(iii) l'admission est généralement possible dans un délai de 72 heures.",
    'q': "--",
    'r': "Structures ouvertes aux patients pour l'équivalent d'au moins quatre demi-journées par semaine. Tous les patients n'ont pas besoin de recourir si souvent à ce service pour pouvoir être classés dans cette catégorie 'très intensifs', mais il doit cependant au moins être possible pour eux de le faire. <br /><b>Les services ne doivent généralement pas être classés à la fois comme très intensifs et peu intensifs : s'il est possible pour les patients de se présenter dans un service au moins quatre demi-journées par semaine, le service en question sera classé comme un service très intensif, même si certaines personnes fréquentent moins souvent le service.</b>",
    's': "Services qui offrent la possibilité aux patients de travailler en étant payés au moins 50 % du salaire minimum local habituellement garanti pour ce type de travail. S'il n'existe pas de salaire minimum, nous suggérons de calculer un taux de salaire sur la base des salaires d'embauche pour des postes de travail similaires proposés dans la presse locale au cours du mois écoulé. Le travail peut être basé dans un environnement protégé ou bien dans un contexte où certains travailleurs ne sont pas atteints de troubles mentaux. Cela dit, les patients n'obtiennent pas ce travail par le jeu de la libre concurrence ; leurs postes de travail sont en quelque sorte spécifiquement réservés à des gens qui ont des besoins particuliers, y compris en rapport avec des troubles mentaux.",
    't': "Services dans lesquels les patients mènent une activité qui ressemble beaucoup à un travail qui, dans les conditions du marché, serait rémunéré, mais qui, dans ce cas, n'est pas rémunéré ou alors est rémunéré à moins de 50 % du salaire habituel local attendu pour ce type de travail.",
    'u': "Services qui proposent des activités structurées autres que le travail ou une activité en rapport avec le travail. Ces activités peuvent être des activités de formation, des activités de création telles que des activités artistiques ou musicales, ou encore un travail de groupe. Ces activités doivent être accessibles pendant au moins 25 % des heures d'ouverture du service.",
    'v': "Services qui remplissent les critères de services de jour pour soins non aigus, mais où le travail ou autres activités structurées ne sont pas accessibles ou alors ne sont accessibles que pendant moins de 25 % des heures d'ouverture, de sorte que les fonctions principales du service sont d'assurer un contact social, une aide pratique et/ou un soutien.<br /><b>Les services ne doivent généralement pas être classés à la fois comme 'contact social' et comme 'travail', 'activités en rapport avec le travail' ou 'autres activités structurées' : ils ne pourront être classés comme 'contact social' que s'ils n'assurent ni travail ni une autre activité structurée pendant au moins 25 % de leurs heures d'ouverture.</b>",
    'w': "Structures que les patients fréquentent généralement moins de l'équivalent de quatre demi-journées par semaine.",
    'x': "Il s'agit de services qui <br />(i) impliquent un contact entre le personnel chargé de la santé mentale et les patients à des fins en rapport avec la prise en charge de la santé mentale et des difficultés cliniques et sociales qui lui sont associées ; et <br />(ii) qui ne sont pas assurés dans le cadre de services institutionnalisés ou de jour et d'activités structurées, tels qu'ils ont été définis ci-dessus.",
    'y': "Services qui <br />(i) assurent l'évaluation et le traitement initial en réponse à une dégradation de l'état mental, du comportement ou fonctionnement social, en rapport avec un trouble psychiatrique, et <br />(ii) peuvent généralement apporter une réponse le jour même, aux heures ouvrées.",
    '1': "Services pour lesquels le contact avec les patients intervient dans toute une série de contextes, y compris au domicile des patients, selon ce que les professionnels et les patients jugent le plus approprié. Un service est qualifié de 'mobile' si au moins 20 % des contacts interviennent en dehors des locaux dans lesquels le service en question est basé. Pour certains services, le site principal de prestation du service peut varier d'un jour à l'autre (p.ex. les services assurés dans les zones rurales se déplaçant de village en village) ; <br />cela ne veut pas dire pour autant, dans ce cas-là, que les services doivent être classés comme 'mobiles', sauf si le personnel se déplace pour effectuer son travail en dehors du site principal de la journée considérée.<br />Les services ne doivent pas être classés à la fois comme mobiles et non mobiles : si au moins 20 % des visites ont lieu en dehors du site principal du service, le service doit être classé uniquement comme mobile.",
    '2': "Services ne répondant pas aux critères de services 'mobiles'.",
    '3': "Services accessibles 24 heures sur 24, 7 jours par semaine. <br /><b>Les services ne doivent pas être classés à la fois comme fonctionnant 24 h/24 et à des heures limitées </b>: s'il y a des périodes au cours de la semaine où le service est fermé et n'assure pas de visites, le service en question doit être classé comme fonctionnant à des 'heures limitées'.",
    '4': "Services qui ne sont pas toujours accessibles (heures d'ouverture : moins de 24 heures par jour, moins de 7 jours par semaine).",
    '5': "Services qui fournissent aux patients un contact régulier avec un professionnel de santé mentale, contact qui peut être à long terme, le cas échéant.",
    '6': "Services pour lesquels le contact avec les patients intervient dans toute une série de contextes, y compris au domicile des patients, selon ce que les professionnels et les patients jugent le plus approprié. Un service est qualifié de 'mobile' si au moins 20 % des contacts interviennent en dehors des locaux dans lesquels le service en question est basé. Pour certains services, le site principal de prestation du service peut varier d'un jour à l'autre (p.ex. les services assurés dans les zones rurales se déplaçant de village en village) ; <br />cela ne veut pas dire pour autant, dans ce cas-là, que les services doivent être classés comme 'mobiles', sauf si le personnel se déplace pour effectuer son travail en dehors du site principal de la journée considérée.<br />Les services ne doivent pas être classés à la fois comme mobiles et non mobiles : si au moins 20 % des visites ont lieu en dehors du site principal du service, le service doit être classé uniquement comme mobile.",
    '7': "Services ne répondant pas aux critères de services 'mobiles'.",
    '8': "Services qui ont la possibilité d'assurer des contacts directs avec les patients au moins trois fois par semaine si cela s'avère nécessaire sur le plan clinique.<br /><b>Les catégories fortement intensif, modérément intensif et peu intensif s'excluent mutuellement <b/>: si un service peut assurer des visites trois fois par semaine, il est considéré comme très intensif, même si de nombreux patients de ce service sont vus moins souvent que cela. Si un service peut assurer des visites au moins une fois tous les quinze jours, mais pas au rythme de trois fois par semaine, il est considéré comme modérément intensif, même si certains patients sont vus moins souvent qu'une fois tous les quinze jours. Seuls les services qui ne peuvent généralement pas assurer de contacts au moins une fois tous les quinze jours doivent être classés comme peu intensifs.",
    '9': "Services qui n'ont pas la possibilité d'assurer des contacts avec les patients au rythme de trois fois par semaine, mais qui peuvent assurer des contacts au moins une fois tous les quinze jours, si cela s'avère nécessaire.",
    '0': "Services qui assurent aux patients des contacts réguliers avec des professionnels de la santé mentale, mais qui n'ont pas la possibilité de voir les patients au rythme d'une fois tous les quinze jours.",
    'qq': "Services qui ciblent spécifiquement les adultes atteints de troubles mentaux, mais qui n'emploient pas de personnel spécialisé chargé d'évaluer, de soutenir ou de traiter les personnes atteintes de troubles mentaux.<br /><b>les services classés ici sont les services dont le rôle principal est d'assurer une certaine forme de soutien, d'aide ou de contact à des personnes atteintes de maladies mentales ou à leurs soignants, mais qui n'emploient pas de personnel dont le rôle serait d'assurer les services institutionnalisés, de jour, ambulatoires ou communautaires décrits pour les autres branches. <br />Les groupes d'entraide animés par les utilisateurs ou bien les centres d'accueil, les groupements de soignants informels assurant un soutien mutuel ainsi que les services exclusivement fournis par des bénévoles doivent être regroupés dans cette branche.</b>",
    'rr': 'Soutien & Ecoute Téléphonique: Branch T1',
    'ss': 'Soutien ou Répit pour Familles ou Proches: Branch F1',
}

EXPLICATIONSEN = {
    'z': "Facilities which provide beds overnight for patients for a purpose related to the clinical and social management of their mental illnesses - patients are not intended to sleep there solely because they have no home or are unable to reach home. <br /><b>Most residential facilities should be classifiable as belonging to only one of these branches, although occasionally it may be necessary to place a facility on multiple branches - e.g. a hostel which has a mixture of beds clearly designated for crisis admission and beds to which patients are admitted in a planned way for an indefinite period. <br />Facilities should not be classified as both time-limited and indefinite stay, or as both hospital and non-hospital. <br />24 hour supported, daily supported and lower support are also intended to be mutually exclusive categories</b>",
    'a': "Beds to which patients are admitted because they are considered by clinicians to be too dangerous to themselves or others to be managed adequately on the usual catchment area admission wards, or because of a specific legal judgement which states that for reasons of safety they must go to this particular facility rather than to the local generic facilities. <br />NB Beds to which compulsory admissions can be made should not automatically be categorised as secure beds - it is possible for a patient to be compulsorily admitted to a generic acute facility. Only beds specifically intended to provide a greater level of security than those to which patients from the catchment area are routinely admitted should be classified as secure.",
    'b': "Facilities where <br />(i) patients are admitted because of a deterioration in their mental state, behaviour or social functioning which is related to psychiatric disorder; <br />(ii) admission usually available within 24 hours; <br />(iii) patients usually retain their own accommodation.",
    'm': "Residential facilities which are located within the grounds of an institution classified under national or local laws as a hospital.",
    'c': "Residential facilities which are located within the grounds of an institution classified under national or local laws as a hospital.",
    'n': "All residential facilities located outside hospital grounds.",
    'd': "All residential facilities located outside hospital grounds.",
    'e': "All residential facilities which do not satisfy the criteria for acute or secure facilities.",
    'f': "These are facilities where a fixed maximum period of residence is routinely specified. A facility should be classified as time-limited if a maximum length of stay is fixed for at least 80% of those entering the facility.",
    'j': "These are facilities where a fixed maximum period of residence is routinely specified. A facility should be classified as time-limited if a maximum length of stay is fixed for at least 80% of those entering the facility.",
    'k': "Residential facilities which do not fulfil the above criteria for ‘time-limited’ services.",
    'i': "Residential facilities which do not fulfil the above criteria for ‘time-limited’ services.",
    'g': "Facilities where there are staff present within the facility 24 hours a day, with responsibilities relating to the monitoring and clinical and social care of the patient (i.e. domestic or security staff are not included).",
    'h': "Facilities where there are members of staff regularly on site at least five days a week for some part of the day, with responsibilities related to the monitoring and clinical and social care of the patient.",
    'l': "Facilities where the patient resides for some purpose related to the management of his/her mental illness and where there is a direct link between residing in the facility and some support from staff, but where staff are regularly present fewer than five days per week.",
    'o': "These are facilities which <br />(i) are normally available to several patients at a time (rather than delivering services to individuals one at at time); <br />(ii) provide some combination of treatment for problems related to mental illness, structured activity, social contact and/or support; <br />(iii) have regular opening hours during which they are normally available: and (iv) expect patients to stay at the facilities beyond the periods during which they have face-to-face contact with staff (i.e. the service is not simply based on patients coming for appointments with staff & then leaving immediately after their appointments).",
    'p': "Facilities where <br />(i) patients are regularly admitted because of a deterioration in mental state, behaviour or social functioning which is related to psychiatric disorder; <br />(ii) alleviating this deterioration is a purpose of the programme; <br />(iii) admission to the programme is usually available within 72 hours.",
    'q': "--",
    'r': "Facilities which are available for patients to attend for at least the equivalent of four half days per week. Not all the patients need attend as frequently as this for the service to be classified as ‘high intensity’, but it should at least be possible for them to do so.<br /><b>Services should not generally be classified as both high intensity and low intensity:</b> if it is possible for patients to attend at least four half days a week, the service should be classified as high intensity, even if some attend less frequently than this.",
    's': "Services which provide patients with the opportunity to work, with pay at least 50% of the usual local minimum expected wage for this form of work. Where there is no minimum wage, we suggest calculating an expected level based on starting salaries for similar jobs advertised in the local press over the past month. The work may be in a sheltered setting or in a setting where some workers are not mentally ill. However, patients have not obtained this work through fully open competition - their jobs are in some way specifically reserved for people with particular needs including those arising from mental illness.",
    't': "Services where patients carry out an activity which closely resembles work for which payment would be expected in the open market, but where patients are not paid or are paid less than 50% of the usual local expected wage for this form of work.",
    'u': "Services which provide structured activities apart from work and work-related activity. Such activities may include skills training, creative activities such as art or music, and group work. These activities should be available during at least 25% of the service’s opening hours.",
    'v': "Services which fulfil the criteria for non-acute day services, but where work or other structured activities are not available, or available only during less than 25% of opening hours, so that the main functions of the service are the provision of social contact, practical help and/or support.<br /><b>Services should not generally be classified as ‘social contact’ as well as ‘work’, work related activity’ or ‘other stuctured activity’:</b> They should only be classified as ‘social contact’ if they do not provide work or other structured activity for at least 25% of their opening hours",
    'w': "Facilities at which patients usually attend for less than the equivalent of four half days per week.",
    'x': "These are services which <br />(i) involve contact between mental health staff and patients for some purpose related to management of mental illness and its associated clinical and social difficulties and <br />(ii) are not provided as a part of delivery of residential or day and structured activity services, as defined above.",
    'y': "Services which <br />(i) provide assessment and initial treatment in response to a deterioration in mental state, behaviour or social functioning which is related to psychiatric disorder; and <br />(ii) can usually provide a same day response during working hours.",
    '1': "Services where contact with patients occurs in a range of settings including patients’ homes, as judged most appropriate by professionals and patients. For a service to be classified as ‘mobile’, at least 20% of contacts should take place away from the premises at which the service is based. For some services, the main site of service provision may vary from day to day (e.g. services in rural areas which move from village to village) - this does not mean they should be classified as ‘mobile’ unless staff go and do work at locations away from that day’s main site.<br /><b>Services should not be classified as both mobile and non-mobile:</b> If at least 20% of visits take place away from the main service site, they should be classified only as mobile.",
    '2': "Services which do not meet the criteria for ‘mobile’.",
    '3': "Services which are available 24 hours a day, 7 days per week. <br />Services should not be classified as both 24 hours and limited hours: If there are any periods during the week when the service is closed and carries out no visits, it should be classified as ‘limited hours",
    '4': "Services which are not always available (opening hours less than 24 hours, 7 days per week)",
    '5': "Services which provide patients with regular contact with a mental health professional, which may be long term if required.",
    '6': "Services where contact with patients occurs in a range of settings including patients’ homes, as judged most appropriate by professionals and patients. For a service to be classified as ‘mobile’, at least 20% of contacts should take place away from the premises at which the service is based. For some services, the main site of service provision may vary from day to day (e.g. services in rural areas which move from village to village) - this does not mean they should be classified as ‘mobile’ unless staff go and do work at locations away from that day’s main site.<br /><b>Services should not be classified as both mobile and non-mobile:</b> If at least 20% of visits take place away from the main service site, they should be classified only as mobile.",
    '7': "Services which do not meet the criteria for ‘mobile’.",
    '8': "Services which have the capacity to make face to face contact with patients at least three times per week when clinically indicated.<br /><b>High intensity, medium intensity and low intensity are intended to be mutually exclusive</b>: If a service can provide visits three times per week, it is high intensity, even if many of its patients are seen less frequently than this. If a service can provide visits at least once a fortnight, but not as often as three times per week, it is medium intensity, even if some patients are seen less frequently than once a fortnight. Only servces which cannot generally provide contacts at least once a fortnight should be classified as low intensity",
    '9': "Services which do not have the capacity to supply three times weekly contact to patients, but which can provide contacts at least once a fortnight when indicated.",
    '0': "Services which provide regular contacts with mental health professionals for patients, but which do not have the capacity to see patients as often as once a fortnight.",
    'qq': "Services which specifically target adults with mental illnesses, but which do not employ any specialist staff whose work is to assess, support or treat people with mental illnesses",
    'rr': 'Soutien & Ecoute Téléphonique: Branch T1',
    'ss': 'Soutien ou Répit pour Familles ou Proches: Branch F1',
}

