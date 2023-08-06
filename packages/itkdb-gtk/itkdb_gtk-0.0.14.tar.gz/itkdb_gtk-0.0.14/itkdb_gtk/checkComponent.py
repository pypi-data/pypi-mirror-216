#!/usr/bin/env python3
"""Check children of DB component."""

try:
    import readAVSdata
    import ITkDBlogin
    import ITkDButils

    from dbGtkUtils import replace_in_container, DictDialog, ask_for_confirmation

except ModuleNotFoundError:
    from itkdb_gtk import readAVSdata, ITkDBlogin, ITkDButils
    from itkdb_gtk.dbGtkUtils import replace_in_container, DictDialog, ask_for_confirmation

import json


def ascii_complain(main_msg, secondary_msg=None):
    """Prints an error message

    Args:
    -----
        main (): Main message
        secondary (): Seconday message
    """
    print("**Error\n{}".format(main_msg))
    if secondary_msg:
        msg = secondary_msg.replace("\n", "\n\t")
        print("\t{}".format(msg))


def find_petal(session, SN, silent=False):
    """Finds petal with given SN."""
    try:
        petal_core = ITkDButils.get_DB_component(session, SN)

    except Exception as E:
        if not silent:
            ascii_complain("Could not find Petal Core in DB", str(E))

        petal_core = None
        return

    try:
        if petal_core["type"]["code"] != "CORE_AVS":
            ascii_complain("Wrong component type", "This is not an AVS petal core")

        # print(json.dumps(petal_core, indent=3))

    except KeyError:
        # Petal is not there
        petal_core = None

    return petal_core


def get_type(child):
    """Return object type

    Args:
    -----
        child (): object

    Returns
    -------
        str: object type

    """
    if child["type"] is not None:
        ctype = child["type"]["code"]
    else:
        ctype = child["componentType"]["code"]

    return ctype


def main():
    """Main entry point."""
    # ITk_PB authentication
    dlg = ITkDBlogin.ITkDBlogin()
    session = dlg.get_client()

    final_stage = {
        "BT_PETAL_FRONT": "COMPLETED",
        "BT_PETAL_BACK": "COMPLETED",
        "COOLING_LOOP_PETAL": "CLINCORE",
        "THERMALFOAMSET_PETAL": "IN_CORE"
    }

    # find all cores
    # Now all the objects
    payload = {
        "componentType": ["BT"],
        "componentType": ["CORE_PETAL"],
        "type": ["CORE_AVS"],
    }
    core_list = session.get("listComponents", json=payload)

    for obj in core_list:
        SN = obj["serialNumber"]
        id = obj['alternativeIdentifier']
        if "PPB" not in id:
            continue
        
        core = find_petal(session, SN)
        if core is None:
            print("SN: not a petal core.")
            continue

        location = core["currentLocation"]['code']
        stage = core["currentStage"]['code']
        if stage != "AT_QC_SITE":
            rc = ITkDButils.set_object_stage(session, SN, "AT_QC_SITE")
            if rc is not None:
                print("problems setting stage")

        if "children" not in core:
            ascii_complain("{}[{}]".format(SN, id), "Not assembled")
            continue

        print("Petal {} [{}] - {}. {}".format(SN, id, stage, location))
        clist = []
        for child in core["children"]:
            cstage = "Missing"
            if child["component"] is None:
                ctype = get_type(child)
                clist.append((ctype, cstage, None, None))

            else:
                SN = child["component"]["serialNumber"]
                ctype = get_type(child)
                cobj = ITkDButils.get_DB_component(session, child["component"]["id"])
                cstage = cobj["currentStage"]['code']
                if cstage != final_stage[ctype]:
                    rc = ITkDButils.set_object_stage(session, SN, final_stage[ctype])
                    if rc is not None:
                        cstage = final_stage[ctype]

                clocation = cobj["currentLocation"]['code']
                clist.append((ctype, cstage, SN, clocation))

        for item in clist:
            print("\t{} [{}] - {} at {}".format(item[2], item[0], item[1], item[3]))

        print()

    dlg.die()


if __name__ == "__main__":
    main()
