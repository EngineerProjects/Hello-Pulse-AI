# Azure Files Classification by Output Type

Based on SAS code analysis, here's the classification of Azure files and the columns extracted for each main output.

---

## **Input Files Overview**

You have **9 input files** on Azure:

### AZ Files (4 files)
1. `IMS_INFP_IIA0P6_3SPEIPFM99_IPF_202509119130Z.csv.gz` → **PTF36a.IPFM99** (Agent CA details)
2. `IMS_INFP_IIA0P6_E1SPEIPFM99_IPF_202509119130Z.csv.gz` → **PTF16a.IPFM99** (Broker CA details)
3. `IMS_INFP_IIA0P6_IPFE16_IPF_202509119130Z.csv.gz` → **PTF16.IPF** (Agent policies - ~880 cols)
4. `IMS_INFP_IIA0P6_IPFE36_IPF_202509119130Z.csv.gz` → **PTF36.IPF** (Broker policies - ~880 cols)

### AZEC Files (2 files)
5. `POLIC_CU.csv` → **POLIC_CU.POLIC_CU** (AZEC policies - ~280 cols)
6. `CAPITXCU.csv` → **CAPITXCU.CAPITXCU** (AZEC capitals)

### IRD RISK Files (3 files)
7. `ird_risk_q45_202509.csv` → **IRD_RISK_Q45** (Ready to use)
8. `ird_risk_q46_202509.csv` → **IRD_RISK_Q46** (Ready to use)
9. `ird_risk_qan_202509.csv` → **IRD_RISK_QAN** (Ready to use)

---

## **1. MVT_PTF Output** (`mvt_ptf.parquet`)

### Files Used:
- **PTF16.IPF** (`IMS_INFP_IIA0P6_IPFE16_IPF_202509119130Z.csv.gz`)
- **PTF36.IPF** (`IMS_INFP_IIA0P6_IPFE36_IPF_202509119130Z.csv.gz`)
- **PTF16a.IPFM99** (`IMS_INFP_IIA0P6_E1SPEIPFM99_IPF_202509119130Z.csv.gz`)
- **PTF36a.IPFM99** (`IMS_INFP_IIA0P6_3SPEIPFM99_IPF_202509119130Z.csv.gz`)

### SAS Reference:
- **AZ**: `PTF_MVTS_AZ_MACRO.sas` (lines 92-114)
- **AZEC**: `PTF_MVTS_AZEC_MACRO.sas` (lines 36-40, 135-224)

### Columns Extracted from PTF16.IPF and PTF36.IPF (Lines 14-89):

**Identifiers:**
- `cdprod`, `nopol`, `NOCLT`, `nmclt`, `NMACTA`, `noint`

**Addresses:**
- `posacta AS posacta_ri`, `rueacta AS rueacta_ri`, `cediacta AS cediacta_ri`

**Dates:**
- `dtcrepol`, `dteffan`, `dttraan`, `dtresilp`, `dttraar`, `DTECHAMM`
- `dttypl11`, `dttypl12`, `dttypl13`
- `DTOUCHAM`, `DTRCCPPR`, `DTRECTXK`, `DTRCPPRE`

**Classifications:**
- `cdnatp`, `cmarch`, `csegt AS CSEG`, `cssegt AS CSSSEG`, `cdri`, `cdsitp`
- `CDCIEORI`, `CDSITMGR`, `cdtypli1`, `cdtypli2`, `cdtypli3`
- `CDNAF`, `CDTRE`, `CDACTPRO`, `CDREG`

**Financial:**
- `txcede`, `mtprprto`, `prdccie AS PRDCIE`, `prdccie`
- `FNCMACA AS MTCA`, `MTCAF`, `MTSMPR`

**Capitals (14 amounts + 14 labels):**
- `MTCAPI1` to `MTCAPI14`
- `LBCAPI1` to `LBCAPI14`

**Indexation (14 codes + 14 coefficients):**
- `CDPRVB1` to `CDPRVB14`
- `PRPRVC1` to `PRPRVC14`

**Co-insurance:**
- `cdpolgp1`, `CDTPCOA AS CDCOAS`, `PRCDCI`

**Risk:**
- `CDFRACT`, `QUARISQ`, `NMRISQ`, `NMSRISQ`, `RESRISQ`, `RUERISQ`, `LIDIRISQ`, `POSRISQ`, `VILRISQ`
- `tydrisi`, `OPAPOFFR`, `ACTPRIM`

**Other:**
- `ptgst`, `Cdmothes`, `cdpolrvi`, `nopoli1`, `CDCASRES`, `CDGREV`
- `CTDEFTTRA`, `CTPRVTRV`, `LBNATTRV`, `DSTCSC`, `LBOLISOU`

**Total Columns from IPF: ~89 columns**

### Columns Extracted from PTF16a.IPFM99 and PTF36a.IPFM99 (Lines 104-109):

Only for product **CDPROD = '01099'**:

- `CDPOLE`, `VISION`, `CDPROD`, `NOPOL`, `NOINT`
- `MTCA`, `MTCAENP`, `MTCASST`, `MTCAVNT`

**Total Columns from IPFM99: 8 columns**

---

### Columns Extracted from AZEC POLIC_CU (Lines 16-40):

**From POLIC_CU.POLIC_CU:**

- `POLICE`, `DATFIN`, `DATRESIL`, `INTERMED`, `POINGEST`, `CODECOAS`
- `DATAFN`, `ETATPOL`, `DUREE`, `FINPOL`, `DATTERME`, `DATEXPIR`
- `PRODUIT`, `EFFETPOL`, `PRIME`, `PARTBRUT`, `CPCUA`, `NOMCLI`
- `MOTIFRES`, `ORIGRES`, `TYPCONTR`, `RMPLCANT`, `GESTSIT`
- `ECHEANMM`, `ECHEANJJ`, `ECHEANAA` (for date reconstruction)
- `INDREGUL`

**Total Columns from POLIC_CU: ~27 columns**

---

## **2. CAPITAUX Output** (`az_azec_capitaux.parquet`)

### Files Used:
- **PTF16.IPF** (`IMS_INFP_IIA0P6_IPFE16_IPF_202509119130Z.csv.gz`)
- **PTF36.IPF** (`IMS_INFP_IIA0P6_IPFE36_IPF_202509119130Z.csv.gz`)
- **CAPITXCU.CAPITXCU** (`CAPITXCU.csv`)
- **INCENDCU.INCENDCU** (AZEC - not in your list, may be embedded in POLIC_CU or separate)

### SAS Reference:
- **AZ**: `CAPITAUX_AZ_MACRO.sas` (lines 1-137)
- **AZEC**: `CAPITAUX_AZEC_MACRO.sas` (lines 1-96)

### Columns Extracted from AZ PTF16.IPF and PTF36.IPF (Lines 10-24):

**Identifiers:**
- `cdprod`, `nopol`, `nmclt`, `noint`, `ptgst`

**Dates:**
- `dtcrepol`, `DTFFSITT`, `DTECHANN`
- `dtresilp` (named `diresilp` in code - likely typo)

**Classifications:**
- `cdnatp`, `cmarch`, `csegt AS cseg`, `cssegt AS cssseg`, `cdsitp`
- `cdgecent`, `cdmotres`, `CDCASRES`, `CDTPCOA AS CDCOAS`

**Financial:**
- `txcede`, `mtprpto` (likely `mtprprto`), `prcdcie`, `cdpolqp1` (likely `cdpolgp1`)

**Capitals (14 amounts + 14 labels + 14 indexation codes + 14 evolution coefficients):**
- `MTCAPT1` to `MTCAPT14` (likely `MTCAPI1` to `MTCAPI14`)
- `LBCAPT1` to `LBCAPT14` (likely `LBCAPI1` to `LBCAPI14`)
- `CDPRVB1` to `CDPRVB14`
- `PRPRVC1` to `PRPRVC14`

**Total Columns from IPF for CAPITAUX: ~70 columns**

### Columns Extracted from AZEC CAPITXCU.CAPITXCU (Lines 5-63):

- `POLICE`, `PRODUIT`
- `smp_sre` (SMP or LCI indicator)
- `brch_rea` (Branch: IP0=Perte Exploit, ID0=Dommages Direct)
- `capx_100` (Capital at 100%)
- `capx_cua` (Capital company share)

**Total Columns from CAPITXCU: 6 columns**

### Additional AZEC Data (if INCENDCU exists):

From `INCENDCU.INCENDCU` (Lines 75-79):
- `POLICE`, `PRODUIT`
- `MT_BASPE` (Base Perte Exploitation)
- `MT_BASDI` (Base Dommages Immobiliers/Directs)

---

## **3. EMISSIONS Output** (2 files)

### 3A. `primes_emises_pol_garp.parquet`
### 3B. `primes_emises_pol.parquet`

### Files Used:
**Direct from One BI system (PRM.rf_frl_prm_dtl_midcorp_m) - NOT from your Azure files**

The emissions processing reads from **PRM database** on One BI, not from the Azure files you listed.

### SAS Reference:
- **EMISSIONS_RUN.sas** (lines 273-388)

### Columns Used from One BI (Lines 275-276):

- `CD_NIV_2_STC`, `CD_INT_STC`, `NU_CNT_PRM`, `CD_PRD_PRM`
- `CD_STATU_CTS`, `DT_CPTA_CTS`, `DT_EMIS_CTS`, `DT_ANNU_CTS`
- `MT_HT_CTS`, `MT_CMS_CTS`, `CD_CAT_MIN`, `CD_GAR_PRINC`
- `CD_GAR_PROSPCTIV`, `nu_ex_ratt_cts`, `cd_marche`

**Total Columns: 15 columns from One BI**

### ⚠️ Important Note:
The EMISSIONS outputs **do NOT use your Azure files**. They connect to One BI PRM database.

---

## **4. IRD RISK Outputs** (3 files)

### 4A. `ird_risk_q45.parquet`
### 4B. `ird_risk_q46.parquet`
### 4C. `ird_risk_qan.parquet`

### Files Used:
- `ird_risk_q45_202509.csv`
- `ird_risk_q46_202509.csv`
- `ird_risk_qan_202509.csv`

### SAS Reference:
- **PTF_MVTS_CHARG_DATARISK_ONEBI_BIFR.sas** (lines 61-123)

### Processing:
These files are **already in final format** and only require:
1. Character encoding fixes (é → e, è → e, etc.)
2. Direct download to output

**All columns are used as-is** (no column selection in SAS code).

---

## **Summary Table**

| Output File | Azure Input Files | # Cols Used | Key Purpose |
|-------------|------------------|-------------|-------------|
| **mvt_ptf.parquet** | `IPFE16_IPF`, `IPFE36_IPF`, `E1SPEIPFM99_IPF`, `3SPEIPFM99_IPF`, `POLIC_CU` | ~89 (AZ) + ~27 (AZEC) | Portfolio movements, policies, contracts |
| **az_azec_capitaux.parquet** | `IPFE16_IPF`, `IPFE36_IPF`, `CAPITXCU` | ~70 (AZ) + ~6 (AZEC) | Insured capitals, SMP, LCI |
| **primes_emises_pol_garp.parquet** | ❌ One BI PRM DB | 15 | Emitted premiums by GARP |
| **primes_emises_pol.parquet** | ❌ One BI PRM DB | 15 | Emitted premiums aggregated |
| **ird_risk_q45.parquet** | `ird_risk_q45_202509.csv` | All | Risk data Q45 |
| **ird_risk_q46.parquet** | `ird_risk_q46_202509.csv` | All | Risk data Q46 |
| **ird_risk_qan.parquet** | `ird_risk_qan_202509.csv` | All | Risk data QAN |

---

## **Recommendations for Bronze Layer**

### 1. **For MVT_PTF Processing:**

You should create a Bronze reader that:

**For AZ files (IPFE16_IPF, IPFE36_IPF):**
```python
# Select only the ~89 needed columns, not all 880
az_columns = [
    'cdprod', 'nopol', 'NOCLT', 'nmclt', 'NMACTA', 'noint',
    'dtcrepol', 'dteffan', 'dttraan', 'dtresilp', 'dttraar', 'DTECHAMM',
    # ... (full list in document above)
]
```

**For IPFM99 files:**
```python
# Only for CDPROD = '01099'
ipfm99_columns = ['CDPOLE', 'VISION', 'CDPROD', 'NOPOL', 'NOINT',
                  'MTCA', 'MTCAENP', 'MTCASST', 'MTCAVNT']
```

### 2. **For CAPITAUX Processing:**

**For AZ files:**
```python
# Select ~70 columns focused on capitals
az_capital_columns = [
    'cdprod', 'nopol', 'nmclt', 'noint', 'ptgst',
    'MTCAPI1', 'MTCAPI2', ..., 'MTCAPI14',
    'LBCAPI1', 'LBCAPI2', ..., 'LBCAPI14',
    # ... (full list in document above)
]
```

**For CAPITXCU:**
```python
# All 6 columns needed
capitxcu_columns = ['POLICE', 'PRODUIT', 'smp_sre', 'brch_rea', 'capx_100', 'capx_cua']
```

### 3. **For IRD RISK:**
Read all columns as-is, only apply encoding fixes.

### 4. **For EMISSIONS:**
❌ **Not applicable** - this data comes from One BI database, not your Azure files.

---

## **Next Steps**

1. ✅ Create separate Bronze readers per file type:
   - `BronzeReaderAZ_IPF` (for IPFE16/IPFE36)
   - `BronzeReaderAZ_IPFM99` (for IPFM99 files)
   - `BronzeReaderAZEC_POLIC_CU` (for POLIC_CU)
   - `BronzeReaderAZEC_CAPITXCU` (for CAPITXCU)
   - `BronzeReaderIRD` (for IRD files)

2. ✅ Each reader should:
   - Extract only needed columns (not all 880!)
   - Apply basic type casting
   - Handle compression (.gz)
   - Save to Bronze layer

3. ✅ Silver layer will then:
   - Apply harmonization (AZEC → AZ renames)
   - Clean data
   - Apply unified schema
   - Output: `az_harmonized.parquet` + `azec_harmonized.parquet`
