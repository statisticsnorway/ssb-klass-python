import requests

from klass import KlassConfig


def base_request(content: str, status_code: int = 200) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response._content = bytes(
        content,
        "utf8",
    )
    response.request = requests.PreparedRequest()
    response.request.headers = KlassConfig().HEADERS
    return response


def classifications_fake_content():
    return base_request(
        """{"_embedded": {"classifications": [{"name": "Standard for mocking tests",
    "classificationType": "Klassifikasjon",
    "lastModified": "2023-04-18T12:56:21.000+0000",
    "_links": {"self": {"href": "https://data.ssb.no/api/klass/v1/classifications/0"}}},
   ]},
 "_links": {"first": {"href": "https://data.ssb.no/api/klass/v1/classifications?includeCodelists=false&page=0&size=20"},
  "self": {"href": "https://data.ssb.no/api/klass/v1/classifications?includeCodelists=false"},
  "next": {"href": "https://data.ssb.no/api/klass/v1/classifications?includeCodelists=false&page=0&size=20"},
  "last": {"href": "https://data.ssb.no/api/klass/v1/classifications?includeCodelists=false&page=0&size=20"},
  "search": {"href": "https://data.ssb.no/api/klass/v1/classifications/search{?query,includeCodelists}",
   "templated": true}},
 "page": {"size": 20, "totalElements": 1, "totalPages": 1, "number": 0}}"""
    )


def classification_search_fake_content():
    return base_request(
        """{"_embedded": {"searchResults": [{"name": "Standard for mocking tests",
    "snippet": "<strong>1</strong> - Mann 2 - Kvinne",
    "searchScore": 1.1026883125305176,
    "_links": {"self": {"href": "https://data.ssb.no/api/klass/v1/classifications/0"}}}]},
 "_links": {"first": {"href": "https://data.ssb.no/api/klass/v1/classifications/search?query=1&includeCodelists=false&page=0&size=20"},
  "self": {"href": "https://data.ssb.no/api/klass/v1/classifications/search?query=1&includeCodelists=false"},
  "next": {"href": "https://data.ssb.no/api/klass/v1/classifications/search?query=1&includeCodelists=false&page=0&size=20"},
  "last": {"href": "https://data.ssb.no/api/klass/v1/classifications/search?query=1&includeCodelists=false&page=0&size=20"}},
 "page": {"size": 20, "totalElements": 1, "totalPages": 1, "number": 0}}"""
    )


def classification_by_id_fake_content():
    return base_request(
        """{"name": "Standard for mocking tests",
 "classificationType": "Klassifikasjon",
 "lastModified": "2023-04-18T12:56:21.000+0000",
 "description": "",
 "primaryLanguage": "en",
 "copyrighted": false,
 "includeShortName": false,
 "includeNotes": true,
 "contactPerson": {"name": "SSB Pythonistas",
  "email": "pythonistas@ssb.no",
  "phone": "99999999"},
 "owningSection": "320 - Seksjon for befolkningsstatistikk",
 "statisticalUnits": ["Mock"],
 "versions": [{"name": "Mock Version",
   "validFrom": "2016-01-01",
   "validTo": "2050-01-01",
   "lastModified": "2023-04-18T12:43:39.000+0000",
   "published": ["en"],
   "_links": {"self": {"href": "https://data.ssb.no/api/klass/v1/versions/0"}}}],
 "_links": {"self": {"href": "https://data.ssb.no/api/klass/v1/classifications/0"},
  "codes": {"href": "https://data.ssb.no/api/klass/v1/classifications/0/codes{?from=<yyyy-MM-dd>,to=<yyyy-MM-dd>,csvSeparator,level,selectCodes,presentationNamePattern}",
   "templated": true},
  "codesAt": {"href": "https://data.ssb.no/api/klass/v1/classifications/0/codesAt{?date=<yyyy-MM-dd>,csvSeparator,level,selectCodes,presentationNamePattern}",
   "templated": true},
  "variant": {"href": "https://data.ssb.no/api/klass/v1/classifications/0/variant{?variantName,from=<yyyy-MM-dd>,to=<yyyy-MM-dd>,csvSeparator,level,selectCodes,presentationNamePattern}",
   "templated": true},
  "variantAt": {"href": "https://data.ssb.no/api/klass/v1/classifications/0/variantAt{?variantName,date=<yyyy-MM-dd>,csvSeparator,level,selectCodes,presentationNamePattern}",
   "templated": true},
  "corresponds": {"href": "https://data.ssb.no/api/klass/v1/classifications/0/corresponds{?targetClassificationId,from=<yyyy-MM-dd>,to=<yyyy-MM-dd>,csvSeparator}",
   "templated": true},
  "correspondsAt": {"href": "https://data.ssb.no/api/klass/v1/classifications/0/correspondsAt{?targetClassificationId,date=<yyyy-MM-dd>,csvSeparator}",
   "templated": true},
  "changes": {"href": "https://data.ssb.no/api/klass/v1/classifications/0/changes{?from=<yyyy-MM-dd>,to=<yyyy-MM-dd>,csvSeparator}",
   "templated": true}}}"""
    )


def codes_fake_content():
    return base_request(
        '"code","parentCode","level","name","shortName","presentationName","validFrom","validTo","validFromInRequestedRange","validToInRequestedRange","notes"\n"1",,"1","Mann","","",,,"2023-01-01",,""\n"2",,"1","Kvinne","","",,,"2023-01-01",,""\n'
    )


def codes_at_fake_content():
    return base_request(
        '"code","parentCode","level","name","shortName","presentationName","validFrom","validTo","notes"\n"1",,"1","Mann","","",,,""\n"2",,"1","Kvinne","","",,,""\n'
    )


def version_by_id_fake_content():
    return base_request(
        '{"name":"Sivilstand 1993","validFrom":"1993-01-01","lastModified":"2016-10-07T12:06:18.000+0000","published":["nb","nn","en"],"introduction":"Denne klassifiserngen av sivilstand er brukt i befolkningsstatistikken fra 1993.","contactPerson":{"name":"Nordmann, Ola","email":"Ola.Nordmann@ssb.no","phone":"9999999"},"owningSection":"320 - Seksjon for befolkningsstatistikk","legalBase":"","publications":"html","derivedFrom":"","correspondenceTables":[{"name":"Sivilstand 1993 - Sivilstand 1964","contactPerson":{"name":"Nordmann, Ola","email":"Ola.Nordmann@ssb.no","phone":"9999999"},"owningSection":"320 - Seksjon for befolkningsstatistikk","source":"Sivilstand 1993","sourceId":50,"target":"Sivilstand 1964","targetId":51,"changeTable":true,"lastModified":"2019-06-04T08:37:54.000+0000","published":["nb","nn","en"],"sourceLevel":null,"targetLevel":null,"_links":{"self":{"href":"https://data.ssb.no/api/klass/v1/correspondencetables/447"},"source":{"href":"https://data.ssb.no/api/klass/v1/versions/50"},"target":{"href":"https://data.ssb.no/api/klass/v1/versions/51"}}}],"classificationVariants":[],"changelogs":[],"levels":[{"levelNumber":1,"levelName":"Sivilstand"}],"classificationItems":[{"code":"1","parentCode":"","level":"1","name":"Ugift","shortName":null,"notes":null},{"code":"2","parentCode":"","level":"1","name":"Gift","shortName":null,"notes":null},{"code":"3","parentCode":"","level":"1","name":"Enke/enkemann","shortName":null,"notes":null},{"code":"4","parentCode":"","level":"1","name":"Skilt","shortName":null,"notes":null},{"code":"5","parentCode":"","level":"1","name":"Separert","shortName":null,"notes":null},{"code":"6","parentCode":"","level":"1","name":"Registrert partner","shortName":null,"notes":null},{"code":"7","parentCode":"","level":"1","name":"Separert partner","shortName":null,"notes":null},{"code":"8","parentCode":"","level":"1","name":"Skilt partner","shortName":null,"notes":null},{"code":"9","parentCode":"","level":"1","name":"Gjenlevende partner","shortName":null,"notes":null}],"_links":{"self":{"href":"https://data.ssb.no/api/klass/v1/versions/50"}}}'
    )


def variant_fake_content():
    return base_request(
        '"code","parentCode","level","name","shortName","presentationName","validFrom","validTo","validFromInRequestedRange","validToInRequestedRange","notes"\n"05",,"1","05","","",,,"2023-01-01",,""\n"05",,"1","05","","",,,"2023-01-01",,""\n"10",,"1","10","","",,,"2023-01-01",,""\n"10",,"1","10","","",,,"2023-01-01",,""\n"10",,"1","10","","",,,"2023-01-01",,""\n"10",,"1","Fagskolepoeng","","",,,"2023-01-01",,""\n"12",,"1","12","","",,,"2023-01-01",,""\n"12",,"1","12","","",,,"2023-01-01",,""\n"120",,"1","120","","",,,"2023-01-01",,""\n"120",,"1","120","","",,,"2023-01-01",,""\n"120",,"1","120","","",,,"2023-01-01",,""\n"120",,"1","120","","",,,"2023-01-01",,""\n"15",,"1","15","","",,,"2023-01-01",,""\n"15",,"1","15","","",,,"2023-01-01",,""\n"15",,"1","15","","",,,"2023-01-01",,""\n"15",,"1","15","","",,,"2023-01-01",,""\n"24",,"1","24","","",,,"2023-01-01",,""\n"24",,"1","24","","",,,"2023-01-01",,""\n"30",,"1","30","","",,,"2023-01-01",,""\n"30",,"1","30","","",,,"2023-01-01",,""\n"30",,"1","30","","",,,"2023-01-01",,""\n"30",,"1","30","","",,,"2023-01-01",,""\n"36",,"1","36","","",,,"2023-01-01",,""\n"36",,"1","36","","",,,"2023-01-01",,""\n"36",,"1","36","","",,,"2023-01-01",,""\n"36",,"1","36","","",,,"2023-01-01",,""\n"40",,"1","40","","",,,"2023-01-01",,""\n"40",,"1","40","","",,,"2023-01-01",,""\n"40",,"1","40","","",,,"2023-01-01",,""\n"40",,"1","40","","",,,"2023-01-01",,""\n"45",,"1","45","","",,,"2023-01-01",,""\n"45",,"1","45","","",,,"2023-01-01",,""\n"45",,"1","45","","",,,"2023-01-01",,""\n"45",,"1","45","","",,,"2023-01-01",,""\n"5",,"1","5","","",,,"2023-01-01",,""\n"514110","120","2","Fagskoleutdanning, Frelsesarmeens offiserutdanning, toårig","","",,,"2023-01-01",,'
    )


def variant_at_fake_content():
    return base_request(
        '"code","parentCode","level","name","shortName","presentationName","validFrom","validTo","notes"\n"05",,"1","05","","",,,""\n"05",,"1","05","","",,,""\n"10",,"1","10","","",,,""\n"10",,"1","10","","",,,""\n"10",,"1","10","","",,,""\n"10",,"1","Fagskolepoeng","","",,,""\n"12",,"1","12","","",,,""\n"12",,"1","12","","",,,""\n"120",,"1","120","","",,,""\n"120",,"1","120","","",,,""\n"120",,"1","120","","",,,""\n"120",,"1","120","","",,,""\n"15",,"1","15","","",,,""\n"15",,"1","15","","",,,""\n"15",,"1","15","","",,,""\n"15",,"1","15","","",,,""\n"24",,"1","24","","",,,""\n"24",,"1","24","","",,,""\n"30",,"1","30","","",,,""\n"30",,"1","30","","",,,""\n"30",,"1","30","","",,,""\n"30",,"1","30","","",,,""\n"36",,"1","36","","",,,""\n"36",,"1","36","","",,,""\n"36",,"1","36","","",,,""\n"36",,"1","36","","",,,""\n"40",,"1","40","","",,,""\n"40",,"1","40","","",,,""\n"40",,"1","40","","",,,""\n"40",,"1","40","","",,,""\n"45",,"1","45","","",,,""\n"45",,"1","45","","",,,""\n"45",,"1","45","","",,,""\n"45",,"1","45","","",,,""\n"5",,"1","5","","",,,""\n"514110","120","2","Fagskoleutdanning, Frelsesarmeens offiserutdanning, toårig","","",,,""'
    )


def variants_by_id_fake_content():
    return base_request(
        '{"name":"Klassetrinn 2023-01 2023  - variant av Utdanningsgruppering (NUS) 2023","contactPerson":{"name":"Nordmann, Ola","email":"Ola.Nordmann@ssb.no","phone":"99999999"},"owningSection":"360 - Seksjon for utdannings- og kulturstatistikk","lastModified":"2023-01-19T14:18:18.000+0000","published":["nb","nn","en"],"validFrom":"2023-01-01","introduction":"Vi kan skille mellom klassetrinn for enkeltutdanninger og klassetrinn for samlekoder. Enkeltutdanningene har forhåndsbestemte klassetrinn, mens de som har tatt utdanning som faller inn under samlekodene vil befinne seg på ulike klassetrinn. Klassetrinn regnes fra nivå 1 (barneskoleutdanning), hvor første året i grunnskolen er klassetrinn 01. Nivåene 1 og 2 utgjør klassetrinn 01 - 10. Første år etter obligatorisk grunnskole (nivå 3) blir således 11. klassetrinn osv. Høyeste klassetrinn er 22 (forskerutdanning).","correspondenceTables":[],"changelogs":[],"levels":[{"levelNumber":1,"levelName":"Nivå 1"},{"levelNumber":2,"levelName":"Nivå 2"}],"classificationItems":[{"code":"01-07","parentCode":"","level":"1","name":"Fra-til klassetrinn","shortName":null,"notes":null},{"code":"01-08","parentCode":"","level":"1","name":"Fra-til klassetrinn","shortName":null,"notes":null},{"code":"08-10","parentCode":"","level":"1","name":"Fra-til klassetrinn","shortName":null,"notes":null},{"code":"899999","parentCode":"20-22","level":"2","name":"Forskerutdanning, uspesifisert fagfelt","shortName":null,"notes":null}],"_links":{"self":{"href":"https://data.ssb.no/api/klass/v1/variants/1965"}}}'
    )


def corresponds_fake_content():
    return base_request(
        '"sourceCode","sourceName","sourceShortName","targetCode","targetName","targetShortName","validFrom","validTo"\n"03","Oslo","","03001","Oslo","","2023-01-01",\n"11","Rogaland","","11001","Dalane","","2023-01-01",\n"11","Rogaland","","11002","Stavanger/Sandnes","","2023-01-01",\n"11","Rogaland","","11003","Jæren","","2023-01-01",\n"11","Rogaland","","11004","Indre Ryfylke","","2023-01-01",\n"11","Rogaland","","11005","Haugaland","","2023-01-01",\n"15","Møre og Romsdal","","15001","Ørsta/Volda","","2023-01-01",\n"15","Møre og Romsdal","","15002","Søre Sunnmøre","","2023-01-01",\n"15","Møre og Romsdal","","15003","Ålesund","","2023-01-01"'
    )


def corresponds_at_fake_content():
    return base_request(
        '"sourceCode","sourceName","sourceShortName","targetCode","targetName","targetShortName"\n"03","Oslo","","03001","Oslo",""\n"11","Rogaland","","11001","Dalane",""\n"11","Rogaland","","11002","Stavanger/Sandnes",""\n"11","Rogaland","","11003","Jæren",""\n"11","Rogaland","","11004","Indre Ryfylke",""\n"11","Rogaland","","11005","Haugaland",""\n"15","Møre og Romsdal","","15001","Ørsta/Volda",""\n"15","Møre og Romsdal","","15002","Søre Sunnmøre",""\n"15","Møre og Romsdal","","15003","Ålesund",""\n"15","Møre og Romsdal","","15004","Ålesund omland",""\n"15","Møre og Romsdal","","15005","Molde",""'
    )


def correspondance_table_by_id_fake_content():
    return base_request(
        '{"name":"Fylkesinndeling 2022 - Økonomiske regioner 2020","contactPerson":{"name":"Nordmann, Ola","email":"Ola.Nordmann@ssb.no","phone":"99999999"},"owningSection":"320 - Seksjon for befolkningsstatistikk","source":"Fylkesinndeling 2022","sourceId":2108,"target":"Økonomiske regioner 2020","targetId":1308,"changeTable":false,"lastModified":"2023-04-04T07:38:04.000+0000","published":["nb","nn","en"],"sourceLevel":null,"targetLevel":null,"description":"","changelogs":[],"correspondenceMaps":[{"sourceCode":"03","sourceName":"Oslo","targetCode":"03001","targetName":"Oslo"},{"sourceCode":"11","sourceName":"Rogaland","targetCode":"11001","targetName":"Dalane"},{"sourceCode":"11","sourceName":"Rogaland","targetCode":"11002","targetName":"Stavanger/Sandnes"},{"sourceCode":"11","sourceName":"Rogaland","targetCode":"11003","targetName":"Jæren"},{"sourceCode":"54","sourceName":"Troms og Finnmark - Romsa ja Finnmárku - Tromssa ja Finmarkku","targetCode":"54007","targetName":"Øst-Finnmark"}],"_links":{"self":{"href":"https://data.ssb.no/api/klass/v1/correspondencetables/1287"},"source":{"href":"https://data.ssb.no/api/klass/v1/versions/2108"},"target":{"href":"https://data.ssb.no/api/klass/v1/versions/1308"}}}'
    )


def changes_fake_content():
    return base_request(
        '"oldCode","oldName","oldShortName","newCode","newName","newShortName","changeOccurred"\n"355112","Elektrofag, Vg1","","355112","Elektro og datateknologi, Vg1","","2022-05-01"\n"355113","Elektrofag, Vg1, grunnkompetanse","","355113","Elektro og datateknologi, Vg1, grunnkompetanse","","2022-05-01"\n"355901","Teknikk og industriell produksjon, Vg1","","355901","Teknologi- og industrifag, Vg1","","2022-05-01"\n"355902","Teknikk og industriell produksjon med studiespesialisering, Vg2","","355902","Teknologi- og industrifag med studiespesialisering, Vg2","","2022-05-01"\n,,,"737910","Master of Laws (LL.M.) Programme in EU and EEA Law","","2022-10-01"\n"741154","Master in Sustainability Management (MBA), 1½-årig","","741154","Master, Sustainability Management, toårig","","2022-10-01"\n'
    )


def classificationfamilies_fake_content():
    return base_request(
        '{"_embedded":{"classificationFamilies":[{"name":"Utdanning","numberOfClassifications":5,"_links":{"self":{"href":"https://data.ssb.no/api/klass/v1/classificationfamilies/20"}}}]},"_links":{"self":{"href":"https://data.ssb.no/api/klass/v1/classificationfamilies?includeCodelists=false&language=nb&ssbSection=360+-+Seksjon+for+utdannings-+og+kulturstatistikk"}}}'
    )


def classificationfamilies_by_id_fake_content():
    return base_request(
        '{"name":"Utdanning","classifications":[{"name":"Standard for utdanningsgruppering (NUS)","classificationType":"Klassifikasjon","lastModified":"2023-03-29T08:58:03.000+0000","_links":{"self":{"href":"https://data.ssb.no/api/klass/v1/classifications/36"}}}],"_links":{"self":{"href":"https://data.ssb.no/api/klass/v1/classificationfamilies/20"}}}'
    )


def sections_fake_content():
    return base_request(
        '{"_embedded":{"ssbSections":[{"name":"160 - Seksjon for eiendom, arkiv og administrative systemer"},{"name":"210 - Seksjon for nasjonalregnskap"},{"name":"211 - Seksjon for finansregnskap"},{"name":"212 - Seksjon for offentlige finanser"},{"name":"213 - Seksjon for finansmarkedsstatistikk"},{"name":"214 - Seksjon for utenrikshandel"},{"name":"240 - Seksjon for prisstatistikk"},{"name":"312 - Seksjon for arbeidsmarked og lønnsstatistikk"},{"name":"320 - Seksjon for befolkningsstatistikk"},{"name":"330 - Seksjon for helse-, omsorg- og sosialstatistikk"},{"name":"350 - Seksjon for inntekts- og levekårsstatistikk"},{"name":"360 - Seksjon for utdannings- og kulturstatistikk"},{"name":"421 - Seksjon for Fou, teknologi og næringslivets utvikling"},{"name":"422 - Seksjon for næringslivets konjunkturer"},{"name":"423 - Seksjon for næringslivets strukturer"},{"name":"424 - Seksjon for regnskapsstatistikk og VoF"},{"name":"425 - Seksjon for energi, miljø- og transportstatistikk"},{"name":"425 - Seksjon for energi- miljø og transportstatistikk"},{"name":"426 - Seksjon for eiendom-, areal- og primærnæringsstatistikk"},{"name":"426 - Seksjon for eiendoms-, areal- og primærnæringsstatistikk"},{"name":"610 - Seksjon for redaksjon og publisering"},{"name":"702 - Seksjon for IT-arkitektur"},{"name":"703 - Seksjon for IT-partner"},{"name":"821 - Seksjon for næringslivsundersøkelser"},{"name":"Befolkningsstatistikk"}]},"_links":{"self":{"href":"https://data.ssb.no/api/klass/v1/ssbsections"}}}'
    )
