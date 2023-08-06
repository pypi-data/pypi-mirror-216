from finbourne_lab.luminesce import CoreLumiLab, DriveLumiLab
from finbourne_lab.luminesce.lusid.lusid_read import LusidLumiLabRead


def make_shopper(atlas, verbose=False, skip_checks=False):
    """Make a shopper object that runs all measurements in all LumiLab classes in finbourne_lab.luminesce.

    Args:
        atlas (Atlas): the lumipy atlas to run luminesce queries with.
        verbose (bool): whether to run in verbose mode. This will give feedback on ensure (entity) steps
        during running. Defaults to false.
        skip_checks (bool): whether to skip ensure (instruments/portfolios/holdings/txns). Defaults to false.

    Returns:
        Shopper: constructed lumi shopper instance.
    """

    core = CoreLumiLab(atlas, verbose)
    drive = DriveLumiLab(atlas, verbose)
    lusid_read = LusidLumiLabRead(atlas, verbose, skip_checks)

    core_shopper = core.shopper()
    drive_shopper = drive.shopper()
    lusid_read_shopper = lusid_read.shopper()

    return core_shopper + drive_shopper + lusid_read_shopper
