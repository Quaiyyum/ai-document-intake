# Sources

Every real document used in this project, so the corpus can be rebuilt. The files themselves are
third-party material and are not committed (`data/raw/` is gitignored).

## Tender notices (real, public)

Source: NZ Government Electronic Tenders Service, https://www.gets.govt.nz/

Each file is the public notice page printed to PDF into `data/raw/tender/`. The `agency` column holds
the GETS agency code from the URL. `retrieved` and `sha256` are filled in once the files are saved.

    python -m src.fetch_docs --print    # print any missing notice page to PDF (needs Google Chrome)
    python -m src.fetch_docs            # verify the files and write data/raw/manifest.csv

| doc_id | url | agency | retrieved | file_name | sha256 |
| --- | --- | --- | --- | --- | --- |
| GETS-2026-0001 | https://www.gets.govt.nz/NZTAHNO/ExternalTenderDetails.htm?id=35030310 | NZTAHNO | | tender_35030310.pdf | |
| GETS-2026-0002 | https://www.gets.govt.nz/NZTAHNO/ExternalTenderDetails.htm?id=35111110 | NZTAHNO | | tender_35111110.pdf | |
| GETS-2026-0003 | https://www.gets.govt.nz/NZTAHNO/ExternalTenderDetails.htm?id=34870463 | NZTAHNO | | tender_34870463.pdf | |
| GETS-2026-0004 | https://www.gets.govt.nz/MEDUR/ExternalTenderDetails.htm?id=35035327 | MEDUR | | tender_35035327.pdf | |
| GETS-2026-0005 | https://www.gets.govt.nz/KRG/ExternalTenderDetails.htm?id=34960103 | KRG | | tender_34960103.pdf | |
| GETS-2026-0006 | https://www.gets.govt.nz/ORC/ExternalTenderDetails.htm?id=35092357 | ORC | | tender_35092357.pdf | |
| GETS-2026-0007 | https://www.gets.govt.nz/MPI/ExternalTenderDetails.htm?id=34962605 | MPI | | tender_34962605.pdf | |
| GETS-2026-0008 | https://www.gets.govt.nz/MSD/ExternalTenderDetails.htm?id=32705858 | MSD | | tender_32705858.pdf | |
| GETS-2026-0009 | https://www.gets.govt.nz/NPDC/ExternalTenderDetails.htm?id=34911428 | NPDC | | tender_34911428.pdf | |
| GETS-2026-0010 | https://www.gets.govt.nz/NPDC/ExternalTenderDetails.htm?id=34921850 | NPDC | | tender_34921850.pdf | |
| GETS-2026-0011 | https://www.gets.govt.nz/UW/ExternalTenderDetails.htm?id=34891545 | UW | | tender_34891545.pdf | |
| GETS-2026-0012 | https://www.gets.govt.nz/UW/ExternalTenderDetails.htm?id=35090813 | UW | | tender_35090813.pdf | |
| GETS-2026-0013 | https://www.gets.govt.nz/UW/ExternalTenderDetails.htm?id=35068879 | UW | | tender_35068879.pdf | |
| GETS-2026-0014 | https://www.gets.govt.nz/AT/ExternalTenderDetails.htm?id=34761285 | AT | | tender_34761285.pdf | |
| GETS-2026-0015 | https://www.gets.govt.nz/AT/ExternalTenderDetails.htm?id=34842108 | AT | | tender_34842108.pdf | |
| GETS-2026-0016 | https://www.gets.govt.nz/NZIST/ExternalTenderDetails.htm?id=34924335 | NZIST | | tender_34924335.pdf | |
| GETS-2026-0017 | https://www.gets.govt.nz/NZIST/ExternalTenderDetails.htm?id=34924423 | NZIST | | tender_34924423.pdf | |
| GETS-2026-0018 | https://www.gets.govt.nz/DIA/ExternalTenderDetails.htm?id=23700412 | DIA | | tender_23700412.pdf | |
| GETS-2026-0019 | https://www.gets.govt.nz/DIA/ExternalTenderDetails.htm?id=33732411 | DIA | | tender_33732411.pdf | |
| GETS-2026-0020 | https://www.gets.govt.nz/MEDUR/ExternalTenderDetails.htm?id=32504269 | MEDUR | | tender_32504269.pdf | |
| GETS-2026-0021 | https://www.gets.govt.nz/WAIMDC/ExternalTenderDetails.htm?id=31377530 | WAIMDC | | tender_31377530.pdf | |
| GETS-2026-0022 | https://www.gets.govt.nz/EECA/ExternalTenderDetails.htm?id=29898765 | EECA | | tender_29898765.pdf | |
| GETS-2026-0023 | https://www.gets.govt.nz/EECA/ExternalTenderDetails.htm?id=31232412 | EECA | | tender_31232412.pdf | |
| GETS-2026-0024 | https://www.gets.govt.nz/HEALTHNZ/ExternalTenderDetails.htm?id=35147829 | HEALTHNZ | | tender_35147829.pdf | |
| GETS-2026-0025 | https://www.gets.govt.nz/WaikDC/ExternalTenderDetails.htm?id=34645793 | WaikDC | | tender_34645793.pdf | |
| GETS-2026-0026 | https://www.gets.govt.nz/MEDU/ExternalTenderDetails.htm?id=35116860 | MEDU | | tender_35116860.pdf | |
| GETS-2026-0027 | https://www.gets.govt.nz/HEALTHNZ/ExternalTenderDetails.htm?id=35098594 | HEALTHNZ | | tender_35098594.pdf | |
| GETS-2026-0028 | https://www.gets.govt.nz/TCDC/ExternalTenderDetails.htm?id=34992673 | TCDC | | tender_34992673.pdf | |
| GETS-2026-0029 | https://www.gets.govt.nz/TASDC/ExternalTenderDetails.htm?id=35010726 | TASDC | | tender_35010726.pdf | |
| GETS-2026-0030 | https://www.gets.govt.nz/WAIDC/ExternalTenderDetails.htm?id=35045167 | WAIDC | | tender_35045167.pdf | |
| GETS-2026-0031 | https://www.gets.govt.nz/WAIDC/ExternalTenderDetails.htm?id=35127157 | WAIDC | | tender_35127157.pdf | |
| GETS-2026-0032 | https://www.gets.govt.nz/HCC/ExternalTenderDetails.htm?id=35129419 | HCC | | tender_35129419.pdf | |
| GETS-2026-0033 | https://www.gets.govt.nz/MBIE/ExternalTenderDetails.htm?id=34908926 | MBIE | | tender_34908926.pdf | |
| GETS-2026-0034 | https://www.gets.govt.nz/MD/ExternalTenderDetails.htm?id=33830698 | MD | | tender_33830698.pdf | |
| GETS-2026-0035 | https://www.gets.govt.nz/MSD/ExternalTenderDetails.htm?id=35034968 | MSD | | tender_35034968.pdf | |
| GETS-2026-0036 | https://www.gets.govt.nz/AC/ExternalTenderDetails.htm?id=35056284 | AC | | tender_35056284.pdf | |
| GETS-2026-0037 | https://www.gets.govt.nz/AURORA/ExternalTenderDetails.htm?id=33266797 | AURORA | | tender_33266797.pdf | |
| GETS-2026-0038 | https://www.gets.govt.nz/ACC/ExternalTenderDetails.htm?id=29971844 | ACC | | tender_29971844.pdf | |
| GETS-2026-0039 | https://www.gets.govt.nz/ACC/ExternalTenderDetails.htm?id=31338623 | ACC | | tender_31338623.pdf | |
| GETS-2026-0040 | https://www.gets.govt.nz/PCO/ExternalTenderDetails.htm?id=34538513 | PCO | | tender_34538513.pdf | |
| GETS-2026-0041 | https://www.gets.govt.nz/QLDC/ExternalTenderDetails.htm?id=35091767 | QLDC | | tender_35091767.pdf | |
| GETS-2026-0042 | https://www.gets.govt.nz/QLDC/ExternalTenderDetails.htm?id=34733646 | QLDC | | tender_34733646.pdf | |
| GETS-2026-0043 | https://www.gets.govt.nz/MFAT/ExternalTenderDetails.htm?id=34134620 | MFAT | | tender_34134620.pdf | |
| GETS-2026-0044 | https://www.gets.govt.nz/WSL/ExternalTenderDetails.htm?id=35091453 | WSL | | tender_35091453.pdf | |
| GETS-2026-0045 | https://www.gets.govt.nz/MPI/ExternalTenderDetails.htm?id=33832412 | MPI | | tender_33832412.pdf | |
| GETS-2026-0046 | https://www.gets.govt.nz/CCC/ExternalTenderDetails.htm?id=33694604 | CCC | | tender_33694604.pdf | |
| GETS-2026-0047 | https://www.gets.govt.nz/GRYDC/ExternalTenderDetails.htm?id=34865819 | GRYDC | | tender_34865819.pdf | |
| GETS-2026-0048 | https://www.gets.govt.nz/GDC/ExternalTenderDetails.htm?id=34708070 | GDC | | tender_34708070.pdf | |
| GETS-2026-0049 | https://www.gets.govt.nz/TEC/ExternalTenderDetails.htm?id=34939478 | TEC | | tender_34939478.pdf | |
| GETS-2026-0050 | https://www.gets.govt.nz/HBRC/ExternalTenderDetails.htm?id=35008398 | HBRC | | tender_35008398.pdf | |

## Loan application form (real blank layout, fictional content)

To be added at checkpoint H4.

## Real-estate enquiries (fictional, script-written)

Written by `python -m src.make_fictional_leads`. No source document; every detail is made up.
