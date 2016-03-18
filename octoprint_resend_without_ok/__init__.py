# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import logging

logger = logging.getLogger("octoprint.plugins." + __name__)

PROBLEMATIC_VERSION = "1.2.10"

class ResendWithoutOkPlugin(octoprint.plugin.SettingsPlugin):

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			resend_without_ok=dict(
				displayName=self._plugin_name,
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="OctoPrint",
				repo="OctoPrint-ResendWithoutOk",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/OctoPrint/OctoPrint-ResendWithoutOk/archive/{target_version}.zip"
			)
		)

# ~ helpers

def _octoprint_version_matches(target):
	from octoprint import __version__
	return __version__ and (__version__ == target or
	                        __version__.startswith(target + "+") or
	                        __version__.startswith(target + "-") or
	                        __version__.startswith(target + "."))


def _monkey_patch_resend_handler():
	from octoprint.util.comm import MachineCom

	original_resend_handler = MachineCom._handleResendRequest
	def new_resend_handler(self, *args, **kwargs):
		result = original_resend_handler(self, *args, **kwargs)
		self._handle_ok()
		return result
	MachineCom._handleResendRequest = new_resend_handler

# ~ plugin registration

__plugin_name__ = "Resend without ok support"

if not _octoprint_version_matches(PROBLEMATIC_VERSION):
	__plugin_name__ += " (can be uninstalled now)"
	__plugin_description__ = "Since you are not running OctoPrint {}, this plugin is non-functional and can be uninstalled.".format(PROBLEMATIC_VERSION)


def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ResendWithoutOkPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}


def __plugin_enable__():
	# we do the monkey patching in the plugin enable handler since
	# we need to make sure to monkey patch MachineCom before its
	# imported anywhere else

	if _octoprint_version_matches(PROBLEMATIC_VERSION):
		logger.info("Monkey patching resend handler of communication layer to emulate an extra ok")
		_monkey_patch_resend_handler()
	else:
		logger.info("Not monkey patching the resend handler for extra ok's, this OctoPrint version doesn't need that")

