from upload import ROOT
from PyPDF2 import PdfFileMerger

WRITE_DIR = ROOT + "uploads"

def merge(pdfs):
	merger = PdfFileMerger(strict=False) # Enforcing strict=False allows us to avoid the 'xref not zero-indexed' error from scanned documents.
	app.logger.debug(f"Merging files...")

	for pdf in pdfs:
		try:
			merger.append(pdf)
		except:
			app.logger.warning(f"Error merging '{pdf}'. Operation cancelled.")
			return


	new_name = "new year new me" + ".pdf"
	# Trim to first 128 chars for filename?

	try:
		merger.write(WRITE_DIR + new_name)
	except:
		app.logger.debug("Error writing output file. Operation cancelled.")
		return

	app.logger.debug(f"Wrote to {WRITE_DIR + new_name}")

	merger.close()
	return
