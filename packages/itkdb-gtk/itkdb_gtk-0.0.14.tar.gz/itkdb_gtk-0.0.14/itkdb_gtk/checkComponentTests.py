#!/usr/bin/env python3
"""Check children of DB component."""

try:
    import ITkDBlogin
    import ITkDButils

    from dbGtkUtils import replace_in_container, DictDialog, ask_for_confirmation

except ModuleNotFoundError:
    from itkdb_gtk import ITkDBlogin, ITkDButils
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

    # find all cores
    # Now all the objects
    payload = {
        "componentType": ["BT"],
        "componentType": ["CORE_PETAL"],
        "type": ["CORE_AVS"],
        "currentLocation": "IFIC"
    }
    core_list = session.get("listComponents", json=payload)

    for core in core_list:
        SN = core["serialNumber"]
        id = core['alternativeIdentifier']
        if "PPB" not in id:
            continue

        location = core["currentLocation"]['code']
        stage = core["currentStage"]['code']
        print("Petal {} [{}] - {}. {}".format(SN, id, stage, location))

        # get list of tests
        test_list = session.get("listTestRunsByComponent", json={"component": SN})
        for tst in test_list:
            ttype = tst["testType"]["code"]
            inst = tst["institution"]["code"]
            stage = tst["stage"]["code"]
            print("\t{:<18} {:<16} {:>8} {:>3} {}".format(ttype, stage, inst, tst["runNumber"], tst["date"][:10]))

        print()

    dlg.die()


if __name__ == "__main__":
    main()
