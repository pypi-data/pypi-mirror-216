"""Auxiliary functions used by the credentials class
"""
import math
import re
from pathlib import Path
from typing import TypedDict

from zxcvbn import zxcvbn

THISDIR = str(Path(__file__).resolve().parent)


class ZxcvbnScore(TypedDict):
	"""ZxcvbnScore is a dict containing the following attributes:

	- score: int
	- suggestions: str
	- crack_time: float
	"""

	score: int
	suggestions: str
	crack_time: float


def isMfaEnabled(notes: str) -> bool:
	"""Use the notes field to determine if MFA has been enabled

	Args:
		notes (str): notes field

	Returns:
		bool: isMfaEnabled
	"""

	patterns = [
		r"[2m]fa.*?enabled",
		r"authenticated.*?x\d*",
		r"sms.*?[2m]fa",
		r"text.*?[2m]fa",
		r"[2m]fa.*?sms",
		r"[2m]fa.*?text",
		r"\w.*?authenticat",
		"aegis",
		"otp",
		"authy",
		"keepass",
		"duo",
	]

	return re.search("|".join(patterns), notes, re.I) is not None


def isHttp(urlstr: str) -> bool:
	"""Use the urls field to determine if http is used instead of https

	Args:
		urlstr (str): urlstr field

	Returns:
		bool: isHttp
	"""
	return "http:" in urlstr


def entropyLen(string: str):
	"""Calculates the Shannon entropy * length of a string"""
	prob = [string.count(c) / len(string) for c in set(string)]
	entropy = -sum(p * math.log(p) / math.log(2.0) for p in prob)
	return entropy * len(string)


def zxcvbnScore(password: str) -> ZxcvbnScore:
	"""Calculate a ZxcvbnScore from a password

	Args:
		password (str): password

	Returns:
		ZxcvbnScore: Return a dict of type ZxcvbnScore
	"""
	try:
		scores = zxcvbn(password)
	except IndexError:
		return {"score": -1, "suggestions": "Add a password", "crack_time": -1}
	return {
		"score": int(scores["score"] + entropyLen(password) / 50),
		"suggestions": " ".join(scores["feedback"]["suggestions"]),
		"crack_time": float(scores["crack_times_seconds"]["offline_slow_hashing_1e4_per_second"])
		/ 100,
	}


def passwordPrint(password: str) -> str:
	"""Output a password whilst obfuscating details

	Args:
		password (str): raw password

	Returns:
		str: obfuscated password
	"""
	if len(password) < 7:
		return "*" * len(password)
	return password[:2] + ("*" * (len(password) - 4)) + password[-2:]


MFA = Path(f"{THISDIR}/mfa_sites.txt").read_text(encoding="utf-8").splitlines()


def isMfaAvailable(urlstr: str) -> bool:
	"""Identify if mfa is available using data from https://2fa.directory/

	Args:
		urlstr (str): urlstr field

	Returns:
		bool: isMfaAvailable
	"""
	return any(ele in urlstr for ele in MFA)
