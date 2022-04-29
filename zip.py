import zipfile


# files = ["output_data/sac_report_maintanance_jobs.csv"]
files = ["temp_files/df.csv"]
archive = "output_data/sac_report_maintanance_jobs.zip"


with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for file in files:
        zf.write(file)


