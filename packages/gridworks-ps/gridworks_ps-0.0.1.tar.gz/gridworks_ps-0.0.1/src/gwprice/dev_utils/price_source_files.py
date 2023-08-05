caiso_file_prefix = "input_data/electricity_prices/caiso/"
isone_file_prefix = "input_data/electricity_prices/isone/"
ng_file_prefix = "input_data/electricity_prices/ng/"


###################################################
# ENTER REAL TIME ELECTRICITY PRICE SOURCES FILES HERE
###################################################
def get_eprt_sync_uid_by_source_file():
    eprt_source_uid_by_file = {}

    eprt_source_uid_by_file[
        caiso_file_prefix + "eprt__w.caiso.n15__2020__gw.up50.csv"
    ] = "0c3c167d-fa6d-4ebc-969e-1ffe808c9eb6"
    eprt_source_uid_by_file[
        caiso_file_prefix
        + "eprt__w.caiso.n15__2018__caisoenergyonline.from5min.dubious.csv"
    ] = "4c96665c-21c4-4e28-8ef2-d87a0192d3d5"
    eprt_source_uid_by_file[
        caiso_file_prefix
        + "eprt__w.caiso.n15__2019__caisoenergyonline.from5min.dubious.csv"
    ] = "e37ada67-de50-45a0-996d-de29e91428f9"
    eprt_source_uid_by_file[
        caiso_file_prefix + "eprt__w.caiso.n15__2019__gw.stdev.up200.csv"
    ] = "60785ab7-f3e0-449b-a352-67a66db6ee19"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.4001__2019.csv"
    ] = "9f8e9dd1-ac19-41eb-b95d-0e482df7919e"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.4001__2020.csv"
    ] = "dd84a579-9737-47d9-bf02-7a089e9c656f"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.4001__2021.csv"
    ] = "df3f8137-7787-4ac5-abd9-ae1b705379e1"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.4001__2022.csv"
    ] = "d1a301bf-0a62-41b3-ade2-57dc4fe16235"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.stetson__2020.csv"
    ] = "4cfba22e-fa07-43ea-a7e4-a8babb4f7bcc"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.stetson__2021.csv"
    ] = "d9d102a6-0392-4a23-9bdc-aad9a3bccd33"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.stetson__2022.csv"
    ] = "66b3435d-7784-4b1b-94db-0115a19f1df3"
    eprt_source_uid_by_file[
        isone_file_prefix
        + "eprt__w.isone.4008__2019__gw.da.predicted.rolling4wks.alpha.csv"
    ] = "e080f0c7-cebc-4cb1-b032-e77004fec11b"
    eprt_source_uid_by_file[
        ng_file_prefix + "eprt__w.ng__20210825.csv"
    ] = "3907f438-aa82-4d51-a243-8739e0d382fe"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.4001_DAnotRT__2020.csv"
    ] = "3907f438-aa82-4d51-a243-8739e0d382f1"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.stetson__gwpathwaysalpha__2020.csv"
    ] = "ed40f2c4-524c-4329-9d9f-fcac2c18d663"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.stetson__gwpathwaysalpha__2022.csv"
    ] = "298f3170-90c6-42dd-8cb1-a7c820ad7409"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.stetson__gwpathwaysbeta__2020.csv"
    ] = "cd82637b-5535-4228-b087-c76637547277"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.stetson__gwpathwaysbeta__2021.csv"
    ] = "1b77cd4f-bd76-4c2c-8ed7-2e6870982bd2"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.stetson__gwpathwaysbeta__2022.csv"
    ] = "2c1ee59c-de41-4855-8476-7a2ef0e9f9f5"
    eprt_source_uid_by_file[
        isone_file_prefix + "eprt__w.isone.suroweic__2019.csv"
    ] = "4cfba22e-fa07-43fa-a7e4-a8babb4f7bcc"
    eprt_uids = []
    for key in eprt_source_uid_by_file.keys():
        if eprt_source_uid_by_file[key] in eprt_uids:
            raise Exception(
                f"file {key} has duplicate uid {eprt_source_uid_by_file[key]}!"
            )
        else:
            eprt_uids.append(eprt_source_uid_by_file[key])
    return eprt_source_uid_by_file


###################################################
# ENTER NEW REGULATION PRICE SOURCES FILES HERE
###################################################
def get_regp_sync_uid_by_source_file():
    regp_uid_by_source_file = {}

    regp_uid_by_source_file[
        isone_file_prefix + "regp__w.isone__2019.csv"
    ] = "2a77bbaa-d860-41f4-a040-f9cd6375b593"

    regp_uids = []
    for key in regp_uid_by_source_file.keys():
        if regp_uid_by_source_file[key] in regp_uids:
            raise Exception(
                f"file {key} has duplicate uid {regp_uid_by_source_file[key]}!"
            )
        else:
            regp_uids.append(regp_uid_by_source_file[key])
    return regp_uid_by_source_file


###################################################
# ENTER NEW ONEPRICE DISTRIBUTION PRICE SOURCES FILES HERE
###################################################
def get_distp_oneprice_uid_by_source_file():
    distp_oneprice_uid_by_source_file = {}

    distp_oneprice_uid_by_source_file[
        caiso_file_prefix + "distp__w.caiso.n15.rcea__2019__gw.ca.rcea.oneprice.csv"
    ] = "c916408a-7528-4591-8e71-7e0314456b33"

    distp_uids = []
    for key in distp_oneprice_uid_by_source_file.keys():
        if distp_oneprice_uid_by_source_file[key] in distp_uids:
            raise Exception(
                f"file {key} has duplicate uid {distp_oneprice_uid_by_source_file[key]}!"
            )
        else:
            distp_uids.append(distp_oneprice_uid_by_source_file[key])
    return distp_oneprice_uid_by_source_file


###################################################
# ENTER NEW MULTI-PRICE DISTRIBUTION PRICE SOURCES FILES HERE
###################################################
def get_distp_sync_uid_by_source_file():
    distp_sync_uid_by_source_file = {}
    distp_sync_uid_by_source_file[
        isone_file_prefix + "distp__w.isone.stetson__2020__gw.me.versant.a1.res.ets.csv"
    ] = "78ca8f20-7024-4178-8cf9-bfafc3813cad"
    distp_sync_uid_by_source_file[
        isone_file_prefix + "distp__w.isone.stetson__2021__gw.me.versant.a1.res.ets.csv"
        ] = "b7d96b56-9e9d-4f3a-92bb-bd90c0907f6e"
    distp_sync_uid_by_source_file[
        isone_file_prefix + "distp__w.isone.stetson__2022__gw.me.versant.a1.res.ets.csv"
        ] = "43949171-3561-475b-86bc-42280c3b63f7"
    distp_sync_uid_by_source_file[
        caiso_file_prefix + "distp__w.caiso.n15.rcea__2018__gw.ca.rcea.offpeak1.csv"
    ] = "243bcd06-c8b6-4c81-83a9-47e3b82da267"
    distp_sync_uid_by_source_file[
        caiso_file_prefix + "distp__w.caiso.n15.rcea__2019__gw.ca.rcea.offpeak1.csv"
    ] = "16391f17-84b2-4a19-b676-a48bdeef4682"

    distp_uids = []
    for key in distp_sync_uid_by_source_file.keys():
        if distp_sync_uid_by_source_file[key] in distp_uids:
            raise Exception(
                f"file {key} has duplicate uid {distp_sync_uid_by_source_file[key]}!"
            )
        else:
            distp_uids.append(distp_sync_uid_by_source_file[key])
    return distp_sync_uid_by_source_file


###################################################
# ENTER NEW DAY AHEAD ELECTRICITY PRICE SOURCES FILES HERE
###################################################
def get_epda_uid_by_source_file():
    epda_uid_by_source_file = {}

    epda_uid_by_source_file[
        isone_file_prefix + "epda__w.isone.4001__2019.csv"
    ] = "34da361f-bc38-4fbd-b78c-355e7f098b75"
    epda_uid_by_source_file[
        isone_file_prefix + "epda__w.isone.4001__2020.csv"
    ] = "460e588a-c57b-4e18-a926-fa3f7e8f2646"

    epda_uids = []
    for key in epda_uid_by_source_file.keys():
        if epda_uid_by_source_file[key] in epda_uids:
            raise Exception(
                f"file {key} has duplicate uid {epda_uid_by_source_file[key]}!"
            )
        else:
            epda_uids.append(epda_uid_by_source_file[key])
    return epda_uid_by_source_file


def get_eprt_sync_source_file_by_uid():
    eprt_uid_by_source_file = get_eprt_sync_uid_by_source_file()
    eprt_sync_source_file_by_uid = {}
    for key in eprt_uid_by_source_file.keys():
        eprt_sync_source_file_by_uid[eprt_uid_by_source_file[key]] = key
    return eprt_sync_source_file_by_uid


def get_regp_sync_source_file_by_uid():
    regp_uid_by_source_file = get_regp_sync_uid_by_source_file()
    regp_sync_source_file_by_uid = {}
    for key in regp_uid_by_source_file.keys():
        regp_sync_source_file_by_uid[regp_uid_by_source_file[key]] = key
    return regp_sync_source_file_by_uid


def get_distp_oneprice_source_file_by_uid():
    distp_oneprice_uid_by_source_file = get_distp_oneprice_uid_by_source_file()
    distp_source_file_by_uid = {}
    for key in distp_oneprice_uid_by_source_file.keys():
        distp_source_file_by_uid[distp_oneprice_uid_by_source_file[key]] = key
    return distp_source_file_by_uid


def get_distp_sync_source_file_by_uid():
    distp_sync_uid_by_source_file = get_distp_sync_uid_by_source_file()
    distp_source_file_by_uid = {}
    for key in distp_sync_uid_by_source_file.keys():
        distp_source_file_by_uid[distp_sync_uid_by_source_file[key]] = key
    return distp_source_file_by_uid


def get_epda_source_file_by_uid():
    epda_uid_by_source_file = get_epda_uid_by_source_file()
    epda_source_file_by_uid = {}
    for key in epda_uid_by_source_file.keys():
        epda_source_file_by_uid[epda_uid_by_source_file[key]] = key
    return epda_source_file_by_uid
