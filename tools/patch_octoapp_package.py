#!/usr/bin/env python3
"""Build the OpenKE OctoApp package without Moonraker-managed updates.

OpenKE installs OctoApp from an AppStore archive, not a Git checkout or Python
virtual environment. Upstream's generated git_repo updater configuration is
therefore invalid here. Keep its announcements subscription in the generated
Moonraker include while leaving package updates to OpenKE's AppStore.
"""

from pathlib import Path
from zipfile import ZipFile


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "packages" / "octoapp-v3.2.4.zip"
DESTINATION = REPO_ROOT / "packages" / "octoapp-v3.2.4-openke.2.zip"
MODULE = "moonraker_octoapp/systemconfigmanager.py"

OLD_START = "        # Special case for K1 and K1 max setups."
OLD_END = "        # Create the expected file path of our update config."
REPLACEMENT = '''        # OpenKE installs OctoApp from an AppStore archive, not a Git checkout
        # or a Python virtual environment. OpenKE's AppStore manages updates,
        # so only configure OctoApp announcements in Moonraker.
        expectedUpdateFileContent = \'''\\
[announcements]
subscriptions:
    octoapp.
\'''

'''

COMMENT_REPLACEMENTS = {
    '    c_updateConfigFileName = "octoapp-system.cfg"':
    '    c_updateConfigFileName = "octoapp-moonraker.cfg"',
    "    # We use config files to integrate into moonraker's update manager, which allows our plugin repo to stay updated.\n"
    "    # This also write a block that's used to allow the announcement system to show updates from our repo.\n"
    "    # This function ensures they exist and are up to date. If not, they are fixed.":
    "    # Keep OctoApp's announcement subscription in its Moonraker include.\n"
    "    # AppStore handles OpenKE package updates.",
    "        # Create the expected file path of our update config.":
    "        # Create the expected OctoApp config file path.",
    "        # Ensure that the main moonraker config file has the include for our sub config file":
    "        # Ensure that Moonraker includes the OctoApp config file.",
    '                    logger.info("Existing update config file found with the correct file contents.")':
    '                    logger.info("Existing OctoApp config file has the expected contents.")',
    '        logger.info("No update config found or it was out of date, writing a new file.")':
    '        logger.info("Writing the OctoApp announcements config file.")',
    "        # Whenever we update the file on disk, also restart moonraker so that it reads it and\n"
    "        # pull the update information into the update manager. It's safe to restart moonraker during a print\n"
    "        # so this won't effect anything.":
    "        # Restart Moonraker so it reloads the announcements config.",
    '        logger.info("No config file was found on disk, so we are going to attempt to restart moonraker.")':
    '        logger.info("Attempting to restart Moonraker after updating its config.")',
}

LEGACY_CLEANUP_METHOD = '''    @staticmethod
    def _removeLegacyUpdateConfigFile(klipperConfigDir:str, logger:LoggerLike):
        legacyConfigName = "octoapp-system.cfg"
        moonrakerConfigFilePath = os.path.join(klipperConfigDir, "moonraker.conf")

        if os.path.isfile(moonrakerConfigFilePath):
            try:
                with open(moonrakerConfigFilePath, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                newLines = []
                changed = False
                for line in lines:
                    stripped = line.strip()
                    if stripped.lower().startswith("[include ") and stripped.endswith("]"):
                        includeTarget = stripped[len("[include "):-1].strip().strip("\\\"'")
                        if os.path.basename(includeTarget) == legacyConfigName:
                            changed = True
                            continue
                    newLines.append(line)
                if changed:
                    with open(moonrakerConfigFilePath, "w", encoding="utf-8") as file:
                        file.writelines(newLines)
                    logger.info("Removed legacy OctoApp config include from moonraker.conf.")
            except Exception as e:
                logger.warning("Failed to remove legacy OctoApp config include. " + str(e))

        legacyConfigPath = os.path.join(klipperConfigDir, legacyConfigName)
        if os.path.isfile(legacyConfigPath):
            try:
                os.remove(legacyConfigPath)
                logger.info("Removed legacy OctoApp config file.")
            except Exception as e:
                logger.warning("Failed to remove legacy OctoApp config file. " + str(e))

'''


def main() -> None:
    with ZipFile(SOURCE, "r") as source_zip:
        original_module = source_zip.read(MODULE).decode("utf-8")
        start = original_module.index(OLD_START)
        end = original_module.index(OLD_END, start)
        patched_module = original_module[:start] + REPLACEMENT + original_module[end:]
        for old_text, new_text in COMMENT_REPLACEMENTS.items():
            if old_text not in patched_module:
                raise ValueError(f"Expected OctoApp source text was not found: {old_text[:60]!r}")
            patched_module = patched_module.replace(old_text, new_text, 1)

        include_setup = (
            "        # Ensure that Moonraker includes the OctoApp config file.\n"
            "        SystemConfigManager._ensureMoonrakerConfigHasUpdateConfigInclude(klipperConfigDir, logger)"
        )
        include_setup_with_migration = (
            "        # Remove the previous OpenKE config filename and its include before migrating.\n"
            "        SystemConfigManager._removeLegacyUpdateConfigFile(klipperConfigDir, logger)\n\n"
            + include_setup
        )
        if include_setup not in patched_module:
            raise ValueError("Expected Moonraker include setup was not found in OctoApp source")
        patched_module = patched_module.replace(include_setup, include_setup_with_migration, 1)

        helper_anchor = "    @staticmethod\n    def _ensureMoonrakerConfigHasUpdateConfigInclude("
        if helper_anchor not in patched_module:
            raise ValueError("Expected Moonraker include helper was not found in OctoApp source")
        patched_module = patched_module.replace(helper_anchor, LEGACY_CLEANUP_METHOD + helper_anchor, 1)

        with ZipFile(DESTINATION, "w") as patched_zip:
            for entry in source_zip.infolist():
                contents = (
                    patched_module.encode("utf-8")
                    if entry.filename == MODULE
                    else source_zip.read(entry.filename)
                )
                patched_zip.writestr(entry, contents)

    print(f"Wrote {DESTINATION}")


if __name__ == "__main__":
    main()
