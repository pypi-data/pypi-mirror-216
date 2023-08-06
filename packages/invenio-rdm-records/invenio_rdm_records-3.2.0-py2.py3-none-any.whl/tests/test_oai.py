# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test OAI-PMH support."""

from copy import deepcopy

from dojson.contrib.marc21.utils import GroupableOrderedDict, create_record
from lxml import etree

from invenio_rdm_records.oai import (
    datacite_etree,
    dublincore_etree,
    oai_datacite_etree,
    oai_dcat_etree,
    oai_marcxml_etree,
)

from .resources.serializers.test_marcxml_serializer import (
    flatten,
    record_to_string_list,
)

# This tests would ideally be E2E. However, due to the lack of assets building
# in tests we cannot safely query the `/oai2d` endpoint, it will fail due to
# the lack of the `manifest.json` file.


def test_marcxml_serializer(running_app, full_record):
    expected_value = "\n".join(
        [
            '<record xmlns="http://www.loc.gov/MARC21/slim">',
            '  <datafield tag="100" ind1="a" ind2=" ">',
            '    <subfield code="a">Nielsen, Lars Holm</subfield>',
            "  </datafield>",
            '  <datafield tag="901" ind1=" " ind2=" ">',
            '    <subfield code="u">info:eu-repo/semantic/other</subfield>',
            "  </datafield>",
            '  <datafield tag="520" ind1=" " ind2=" ">',
            '    <subfield code="a">A description ',
            "with HTML tags</subfield>",
            '    <subfield code="a">Bla bla bla</subfield>',
            "  </datafield>",
            '  <datafield tag="856" ind1=" " ind2="1">',
            '    <subfield code="a">award_identifiers_scheme=null; award_identifiers_identifier=null; award_title=null; award_number=null; funder_id=00k4n6c32; funder_name=null; </subfield>',
            "  </datafield>",
            '  <datafield tag="909" ind1="C" ind2="O">',
            '    <subfield code="o">oai:vvv.com:abcde-fghij</subfield>',
            "  </datafield>",
            '  <datafield tag="700" ind1="a" ind2=" ">',
            '    <subfield code="u">Nielsen, Lars Holm</subfield>',
            "  </datafield>",
            '  <datafield tag="856" ind1=" " ind2="2">',
            '    <subfield code="a">doi:10.1234/foo.bar</subfield>',
            "  </datafield>",
            '  <datafield tag="540" ind1=" " ind2=" ">',
            '    <subfield code="a">A custom license</subfield>',
            '    <subfield code="a">https://customlicense.org/licenses/by/4.0/</subfield>',
            '    <subfield code="a">Creative Commons Attribution 4.0 International</subfield>',
            '    <subfield code="a">https://creativecommons.org/licenses/by/4.0/legalcode</subfield>',
            "  </datafield>",
            '  <datafield tag="520" ind1=" " ind2="2">',
            '    <subfield code="a">11 pages</subfield>',
            "  </datafield>",
            '  <datafield tag="260" ind1="b" ind2=" ">',
            '    <subfield code="a">InvenioRDM</subfield>',
            "  </datafield>",
            '  <datafield tag="520" ind1=" " ind2="1">',
            '    <subfield code="a">application/pdf</subfield>',
            "  </datafield>",
            '  <datafield tag="653" ind1=" " ind2=" ">',
            '    <subfield code="a">custom</subfield>',
            "  </datafield>",
            '  <datafield tag="260" ind1="c" ind2=" ">',
            '    <subfield code="c">2018/2020-09</subfield>',
            "  </datafield>",
            '  <datafield tag="024" ind1=" " ind2="3">',
            '    <subfield code="a">v1.0</subfield>',
            "  </datafield>",
            '  <datafield tag="245" ind1="a" ind2=" ">',
            '    <subfield code="a">InvenioRDM</subfield>',
            "  </datafield>",
            '  <datafield tag="024" ind1=" " ind2=" ">',
            '    <subfield code="a">10.5281/inveniordm.1234</subfield>',
            '    <subfield code="2">doi</subfield>',
            "  </datafield>",
            "</record>",
        ]
    )

    expected_value = create_record(expected_value)

    record = {"_source": full_record}
    ser_rec = create_record(oai_marcxml_etree(None, record))

    record1 = flatten(record_to_string_list(expected_value))
    record2 = flatten(record_to_string_list(ser_rec))

    record1 = set(record1)
    record2 = set(record2)

    assert record1 == record2


def test_dublincore_serializer(running_app, full_record):
    full_record = deepcopy(full_record)
    full_record["access"]["status"] = "embargoed"

    expected_value = (
        '<oai_dc:dc xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">\n'  # noqa
        "  <dc:contributor>Nielsen, Lars Holm</dc:contributor>\n"
        "  <dc:creator>Nielsen, Lars Holm</dc:creator>\n"
        "  <dc:date>2018/2020-09</dc:date>\n"
        "  <dc:date>info:eu-repo/date/embargoEnd/2131-01-01</dc:date>\n"
        "  <dc:description>A description \nwith HTML tags</dc:description>\n"
        "  <dc:description>Bla bla bla</dc:description>\n"
        "  <dc:format>application/pdf</dc:format>\n"
        "  <dc:identifier>https://doi.org/10.5281/inveniordm.1234</dc:identifier>\n"
        "  <dc:identifier>oai:vvv.com:abcde-fghij</dc:identifier>\n"
        "  <dc:identifier>bibcode:1924MNRAS..84..308E</dc:identifier>\n"
        "  <dc:language>dan</dc:language>\n"
        "  <dc:language>eng</dc:language>\n"
        "  <dc:publisher>InvenioRDM</dc:publisher>\n"
        "  <dc:relation>https://doi.org/10.1234/foo.bar</dc:relation>\n"
        "  <dc:rights>info:eu-repo/semantics/embargoedAccess</dc:rights>\n"
        "  <dc:rights>A custom license</dc:rights>\n"
        "  <dc:rights>https://customlicense.org/licenses/by/4.0/</dc:rights>\n"
        "  <dc:rights>Creative Commons Attribution 4.0 International</dc:rights>\n"  # noqa
        "  <dc:rights>https://creativecommons.org/licenses/by/4.0/legalcode</dc:rights>\n"  # noqa
        "  <dc:subject>custom</dc:subject>\n"
        "  <dc:title>InvenioRDM</dc:title>\n"
        "  <dc:type>info:eu-repo/semantic/other</dc:type>\n"
        "</oai_dc:dc>\n"
    )

    record = {"_source": full_record}
    ser_rec = etree.tostring(dublincore_etree(None, record), pretty_print=True)

    assert expected_value == ser_rec.decode("utf-8")


def test_datacite_serializer(running_app, full_record):
    expected_value = (
        '<resource xmlns="http://datacite.org/schema/kernel-4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4.3/metadata.xsd">\n'  # noqa
        '  <identifier identifierType="DOI">10.5281/inveniordm.1234</identifier>\n'  # noqa
        "  <alternateIdentifiers>\n"
        '    <alternateIdentifier alternateIdentifierType="oai">oai:vvv.com:abcde-fghij</alternateIdentifier>\n'
        '    <alternateIdentifier alternateIdentifierType="bibcode">1924MNRAS..84..308E</alternateIdentifier>\n'  # noqa
        "  </alternateIdentifiers>\n"
        "  <creators>\n"
        "    <creator>\n"
        '      <creatorName nameType="Personal">Nielsen, Lars Holm</creatorName>\n'  # noqa
        "      <givenName>Lars Holm</givenName>\n"
        "      <familyName>Nielsen</familyName>\n"
        '      <nameIdentifier nameIdentifierScheme="ORCID">0000-0001-8135-3489</nameIdentifier>\n'  # noqa
        "      <affiliation>free-text</affiliation>\n"
        '      <affiliation affiliationIdentifier="https://ror.org/01ggx4157" affiliationIdentifierScheme="ROR">CERN</affiliation>\n'  # noqa
        "    </creator>\n"
        "  </creators>\n"
        "  <titles>\n"
        "    <title>InvenioRDM</title>\n"
        '    <title xml:lang="eng" titleType="Subtitle">a research data management platform</title>\n'  # noqa
        "  </titles>\n"
        "  <publisher>InvenioRDM</publisher>\n"
        "  <publicationYear>2018</publicationYear>\n"
        "  <subjects>\n"
        "    <subject>custom</subject>\n"
        '    <subject subjectScheme="MeSH">Abdominal Injuries</subject>\n'
        "  </subjects>\n"
        "  <contributors>\n"
        '    <contributor contributorType="Other">\n'
        '      <contributorName nameType="Personal">Nielsen, Lars Holm</contributorName>\n'  # noqa
        "      <givenName>Lars Holm</givenName>\n"
        "      <familyName>Nielsen</familyName>\n"
        '      <nameIdentifier nameIdentifierScheme="ORCID">0000-0001-8135-3489</nameIdentifier>\n'  # noqa
        '      <affiliation affiliationIdentifier="https://ror.org/01ggx4157" affiliationIdentifierScheme="ROR">CERN</affiliation>\n'  # noqa
        "    </contributor>\n"
        "  </contributors>\n"
        "  <dates>\n"
        '    <date dateType="Issued">2018/2020-09</date>\n'
        '    <date dateType="Other" dateInformation="A date">1939/1945</date>\n'  # noqa
        "  </dates>\n"
        "  <language>dan</language>\n"
        '  <resourceType resourceTypeGeneral="Image">Photo</resourceType>\n'
        "  <relatedIdentifiers>\n"
        '    <relatedIdentifier relatedIdentifierType="DOI" relationType="IsCitedBy" resourceTypeGeneral="Dataset">10.1234/foo.bar</relatedIdentifier>\n'  # noqa
        "  </relatedIdentifiers>\n"
        "  <sizes>\n"
        "    <size>11 pages</size>\n"
        "  </sizes>\n"
        "  <formats>\n"
        "    <format>application/pdf</format>\n"
        "  </formats>\n"
        "  <version>v1.0</version>\n"
        "  <rightsList>\n"
        '    <rights rightsURI="https://customlicense.org/licenses/by/4.0/">A custom license</rights>\n'  # noqa
        '    <rights rightsURI="https://creativecommons.org/licenses/by/4.0/legalcode" rightsIdentifierScheme="spdx" rightsIdentifier="cc-by-4.0">Creative Commons Attribution 4.0 International</rights>\n'  # noqa
        "  </rightsList>\n"
        "  <descriptions>\n"
        '    <description descriptionType="Abstract">A description \nwith HTML tags</description>\n'  # noqa
        '    <description descriptionType="Methods" xml:lang="eng">Bla bla bla</description>\n'  # noqa
        "  </descriptions>\n"
        "  <geoLocations>\n"
        "    <geoLocation>\n"
        "      <geoLocationPlace>test location place</geoLocationPlace>\n"
        "      <geoLocationPoint>\n"
        "        <pointLongitude>-60.63932</pointLongitude>\n"
        "        <pointLatitude>-32.94682</pointLatitude>\n"
        "      </geoLocationPoint>\n"
        "    </geoLocation>\n"
        "  </geoLocations>\n"
        "  <fundingReferences>\n"
        "    <fundingReference>\n"
        "      <funderName>European Commission</funderName>\n"
        '      <funderIdentifier funderIdentifierType="ROR">00k4n6c32</funderIdentifier>\n'  # noqa
        "      <awardNumber>755021</awardNumber>\n"
        "      <awardTitle>Personalised Treatment For Cystic Fibrosis Patients With Ultra-rare CFTR Mutations (and beyond)</awardTitle>\n"  # noqa
        "    </fundingReference>\n"
        "  </fundingReferences>\n"
        "</resource>\n"
    )

    record = {"_source": full_record}
    ser_rec = etree.tostring(datacite_etree(None, record), pretty_print=True)

    assert expected_value == ser_rec.decode("utf-8")


def test_oai_datacite_serializer(running_app, full_record):
    expected_value = (
        '<oai_datacite xmlns="http://schema.datacite.org/oai/oai-1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://schema.datacite.org/oai/oai-1.1/ http://schema.datacite.org/oai/oai-1.1/oai.xsd">\n'  # noqa
        "  <schemaVersion>4.3</schemaVersion>\n"
        "  <datacentreSymbol>TEST</datacentreSymbol>\n"
        "  <payload>\n"
        '    <resource xmlns="http://datacite.org/schema/kernel-4" xsi:schemaLocation="http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4.3/metadata.xsd">\n'  # noqa
        '      <identifier identifierType="DOI">10.5281/inveniordm.1234</identifier>\n'  # noqa
        "      <alternateIdentifiers>\n"
        '        <alternateIdentifier alternateIdentifierType="oai">oai:vvv.com:abcde-fghij</alternateIdentifier>\n'
        '        <alternateIdentifier alternateIdentifierType="bibcode">1924MNRAS..84..308E</alternateIdentifier>\n'  # noqa
        "      </alternateIdentifiers>\n"
        "      <creators>\n"
        "        <creator>\n"
        '          <creatorName nameType="Personal">Nielsen, Lars Holm</creatorName>\n'  # noqa
        "          <givenName>Lars Holm</givenName>\n"
        "          <familyName>Nielsen</familyName>\n"
        '          <nameIdentifier nameIdentifierScheme="ORCID">0000-0001-8135-3489</nameIdentifier>\n'  # noqa
        "          <affiliation>free-text</affiliation>\n"
        '          <affiliation affiliationIdentifier="https://ror.org/01ggx4157" affiliationIdentifierScheme="ROR">CERN</affiliation>\n'  # noqa
        "        </creator>\n"
        "      </creators>\n"
        "      <titles>\n"
        "        <title>InvenioRDM</title>\n"
        '        <title xml:lang="eng" titleType="Subtitle">a research data management platform</title>\n'  # noqa
        "      </titles>\n"
        "      <publisher>InvenioRDM</publisher>\n"
        "      <publicationYear>2018</publicationYear>\n"
        "      <subjects>\n"
        "        <subject>custom</subject>\n"
        '        <subject subjectScheme="MeSH">Abdominal Injuries</subject>\n'
        "      </subjects>\n"
        "      <contributors>\n"
        '        <contributor contributorType="Other">\n'
        '          <contributorName nameType="Personal">Nielsen, Lars Holm</contributorName>\n'  # noqa
        "          <givenName>Lars Holm</givenName>\n"
        "          <familyName>Nielsen</familyName>\n"
        '          <nameIdentifier nameIdentifierScheme="ORCID">0000-0001-8135-3489</nameIdentifier>\n'  # noqa
        '          <affiliation affiliationIdentifier="https://ror.org/01ggx4157" affiliationIdentifierScheme="ROR">CERN</affiliation>\n'  # noqa
        "        </contributor>\n"
        "      </contributors>\n"
        "      <dates>\n"
        '        <date dateType="Issued">2018/2020-09</date>\n'
        '        <date dateType="Other" dateInformation="A date">1939/1945</date>\n'  # noqa
        "      </dates>\n"
        "      <language>dan</language>\n"
        '      <resourceType resourceTypeGeneral="Image">Photo</resourceType>\n'  # noqa
        "      <relatedIdentifiers>\n"
        '        <relatedIdentifier relatedIdentifierType="DOI" relationType="IsCitedBy" resourceTypeGeneral="Dataset">10.1234/foo.bar</relatedIdentifier>\n'  # noqa
        "      </relatedIdentifiers>\n"
        "      <sizes>\n"
        "        <size>11 pages</size>\n"
        "      </sizes>\n"
        "      <formats>\n"
        "        <format>application/pdf</format>\n"
        "      </formats>\n"
        "      <version>v1.0</version>\n"
        "      <rightsList>\n"
        '        <rights rightsURI="https://customlicense.org/licenses/by/4.0/">A custom license</rights>\n'  # noqa
        '        <rights rightsURI="https://creativecommons.org/licenses/by/4.0/legalcode" rightsIdentifierScheme="spdx" rightsIdentifier="cc-by-4.0">Creative Commons Attribution 4.0 International</rights>\n'  # noqa
        "      </rightsList>\n"
        "      <descriptions>\n"
        '        <description descriptionType="Abstract">A description \nwith HTML tags</description>\n'  # noqa
        '        <description descriptionType="Methods" xml:lang="eng">Bla bla bla</description>\n'  # noqa
        "      </descriptions>\n"
        "      <geoLocations>\n"
        "        <geoLocation>\n"
        "          <geoLocationPlace>test location place</geoLocationPlace>\n"
        "          <geoLocationPoint>\n"
        "            <pointLongitude>-60.63932</pointLongitude>\n"
        "            <pointLatitude>-32.94682</pointLatitude>\n"
        "          </geoLocationPoint>\n"
        "        </geoLocation>\n"
        "      </geoLocations>\n"
        "      <fundingReferences>\n"
        "        <fundingReference>\n"
        "          <funderName>European Commission</funderName>\n"
        '          <funderIdentifier funderIdentifierType="ROR">00k4n6c32</funderIdentifier>\n'  # noqa
        "          <awardNumber>755021</awardNumber>\n"
        "          <awardTitle>Personalised Treatment For Cystic Fibrosis Patients With Ultra-rare CFTR Mutations (and beyond)</awardTitle>\n"  # noqa
        "        </fundingReference>\n"
        "      </fundingReferences>\n"
        "    </resource>\n"
        "  </payload>\n"
        "</oai_datacite>\n"
    )
    record = {"_source": full_record}
    ser_rec = etree.tostring(oai_datacite_etree(None, record), pretty_print=True)
    assert expected_value == ser_rec.decode("utf-8")


def test_oai_dcat_serializer(running_app, full_record):
    expected_value = (
        '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:adms="http://www.w3.org/ns/adms#" xmlns:bibo="http://purl.org/ontology/bibo/" xmlns:citedcat="https://w3id.org/citedcat-ap/" xmlns:dct="http://purl.org/dc/terms/" xmlns:dctype="http://purl.org/dc/dcmitype/" xmlns:dcat="http://www.w3.org/ns/dcat#" xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:gsp="http://www.opengis.net/ont/geosparql#" xmlns:locn="http://www.w3.org/ns/locn#" xmlns:org="http://www.w3.org/ns/org#" xmlns:owl="http://www.w3.org/2002/07/owl#" xmlns:prov="http://www.w3.org/ns/prov#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:skos="http://www.w3.org/2004/02/skos/core#" xmlns:vcard="http://www.w3.org/2006/vcard/ns#" xmlns:wdrs="http://www.w3.org/2007/05/powder-s#">\n'  # noqa
        '  <rdf:Description rdf:about="https://doi.org/10.5281/inveniordm.1234">\n'  # noqa
        '    <rdf:type rdf:resource="http://www.w3.org/ns/dcat#Dataset"/>\n'  # noqa
        '    <dct:type rdf:resource="http://purl.org/dc/dcmitype/Image"/>\n'  # noqa
        '    <dct:identifier rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">https://doi.org/10.5281/inveniordm.1234</dct:identifier>\n'  # noqa
        '    <foaf:page rdf:resource="https://doi.org/10.5281/inveniordm.1234"/>\n'  # noqa
        "    <dct:creator>\n"
        '      <rdf:Description rdf:about="https://orcid.org/0000-0001-8135-3489">\n'  # noqa
        '        <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>\n'  # noqa
        "        <foaf:name>Nielsen, Lars Holm</foaf:name>\n"
        "        <foaf:givenName>Lars Holm</foaf:givenName>\n"
        "        <foaf:familyName>Nielsen</foaf:familyName>\n"
        "        <org:memberOf>\n"
        "          <foaf:Organization>\n"
        "            <foaf:name>free-text</foaf:name>\n"
        "          </foaf:Organization>\n"
        "        </org:memberOf>\n"
        "        <org:memberOf>\n"
        '          <foaf:Organization rdf:about="https://ror.org/https://ror.org/01ggx4157">\n'  # noqa
        '            <dct:identifier rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">https://ror.org/01ggx4157</dct:identifier>\n'  # noqa
        "            <foaf:name>CERN</foaf:name>\n"
        "          </foaf:Organization>\n"
        "        </org:memberOf>\n"
        "      </rdf:Description>\n"
        "    </dct:creator>\n"
        "    <dct:title>InvenioRDM</dct:title>\n"
        "    <dct:publisher>\n"
        "      <foaf:Agent>\n"
        "        <foaf:name>InvenioRDM</foaf:name>\n"
        "      </foaf:Agent>\n"
        "    </dct:publisher>\n"
        '    <dct:issued rdf:datatype="http://www.w3.org/2001/XMLSchema#gYear">2018</dct:issued>\n'  # noqa
        "    <dcat:keyword>custom</dcat:keyword>\n"
        "    <dct:subject>\n"
        "      <skos:Concept>\n"
        "        <skos:prefLabel>Abdominal Injuries</skos:prefLabel>\n"
        "        <skos:inScheme>\n"
        "          <skos:ConceptScheme>\n"
        "            <dct:title>MeSH</dct:title>\n"
        "          </skos:ConceptScheme>\n"
        "        </skos:inScheme>\n"
        "      </skos:Concept>\n"
        "    </dct:subject>\n"
        "    <citedcat:isFundedBy>\n"
        "      <foaf:Project>\n"
        '        <dct:identifier rdf:datatype="http://www.w3.org/2001/XMLSchema#string">755021</dct:identifier>\n'  # noqa
        "        <dct:title>Personalised Treatment For Cystic Fibrosis Patients With Ultra-rare CFTR Mutations (and beyond)</dct:title>\n"
        '        <citedcat:isAwardedBy rdf:resource="https://ror.org/00k4n6c32"/>\n'  # noqa
        "      </foaf:Project>\n"
        "    </citedcat:isFundedBy>\n"
        '    <citedcat:funder rdf:resource="https://ror.org/00k4n6c32"/>\n'  # noqa
        "    <dct:contributor>\n"
        '      <rdf:Description rdf:about="https://orcid.org/0000-0001-8135-3489">\n'  # noqa
        '        <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>\n'  # noqa
        "        <foaf:name>Nielsen, Lars Holm</foaf:name>\n"
        "        <foaf:givenName>Lars Holm</foaf:givenName>\n"
        "        <foaf:familyName>Nielsen</foaf:familyName>\n"
        "        <org:memberOf>\n"
        '          <foaf:Organization rdf:about="https://ror.org/https://ror.org/01ggx4157">\n'  # noqa
        '            <dct:identifier rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">https://ror.org/01ggx4157</dct:identifier>\n'  # noqa
        "            <foaf:name>CERN</foaf:name>\n"
        "          </foaf:Organization>\n"
        "        </org:memberOf>\n"
        "      </rdf:Description>\n"
        "    </dct:contributor>\n"
        '    <dct:issued rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2018/2020-09</dct:issued>\n'  # noqa
        '    <dct:date rdf:datatype="http://www.w3.org/2001/XMLSchema#date">1939/1945</dct:date>\n'  # noqa
        '    <dct:language rdf:resource="http://publications.europa.eu/resource/authority/language/DAN"/>\n'  # noqa
        "    <adms:identifier>\n"
        "      <adms:Identifier>\n"
        "        <skos:notation>oai:vvv.com:abcde-fghij</skos:notation>\n"
        "        <adms:schemeAgency>oai</adms:schemeAgency>\n"
        "      </adms:Identifier>\n"
        "    </adms:identifier>\n"
        '    <owl:sameAs rdf:resource="http://adsabs.harvard.edu/abs/1924MNRAS..84..308E"/>\n'  # noqa
        "    <adms:identifier>\n"
        "      <adms:Identifier>\n"
        '        <skos:notation rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">http://adsabs.harvard.edu/abs/1924MNRAS..84..308E</skos:notation>\n'  # noqa
        "        <adms:schemeAgency>bibcode</adms:schemeAgency>\n"
        "      </adms:Identifier>\n"
        "    </adms:identifier>\n"
        "    <dct:isReferencedBy>\n"
        '      <rdf:Description rdf:about="https://doi.org/10.1234/foo.bar">\n'  # noqa
        "        <dct:identifier>https://doi.org/10.1234/foo.bar</dct:identifier>\n"
        '        <rdf:type rdf:resource="http://www.w3.org/ns/dcat#Dataset"/>\n'  # noqa
        '        <dct:type rdf:resource="http://purl.org/dc/dcmitype/Dataset"/>\n'  # noqa
        "      </rdf:Description>\n"
        "    </dct:isReferencedBy>\n"
        "    <owl:versionInfo>v1.0</owl:versionInfo>\n"
        "    <dct:description>A description with HTML tags</dct:description>\n"
        "    <dct:provenance>\n"
        "      <dct:ProvenanceStatement>\n"
        "        <rdfs:label>Bla bla bla</rdfs:label>\n"
        "      </dct:ProvenanceStatement>\n"
        "    </dct:provenance>\n"
        "    <dct:spatial>\n"
        "      <dct:Location>\n"
        '        <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>\n'  # noqa
        "        <skos:prefLabel>test location place</skos:prefLabel>\n"
        "        <locn:geographicName>test location place</locn:geographicName>\n"
        '        <dcat:centroid rdf:datatype="http://www.opengis.net/ont/geosparql#wktLiteral">POINT(-60.63932 -32.94682)</dcat:centroid>\n'  # noqa
        '        <dcat:centroid rdf:datatype="http://www.opengis.net/ont/geosparql#gmlLiteral">&lt;gml:Point srsName="http://www.opengis.net/def/crs/OGC/1.3/CRS84"&gt;&lt;gml:pos srsDimension="2"&gt;-60.63932 -32.94682&lt;/gml:pos&gt;&lt;/gml:Point&gt;</dcat:centroid>\n'  # noqa
        '        <dcat:centroid rdf:datatype="http://www.opengis.net/ont/geosparql#geoJSONLiteral">{"type":"Point","coordinates":[-60.63932,-32.94682]}</dcat:centroid>\n'  # noqa
        "      </dct:Location>\n"
        "    </dct:spatial>\n"
        "    <dcat:distribution>\n"
        "      <dcat:Distribution>\n"
        "        <dct:extent>\n"
        "          <dct:SizeOrDuration>\n"
        "            <rdfs:label>11 pages</rdfs:label>\n"
        "          </dct:SizeOrDuration>\n"
        "        </dct:extent>\n"
        '        <dcat:mediaType rdf:resource="https://www.iana.org/assignments/media-types/application/pdf"/>\n'  # noqa
        "        <dct:rights>\n"
        '          <dct:RightsStatement rdf:about="https://customlicense.org/licenses/by/4.0/">\n'  # noqa
        "            <rdfs:label>A custom license</rdfs:label>\n"
        "          </dct:RightsStatement>\n"
        "        </dct:rights>\n"
        '        <dct:license rdf:resource="https://creativecommons.org/licenses/by/4.0/legalcode"/>\n'  # noqa
        '        <dcat:accessURL rdf:resource="https://doi.org/10.5281/inveniordm.1234"/>\n'  # noqa
        "      </dcat:Distribution>\n"
        "    </dcat:distribution>\n"
        "  </rdf:Description>\n"
        "</rdf:RDF>\n"
    )
    record = {"_source": full_record}
    ser_rec = etree.tostring(oai_dcat_etree(None, record), pretty_print=True)
    assert expected_value == ser_rec.decode("utf-8")
