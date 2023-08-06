"""Output

- summary table
- duplicate passwords table
- weak passwords table
- http sites table
- enable2fa table
- emails table

To one of the following formats:

- ansi
- plain
- markdown
- json
- raw
- raw-csv
"""

import csv
import json
import re
from io import StringIO

from rich.console import Console
from rich.table import Table

from checkpasswords.credentials import Credentials, generateTables

INFO = {"program": "checkpasswords", "version": "2022"}


def _stripAnsi(string: str) -> str:
	"""Strip ansi codes from a given string

	Args:
		string (str): string to strip codes from

	Returns:
		str: plaintext, utf-8 string (safe for writing to files)
	"""
	return re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])").sub("", string)


def ansi(credentials: list[Credentials]) -> str:
	"""Format to ansi

	Args:
		credentials (list[Credentials]): list of credentials parsed from some input file.
		Such as a bitwarden export to CSV

	Returns:
		str: string to send to specified output in ansi format
	"""
	(
		duplicatePasswordsTable,
		weakPasswordsTable,
		httpSitesTable,
		enable2faTable,
		emailsTable,
	) = generateTables(credentials)

	string = StringIO()

	console = Console(file=string, color_system="truecolor")

	count = lambda x: f"[{'green' if len(x) < 2 else 'red'}]{len(x)-1}[/]"
	table = Table(title="\nSummary")
	table.add_column("Issue", style="cyan")
	table.add_column("No. Instances")
	table.add_row("Duplicate Passwords", count(duplicatePasswordsTable))
	table.add_row("Weak Passwords", count(weakPasswordsTable))
	table.add_row("HTTP Sites", count(httpSitesTable))
	table.add_row("Enable 2FA", count(enable2faTable))
	table.add_row("Emails", count(emailsTable))
	console.print(table)

	table = Table(title="\nDuplicate Passwords")
	table.add_column("Name", style="cyan")
	table.add_column("Username", style="magenta")
	table.add_column("Password", style="red")
	_ = [table.add_row(*x) for x in duplicatePasswordsTable[1:]]
	console.print(table)

	table = Table(title="\nWeak Passwords")
	table.add_column("Name", style="cyan")
	table.add_column("Username", style="magenta")
	table.add_column("Password", style="red")
	table.add_column("Score")
	table.add_column("Suggestion")
	scores = (
		"[black on red]Too Guessable[/]",
		"[black on yellow]Very Weak[/]",
		"[red]Weak[/]",
		"[yellow]Moderate[/]",
	)
	_ = [table.add_row(*x[:3], scores[int(x[3])], x[4]) for x in weakPasswordsTable[1:]]
	console.print(table)

	table = Table(title="\nHTTP Sites")
	table.add_column("Name", style="cyan")
	table.add_column("Username", style="magenta")
	_ = [table.add_row(*x) for x in httpSitesTable[1:]]
	console.print(table)

	table = Table(title="\nEnable 2FA")
	table.add_column("Name", style="cyan")
	table.add_column("Username", style="magenta")
	_ = [table.add_row(*x) for x in enable2faTable[1:]]
	console.print(table)

	table = Table(title="\nEmails")
	table.add_column("Emails", style="cyan")
	_ = [table.add_row(*x) for x in emailsTable[1:]]
	console.print(table)

	return string.getvalue()


def plainText(credentials: list[Credentials]) -> str:
	"""Format to plain text

	Args:
		credentials (list[Credentials]): list of credentials parsed from some input file.
		Such as a bitwarden export to CSV

	Returns:
		str: string to send to specified output in plain text format
	"""
	return _stripAnsi(ansi(credentials))


def markdown(credentials: list[Credentials]) -> str:
	"""Format to markdown

	Args:
		credentials (list[Credentials]): list of credentials parsed from some input file.
		Such as a bitwarden export to CSV

	Returns:
		str: string to send to specified output in markdown format
	"""
	strBuf = []
	(
		duplicatePasswordsTable,
		weakPasswordsTable,
		httpSitesTable,
		enable2faTable,
		emailsTable,
	) = generateTables(credentials)
	count = lambda x: len(x) - 1
	toTB = lambda z: "\n".join([f'|{"|".join([str(y) for y in x])}|' for x in z[1:]])

	strBuf.append("\nSummary\n|Issue|No. Instances|\n|:--|:--|")
	strBuf.append(f"|Duplicate Passwords|{count((duplicatePasswordsTable))}")
	strBuf.append(f"|Weak Passwords|{count((weakPasswordsTable))}")
	strBuf.append(f"|HTTP Sites|{count((httpSitesTable))}")
	strBuf.append(f"|Enable 2FA|{count((enable2faTable))}")
	strBuf.append(f"|Emails|{count((emailsTable))}")

	strBuf.append("\nDuplicate Passwords\n|Name|Username|Password|\n|:--|:--|:--|")
	strBuf.append(toTB(duplicatePasswordsTable))
	strBuf.append("\nWeak Passwords")
	strBuf.append("|Name|Username|Password|Score|Suggestion\n|:--|:--|:--|:--|:--|")
	strBuf.append(toTB(weakPasswordsTable))
	strBuf.append("\nHTTP Sites\n|Name|Username|\n|:--|:--")
	strBuf.append(toTB(httpSitesTable))
	strBuf.append("\nEnable 2FA\n|Name|Username|\n|:--|:--|")
	strBuf.append(toTB(enable2faTable))
	strBuf.append("\nEmails\n|Emails|\n|:--|")
	strBuf.append(toTB(emailsTable))

	return "\n".join(strBuf)


def jsonF(credentials: list[Credentials]) -> str:
	"""Format to json

	Args:
		credentials (list[Credentials]): list of credentials parsed from some input file.
		Such as a bitwarden export to CSV

	Returns:
		str: string to send to specified output in json format
	"""
	(
		duplicatePasswordsTable,
		weakPasswordsTable,
		httpSitesTable,
		enable2faTable,
		emailsTable,
	) = generateTables(credentials)
	count = lambda x: len(x) - 1
	toDict = lambda z: [{z[0][y]: x[y] for y, _ in enumerate(x)} for x in z[1:]]

	data = {
		"summary": {
			"duplicate_passwords": count(duplicatePasswordsTable),
			"weak_passwords": count(weakPasswordsTable),
			"http_sites": count(httpSitesTable),
			"enable_2fa": count(enable2faTable),
			"emails": count(emailsTable),
		},
		"duplicate_passwords": toDict(duplicatePasswordsTable),
		"weak_passwords": toDict(weakPasswordsTable),
		"http_sites": toDict(httpSitesTable),
		"enable_2fa": toDict(enable2faTable),
		"emails": toDict(emailsTable),
	}

	return json.dumps({"info": INFO, "data": data}, indent="\t")


def raw(credentials: list[Credentials]) -> str:
	"""Format to raw json

	Args:
		credentials (list[Credentials]): list of credentials parsed from some input file.
		Such as a bitwarden export to CSV

	Returns:
		str: string to send to specified output in raw json format
	"""
	return json.dumps({"info": INFO, "credentials": [x.__dict__ for x in credentials]}, indent="\t")


def rawCsv(credentials: list[Credentials]) -> str:
	"""Format to raw csv

	Args:
		credentials (list[Credentials]): list of credentials parsed from some input file.
		Such as a bitwarden export to CSV

	Returns:
		str: string to send to specified output in raw csv format
	"""
	string = StringIO()
	data = [x.__dict__ for x in credentials]
	writer = csv.DictWriter(string, fieldnames=list(data[0]), lineterminator="\n")
	writer.writeheader()
	writer.writerows(data)
	return string.getvalue()
