"""Use pass_import to convert an ambiguous password manager source file to a list[Credentials]
"""
import sys

from pass_import.__main__ import pass_import
from pass_import.auto import AutoDetect
from pass_import.tools import Config

from ..credentials import Credentials


def passImport(path: str, manager: str | None = None) -> list[Credentials]:
	"""Use pass_import to convert an ambiguous source file to a list[Credentials]

	Args:
		path (str): path to password source file
		manager (str, optional): specify a pasword manager if pass_import fails to identify it.
		Defaults to None.

	Returns:
		list[Credentials]: list of credentials used by the rest of checkpasswords
	"""
	# Use pass_import to convert an ambiguous source file to a list[Credentials]
	conf = Config()
	conf.readconfig(
		{
			"sroot": "",
		}
	)
	detect = AutoDetect(settings=conf.getsettings())
	passManager = detect.manager(path)
	if passManager is None:
		if manager:
			detect = AutoDetect(manager, settings=conf.getsettings())
			passManager = detect.format(path)
		else:
			print(" [x] Error: Must specify input_format e.g. -i bitwarden")
			sys.exit(1)
	conf["in"] = path
	conf["importer"] = passManager.name
	data = pass_import(conf, passManager)

	if data is None:
		raise RuntimeError(
			f"Failed to handle password file from {path} (password_manager={manager})"
		)

	return transformPass(data)


def transformPass(data: list[dict]) -> list[Credentials]:
	"""Convert pass_import representation to checkpasswords representation (list[Credentials])


	:param dict list[dict]: pass_import representation
	:return list[Credentials]: checkpasswords representation
	"""
	credentials = []
	for row in data:
		credentials.append(
			Credentials(
				name=row["title"],
				urls=[
					x
					for x in ([row.get("url")] + [row.get(f"url{y}") for y in range(10)])
					if x is not None
				],
				username=row.get("login", ""),
				password=row.get("password", ""),
				notes=row.get("comments", ""),
				otpauth=row.get("otpauth", ""),
			)
		)
	return credentials
