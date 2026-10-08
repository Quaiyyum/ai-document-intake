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
| GETS-2026-0001 | https://www.gets.govt.nz/NZTAHNO/ExternalTenderDetails.htm?id=35030310 | NZTAHNO | 2026-10-09 | tender_35030310.pdf | 58e2219e992f65831a82706e0971abd8cac6e50e14c42009f6f2461c4ad09443 |
| GETS-2026-0002 | https://www.gets.govt.nz/NZTAHNO/ExternalTenderDetails.htm?id=35111110 | NZTAHNO | 2026-10-09 | tender_35111110.pdf | bf4c91e47cf1af964c2242c721a671168f009327703b22d1eb7f205175611dc2 |
| GETS-2026-0003 | https://www.gets.govt.nz/NZTAHNO/ExternalTenderDetails.htm?id=34870463 | NZTAHNO | 2026-10-09 | tender_34870463.pdf | 5c6375bd83c4c2627948f690a15b1aec40781132475aba560de6373fd917927d |
| GETS-2026-0004 | https://www.gets.govt.nz/MEDUR/ExternalTenderDetails.htm?id=35035327 | MEDUR | 2026-10-09 | tender_35035327.pdf | f5ea189616085577d270b0711905c739ea810b9db2664ae697be7d49d0ca41d5 |
| GETS-2026-0005 | https://www.gets.govt.nz/KRG/ExternalTenderDetails.htm?id=34960103 | KRG | 2026-10-09 | tender_34960103.pdf | a9958e81e8209785e95cc63b206e641da083dd63992b5ba89e0a5b80f1bf0744 |
| GETS-2026-0006 | https://www.gets.govt.nz/ORC/ExternalTenderDetails.htm?id=35092357 | ORC | 2026-10-09 | tender_35092357.pdf | 9872f377043fe18c45ed72c2d9c04af9dc4cbf508ff7d7fe109bc316edeba5f8 |
| GETS-2026-0007 | https://www.gets.govt.nz/MPI/ExternalTenderDetails.htm?id=34962605 | MPI | 2026-10-09 | tender_34962605.pdf | 1a33973b4b4d20b1bc211db88fdea530f9f5026e7b253240906c8d0b3c2a9927 |
| GETS-2026-0008 | https://www.gets.govt.nz/MSD/ExternalTenderDetails.htm?id=32705858 | MSD | 2026-10-09 | tender_32705858.pdf | e8840dab9a4ceeff2e052c75ae60cd5c95e2bdb090dc956c6c1a88abf138bdb3 |
| GETS-2026-0009 | https://www.gets.govt.nz/NPDC/ExternalTenderDetails.htm?id=34911428 | NPDC | 2026-10-09 | tender_34911428.pdf | ac74638c33e20eca8ac8929b17a15b05ada44134a3a873c094d1f059fd899190 |
| GETS-2026-0010 | https://www.gets.govt.nz/NPDC/ExternalTenderDetails.htm?id=34921850 | NPDC | 2026-10-09 | tender_34921850.pdf | a2e20379da46d0c093a621fbb10173b98a96be62e92cbfc7841707e37363a4d5 |
| GETS-2026-0011 | https://www.gets.govt.nz/UW/ExternalTenderDetails.htm?id=34891545 | UW | 2026-10-09 | tender_34891545.pdf | 3d8a3a0d343a5b7f4a64aa33a7e4114c8f5f299704a7afbe7ed44acf12f8bd29 |
| GETS-2026-0012 | https://www.gets.govt.nz/UW/ExternalTenderDetails.htm?id=35090813 | UW | 2026-10-09 | tender_35090813.pdf | 81fbaf655a1bb42c455c11b99b8253eb4eaf2e19b853fea6197a28c1b46f6644 |
| GETS-2026-0013 | https://www.gets.govt.nz/UW/ExternalTenderDetails.htm?id=35068879 | UW | 2026-10-09 | tender_35068879.pdf | ec244165722f34def9b058fec9d16df57945bc2be49a3b15078f4063a4441cba |
| GETS-2026-0014 | https://www.gets.govt.nz/AT/ExternalTenderDetails.htm?id=34761285 | AT | 2026-10-09 | tender_34761285.pdf | f2121a56dd3c55d4c83ac18fb77bbbddbf0d29cd758a4e89e0b0f8fcff205a39 |
| GETS-2026-0015 | https://www.gets.govt.nz/AT/ExternalTenderDetails.htm?id=34842108 | AT | 2026-10-09 | tender_34842108.pdf | 4024881521ef1a352ec90478e225f36ec31db37bee731368a0893a46f24b438d |
| GETS-2026-0016 | https://www.gets.govt.nz/NZIST/ExternalTenderDetails.htm?id=34924335 | NZIST | 2026-10-09 | tender_34924335.pdf | 4707e81d41c69c9046e91533ce1607f144096cb62f05e2fbae0e5f7f186dfaa7 |
| GETS-2026-0017 | https://www.gets.govt.nz/NZIST/ExternalTenderDetails.htm?id=34924423 | NZIST | 2026-10-09 | tender_34924423.pdf | 826335b49fee7fc120bce2e0a4738701659bc9b19097930eb47b7fa07bb60346 |
| GETS-2026-0018 | https://www.gets.govt.nz/DIA/ExternalTenderDetails.htm?id=23700412 | DIA | 2026-10-09 | tender_23700412.pdf | 47cd6d686fa6edbee97adb8776f7ecec0efe967e4c3fd0a13002f68ae8937165 |
| GETS-2026-0019 | https://www.gets.govt.nz/DIA/ExternalTenderDetails.htm?id=33732411 | DIA | 2026-10-09 | tender_33732411.pdf | 45b18e1b04b4551f3fd00b25b6a6b29f85572f9eb3c228449ae214d65869d8ef |
| GETS-2026-0020 | https://www.gets.govt.nz/MEDUR/ExternalTenderDetails.htm?id=32504269 | MEDUR | 2026-10-09 | tender_32504269.pdf | fb1e4491a27ff5c286ee2ac3843151c36c6133de1cd465db63a43a2d59c55d69 |
| GETS-2026-0021 | https://www.gets.govt.nz/WAIMDC/ExternalTenderDetails.htm?id=31377530 | WAIMDC | 2026-10-09 | tender_31377530.pdf | ffaa91abeb1061b75ab5bf3c513d7de8616850880653a73714509aee13e5cdc5 |
| GETS-2026-0022 | https://www.gets.govt.nz/EECA/ExternalTenderDetails.htm?id=29898765 | EECA | 2026-10-09 | tender_29898765.pdf | 7b8aae9ab50437cc764a84532773c6582a74241ee78de2f9f17a32da70e0be9c |
| GETS-2026-0023 | https://www.gets.govt.nz/EECA/ExternalTenderDetails.htm?id=31232412 | EECA | 2026-10-09 | tender_31232412.pdf | 89904e3185cc9d6fc152d5d09341e3173374ac9cc9d90d71272282ae8c3e63e9 |
| GETS-2026-0024 | https://www.gets.govt.nz/HEALTHNZ/ExternalTenderDetails.htm?id=35147829 | HEALTHNZ | 2026-10-09 | tender_35147829.pdf | 4f20d7e8ac2848672ce7be22796ea2f1fb967f0ae516f808467509ec214615f5 |
| GETS-2026-0025 | https://www.gets.govt.nz/WaikDC/ExternalTenderDetails.htm?id=34645793 | WaikDC | 2026-10-09 | tender_34645793.pdf | e243b14fd5787feda245160adef03bc6405ff4ddaddb878bd810c4be0cd32421 |
| GETS-2026-0026 | https://www.gets.govt.nz/MEDU/ExternalTenderDetails.htm?id=35116860 | MEDU | 2026-10-09 | tender_35116860.pdf | 97b946e9a533717e991bb6e17691015c94e1a186dfe1dafb8c9537b51a183fef |
| GETS-2026-0027 | https://www.gets.govt.nz/HEALTHNZ/ExternalTenderDetails.htm?id=35098594 | HEALTHNZ | 2026-10-09 | tender_35098594.pdf | c5227bb08d56ba7e9320dfc70ec109504398578e88b378c207bef78e4df431ec |
| GETS-2026-0028 | https://www.gets.govt.nz/TCDC/ExternalTenderDetails.htm?id=34992673 | TCDC | 2026-10-09 | tender_34992673.pdf | 46e1e103ad82b687adf364633d61dcdb11c770b36acbe7cb1c8cd10133c3e99e |
| GETS-2026-0029 | https://www.gets.govt.nz/TASDC/ExternalTenderDetails.htm?id=35010726 | TASDC | 2026-10-09 | tender_35010726.pdf | ece227b6985326ea4e2a9cd0fe883c2940e2ab3d2af4beea0d80dbc480b76ba1 |
| GETS-2026-0030 | https://www.gets.govt.nz/WAIDC/ExternalTenderDetails.htm?id=35045167 | WAIDC | 2026-10-09 | tender_35045167.pdf | 3318ce7ee75ed4a2b10ae9ce9e1645c04123380163bbf4168e70c129f7bdfaa8 |
| GETS-2026-0031 | https://www.gets.govt.nz/WAIDC/ExternalTenderDetails.htm?id=35127157 | WAIDC | 2026-10-09 | tender_35127157.pdf | 0b19a02db1c838240ce452724c070d735c16ca302f50c25acc6367341d159473 |
| GETS-2026-0032 | https://www.gets.govt.nz/HCC/ExternalTenderDetails.htm?id=35129419 | HCC | 2026-10-09 | tender_35129419.pdf | cda06a17cea38f5e69e4a5567764b92165d8493573c53712f8f9793961856fd8 |
| GETS-2026-0033 | https://www.gets.govt.nz/MBIE/ExternalTenderDetails.htm?id=34908926 | MBIE | 2026-10-09 | tender_34908926.pdf | 78d44b2f4fe7f6e7589dd3ad27a4dd55812e0934bde8a8183ae5049b8ac8fe44 |
| GETS-2026-0034 | https://www.gets.govt.nz/MD/ExternalTenderDetails.htm?id=33830698 | MD | 2026-10-09 | tender_33830698.pdf | 61032e69355e58342c0e995d0693ba989e83d9cff3473dbf61eeb175985e534b |
| GETS-2026-0035 | https://www.gets.govt.nz/MSD/ExternalTenderDetails.htm?id=35034968 | MSD | 2026-10-09 | tender_35034968.pdf | a2cac034385ccf32e0b590cfc96113f205951d7cce820346543673fcc5768140 |
| GETS-2026-0036 | https://www.gets.govt.nz/AC/ExternalTenderDetails.htm?id=35056284 | AC | 2026-10-09 | tender_35056284.pdf | fc0cca90d8a09ee7c73bbc178fc8367bed3e77512786fa34c30db5cf33ac977b |
| GETS-2026-0037 | https://www.gets.govt.nz/AURORA/ExternalTenderDetails.htm?id=33266797 | AURORA | 2026-10-09 | tender_33266797.pdf | 66cc40441484db17daae9b6e710a2423939cbd5b1da059887feb723b45023bab |
| GETS-2026-0038 | https://www.gets.govt.nz/ACC/ExternalTenderDetails.htm?id=29971844 | ACC | 2026-10-09 | tender_29971844.pdf | 1f3e9bb9fdb4152379c0893577dd076ed9015a4f3b9c29b3a8696bb149d03a26 |
| GETS-2026-0039 | https://www.gets.govt.nz/ACC/ExternalTenderDetails.htm?id=31338623 | ACC | 2026-10-09 | tender_31338623.pdf | 1e8904897b01d4ba3b20f4a7d676feaabe232fce7622a16d0636f989a0574ad8 |
| GETS-2026-0040 | https://www.gets.govt.nz/PCO/ExternalTenderDetails.htm?id=34538513 | PCO | 2026-10-09 | tender_34538513.pdf | a96a00b21accfb8e0636924953c309d99a5341b4c630f82ffb35d2aeb43a0f08 |
| GETS-2026-0041 | https://www.gets.govt.nz/QLDC/ExternalTenderDetails.htm?id=35091767 | QLDC | 2026-10-09 | tender_35091767.pdf | 4c6df3813d84ee207c2b94c25adc040e51db8ea034e242d203529ce341663b8a |
| GETS-2026-0042 | https://www.gets.govt.nz/QLDC/ExternalTenderDetails.htm?id=34733646 | QLDC | 2026-10-09 | tender_34733646.pdf | 78903a2594bb28c712a9fd814e14550e47d0906bb501044be6e023463c2c90e8 |
| GETS-2026-0043 | https://www.gets.govt.nz/MFAT/ExternalTenderDetails.htm?id=34134620 | MFAT | 2026-10-09 | tender_34134620.pdf | 7fd0c1d2416844af6cd8257a1aab84889e192cf6640ddfcef2c5f4328dee3830 |
| GETS-2026-0044 | https://www.gets.govt.nz/WSL/ExternalTenderDetails.htm?id=35091453 | WSL | 2026-10-09 | tender_35091453.pdf | fb108be381f253c018e37645bbffdcfbb799dbdce4c196da5d67647d4aa2461f |
| GETS-2026-0045 | https://www.gets.govt.nz/MPI/ExternalTenderDetails.htm?id=33832412 | MPI | 2026-10-09 | tender_33832412.pdf | a707baa04328756ccfea6021f7205c55365c9a160cbf7ede878b71780f623cb6 |
| GETS-2026-0046 | https://www.gets.govt.nz/CCC/ExternalTenderDetails.htm?id=33694604 | CCC | 2026-10-09 | tender_33694604.pdf | af094a789028b456622bb722ed411b87e315a2f3c66782e009109289e62f39ea |
| GETS-2026-0047 | https://www.gets.govt.nz/GRYDC/ExternalTenderDetails.htm?id=34865819 | GRYDC | 2026-10-09 | tender_34865819.pdf | cf33f08a0424d671c42bc09bef478851a6399e810f3b04ee088da5d3b30e1db1 |
| GETS-2026-0048 | https://www.gets.govt.nz/GDC/ExternalTenderDetails.htm?id=34708070 | GDC | 2026-10-09 | tender_34708070.pdf | 283cdfb4e8f711fab32b5682bef86bc504bbc6ae7282d3045d1ddf30c2be91e2 |
| GETS-2026-0049 | https://www.gets.govt.nz/TEC/ExternalTenderDetails.htm?id=34939478 | TEC | 2026-10-09 | tender_34939478.pdf | bafa5b47048c6c1ea410b1f55e1b0150a416d155a80f503b7f6ed98798d9d412 |
| GETS-2026-0050 | https://www.gets.govt.nz/HBRC/ExternalTenderDetails.htm?id=35008398 | HBRC | 2026-10-09 | tender_35008398.pdf | 7e3378dcb7cadb541f54d8e7d73e8dace1906e9c43e23709552db88891e80b6b |

## Loan application form (real blank layout, fictional content)

To be added at checkpoint H4.

## Real-estate enquiries (fictional, script-written)

Written by `python -m src.make_fictional_leads`. No source document; every detail is made up.
