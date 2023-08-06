"""checkpasswords: Uses pass_import to read a password manager source file storing raw
data and infers data such as:

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
- list emails to submit to HIBP or similar
"""

import argparse
from sys import stdout

from pass_import.__main__ import MANAGERS

from checkpasswords.io import input as input_
from checkpasswords.io import output


def main():
	"""Main entry point."""
	outputMap = {
		"ansi": output.ansi,
		"plain": output.plainText,
		"markdown": output.markdown,
		"json": output.jsonF,
		"raw": output.raw,
		"raw-csv": output.rawCsv,
	}
	parser = argparse.ArgumentParser(
		description=__doc__, formatter_class=argparse.RawTextHelpFormatter
	)
	parser.add_argument(
		"credentials",
		help="Credentials/ passwords file to check",
	)
	parser.add_argument(
		"--output-format",
		"-o",
		help=f"""
Output format. One of {list(outputMap)}. default=ansi""".replace(
			"\n", ""
		),
	)
	parser.add_argument(
		"--input-format",
		"-i",
		help=f"""
Input format. One of {MANAGERS.names()}""".replace(
			"\n", ""
		),
	)
	parser.add_argument(
		"--file",
		"-f",
		help="Filename to write to (omit for stdout)",
	)
	parser.add_argument(
		"--no-colour",
		"-z",
		help="No ANSI colours",
		action="store_true",
	)

	args = parser.parse_args()
	# File
	filename = (
		stdout
		if args.file is None
		else open(args.file, "w", encoding="utf-8")  # pylint: disable=consider-using-with
	)

	outputFunction = outputMap.get(args.output_format, output.ansi)
	# no_colour
	if outputFunction == output.ansi and args.no_colour:  # pylint: disable=comparison-with-callable
		outputFunction = output.plainText

	print(
		outputFunction(input_.passImport(args.credentials, args.input_format)),
		file=filename,
	)


if __name__ == "__main__":
	main()
