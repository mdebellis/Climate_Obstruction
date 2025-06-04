from src.ag_api import *

stop_words1 = {'those', 'on', 'own', '’ve', 'yourselves', 'around', 'between', 'four', 'been', 'alone', 'off', 'am', 'then', 'other', 'can', 'regarding', 'hereafter', 'front', 'too', 'used', 'wherein', '‘ll', 'doing', 'everything', 'up', 'onto', 'never', 'either', 'how', 'before', 'anyway', 'since', 'through', 'amount', 'now', 'he', 'was', 'have', 'into', 'because', 'not', 'therefore', 'they', 'n’t', 'even', 'whom', 'it', 'see', 'somewhere', 'thereupon', 'nothing', 'whereas', 'much', 'whenever', 'seem', 'until', 'whereby', 'at', 'also', 'some', 'last', 'than', 'get', 'already', 'our', 'once', 'will', 'noone', "'m", 'that', 'what', 'thus', 'no', 'myself', 'out', 'next', 'whatever', 'although', 'though', 'which', 'would', 'therein', 'nor', 'somehow', 'whereupon', 'besides', 'whoever', 'ourselves', 'few', 'did', 'without', 'third', 'anything', 'twelve', 'against', 'while', 'twenty', 'if', 'however', 'herself', 'when', 'may', 'ours', 'six', 'done', 'seems', 'else', 'call', 'perhaps', 'had', 'nevertheless', 'where', 'otherwise', 'still', 'within', 'its', 'for', 'together', 'elsewhere', 'throughout', 'of', 'others', 'show', '’s', 'anywhere', 'anyhow', 'as', 'are', 'the', 'hence', 'something', 'hereby', 'nowhere', 'latterly', 'say', 'does', 'neither', 'his', 'go', 'forty', 'put', 'their', 'by', 'namely', 'could', 'five', 'unless', 'itself', 'is', 'nine', 'whereafter', 'down', 'bottom', 'thereby', 'such', 'both', 'she', 'become', 'whole', 'who', 'yourself', 'every', 'thru', 'except', 'very', 'several', 'among', 'being', 'be', 'mine', 'further', 'n‘t', 'here', 'during', 'why', 'with', 'just', "'s", 'becomes', '’ll', 'about', 'a', 'using', 'seeming', "'d", "'ll", "'re", 'due', 'wherever', 'beforehand', 'fifty', 'becoming', 'might', 'amongst', 'my', 'empty', 'thence', 'thereafter', 'almost', 'least', 'someone', 'often', 'from', 'keep', 'him', 'or', '‘m', 'top', 'her', 'nobody', 'sometime', 'across', '‘s', '’re', 'hundred', 'only', 'via', 'name', 'eight', 'three', 'back', 'to', 'all', 'became', 'move', 'me', 'we', 'formerly', 'so', 'i', 'whence', 'under', 'always', 'himself', 'in', 'herein', 'more', 'after', 'themselves', 'you', 'above', 'sixty', 'them', 'your', 'made', 'indeed', 'most', 'everywhere', 'fifteen', 'but', 'must', 'along', 'beside', 'hers', 'side', 'former', 'anyone', 'full', 'has', 'yours', 'whose', 'behind', 'please', 'ten', 'seemed', 'sometimes', 'should', 'over', 'take', 'each', 'same', 'rather', 'really', 'latter', 'and', 'ca', 'hereupon', 'part', 'per', 'eleven', 'ever', '‘re', 'enough', "n't", 'again', '‘d', 'us', 'yet', 'moreover', 'mostly', 'one', 'meanwhile', 'whither', 'there', 'toward', '’m', "'ve", '’d', 'give', 'do', 'an', 'quite', 'these', 'everyone', 'towards', 'this', 'cannot', 'afterwards', 'beyond', 'make', 'were', 'whether', 'well', 'another', 'below', 'first', 'upon', 'any', 'none', 'many', 'serious', 'various', 're', 'two', 'less', '‘ve'}
stop_words2 = {'goal','Target', 'Indicator', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.', '14.', '15.', '16.', '17.'}
all_stop_words = stop_words1.union(stop_words2)


at_issue_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/at_issue")
case_categories_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/case_categories")
summary_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/summary")
abstract_prop = conn.createURI("http://purl.org/dc/terms/abstract")
issue_prop = conn.createURI("http://purl.org/ontology/bibo/issue")
text_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/text")
description_prop = conn.createURI("https://w3id.org/semanticarts/ns/ontology/gist/description")
id_text_prop = conn.createURI("https://w3id.org/semanticarts/ns/ontology/gist/idText")
jurisdictions_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/jurisdictions")
principle_laws_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/principal_laws")
action_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/action")
ad_description_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/ad_description")
assessment_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/assessment")
background_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/background")
response_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/response")
contained_text_prop = conn.createURI("https://w3id.org/semanticarts/ns/ontology/gist/containedText")
skos_definition_property = conn.createURI("http://www.w3.org/2004/02/skos/core#definition")
stance_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/stance")
works_with_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/works_with")
funding_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/funding")
leadership_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/leadership")
lobbying_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/lobbying")
members_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/members")
customer_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/customer")
employee_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/employee")

has_topic_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/has_Topic")
is_topic_of_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/is_topic_of")
skos_alt_label_property = conn.createURI("http://www.w3.org/2004/02/skos/core#altLabel")


agent_class = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/Agent")
geo_region_class = conn.createURI("https://w3id.org/semanticarts/ns/ontology/gist/GeoRegion")
has_jurisdiction_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/has_jurisdiction")
exxon = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/ExxonMobil")


conn.createFreeTextIndex("co_fti", predicates=[case_categories_prop,
                                               at_issue_prop, summary_prop,
                                               abstract_prop, issue_prop,
                                               text_prop, description_prop,id_text_prop,
                                               jurisdictions_prop, principle_laws_prop, action_prop,
                                               ad_description_prop,assessment_prop, background_prop,
                                               response_prop, contained_text_prop, skos_definition_property, stance_prop,works_with_prop,
                                               funding_prop,leadership_prop, lobbying_prop,members_prop, customer_prop, employee_prop], stopWords=all_stop_words)

conn.createFreeTextIndex("jurisdictions", predicates=[jurisdictions_prop], stopWords=all_stop_words)

def make_links_for_topic(topic):
    label = get_value(topic, rdfs_label_property)
    pref_label = get_value(topic, skos_pref_label_property)
    alt_label = get_value(topic, skos_alt_label_property)
    if label: make_fti_matches(topic, label)
    if pref_label: make_fti_matches(topic, pref_label)
    if alt_label: make_fti_matches(topic, alt_label)

def make_fti_matches(iri_to_match, label):
    matches = conn.evalFreeTextSearch(label, index="co_fti")
    for match in matches:
        iri_match_string = match[0]
        iri_match = conn.createURI(iri_match_string)
        make_topic_links(iri_to_match,iri_match)

def make_topic_links(topic, document):
    if topic != document:
        put_value(topic, is_topic_of_prop, document)
        put_value(document, has_topic_prop, topic)
        print(f'Topic links made for:  {topic} and {document} ')

def make_jurisdiction_links():
    places = find_instances_of_class(geo_region_class)
    for place in places:
        label = get_value(place, rdfs_label_property)
        pref_label = get_value(place, skos_pref_label_property)
        alt_label = get_value(place, skos_alt_label_property)
        if label: make_jurisdiction_link(place, label)
        if pref_label: make_jurisdiction_link(place, pref_label)
        if alt_label: make_jurisdiction_link(place, alt_label)

def make_jurisdiction_link(iri_to_match, label):
    print(f'Looking for jurisdictions for: {label} ')
    matches = conn.evalFreeTextSearch(label, index="jurisdictions")
    for match in matches:
        iri_match_string = match[0]
        iri_match = conn.createURI(iri_match_string)
        put_value(iri_match, has_jurisdiction_prop, iri_to_match)
        print(f'Jurisdiction links made for:  {iri_match} and {label} ' )

def make_topic_links_for_all_topics():
    make_jurisdiction_links()
    agents = find_instances_of_class(agent_class)
    geo_regions = find_instances_of_class(geo_region_class)
    topics = geo_regions | agents
    for topic in topics:
        make_links_for_topic(topic)

#make_links_for_topic(exxon)
make_topic_links_for_all_topics()
#make_jurisdiction_links()



