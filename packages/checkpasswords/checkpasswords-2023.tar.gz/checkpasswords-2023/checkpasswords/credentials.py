"""Credentials class and associated methods
"""
import re
from collections import Counter
from dataclasses import dataclass, field

from checkpasswords.auxiliary import (
	ZxcvbnScore,
	isHttp,
	isMfaAvailable,
	isMfaEnabled,
	passwordPrint,
	zxcvbnScore,
)


@dataclass
class Credentials:  # pylint: disable=too-many-instance-attributes
	"""Credentials storing raw data from IO and inferred data such as:
	- zxcvbnScore
	- isPasswordDuplicate
	- passwordPrint
	- isHttp
	- isMfaAvailable
	- isMfaEnabled

	Used to:
	- check for duplicate passwords
	- check for weak passwords
	- identify http sites
	- list available 2fa options using data from https://2fa.directory/
	"""

	name: str
	urls: list[str]
	username: str
	password: str
	notes: str
	otpauth: str
	zxcvbnScore: ZxcvbnScore = field(init=False)
	isPasswordDuplicate: bool = field(init=False)
	passwordPrint: str = field(init=False)
	isHttp: bool = field(init=False)
	isMfaAvailable: bool = field(init=False)
	isMfaEnabled: bool = field(init=False)

	def __post_init__(self):
		"""Populate/ update various attributes using auxiliary functions"""
		self.username = self.username.strip()
		urlstr = " ".join(self.urls).lower()
		self.zxcvbnScore = zxcvbnScore(self.password)
		self.isPasswordDuplicate = False
		self.passwordPrint = passwordPrint(self.password)
		self.isHttp = isHttp(urlstr)
		self.isMfaAvailable = isMfaAvailable(urlstr)
		self.isMfaEnabled = len(self.otpauth) > 0 or isMfaEnabled(self.notes)
		self.instructEnableMfa = self.isMfaAvailable and not self.isMfaEnabled


def applyPasswordDuplicate(credentials: list[Credentials]):
	"""Apply duplicate password flag to each credentials

	Args:
		credentials (list[Credentials]): list of all credentials
	"""
	duplicates = [
		k for k, v in Counter([x.password for x in credentials]).items() if v > 1 and len(k) > 0
	]
	for cred in credentials:
		cred.isPasswordDuplicate = cred.password in duplicates


def emails(credentials: list[Credentials]) -> set[str]:
	"""Return a set of unique emails from the list of credentials

	Args:
		credentials (list[Credentials]): list of all credentials

	Returns:
		set[str]: set of unique emails
	"""
	return {x.username.lower() for x in credentials if re.match(r"[^@]+@[^@]+\.[^@]+", x.username)}


def orderCredentials(credentials: list[Credentials]) -> list[Credentials]:
	"""Order credentials by password crack time

	Args:
		credentials (list[Credentials]): list of credentials parsed from some input file.
		Such as a bitwarden export to CSV

	Returns:
		list[Credentials]: sorted credentials
	"""
	return sorted(credentials, key=lambda x: x.zxcvbnScore["crack_time"])


def generateTables(credentials: list[Credentials]) -> tuple[list[tuple[str, ...]], ...]:
	"""generateTables

	Args:
		credentials (list[Credentials]): list of credentials parsed from some input file.
		Such as a bitwarden export to CSV
	"""
	credentials = orderCredentials(credentials)
	applyPasswordDuplicate(credentials)

	duplicatePasswordsTable = [("Name", "Username", "Password")] + [
		(cred.name, cred.username, cred.passwordPrint)
		for cred in credentials
		if cred.isPasswordDuplicate
	]

	weakPasswordsTable = [("Name", "Username", "Password", "Score", "Suggestion")] + [
		(
			cred.name,
			cred.username,
			cred.passwordPrint,
			str(cred.zxcvbnScore["score"]),
			cred.zxcvbnScore["suggestions"],
		)
		for cred in credentials
		if -1 < cred.zxcvbnScore["score"] < 4
	]

	httpSitesTable = [("Name", "Username")] + [
		(cred.name, cred.username) for cred in credentials if cred.isHttp
	]

	enable2faTable = [("Name", "Username")] + [
		(cred.name, cred.username) for cred in credentials if cred.instructEnableMfa
	]

	emailsTable = [("Emails",)] + [(email,) for email in sorted(emails(credentials))]

	return duplicatePasswordsTable, weakPasswordsTable, httpSitesTable, enable2faTable, emailsTable
