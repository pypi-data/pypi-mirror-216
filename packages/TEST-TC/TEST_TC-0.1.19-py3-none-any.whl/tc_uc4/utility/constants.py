from __future__ import annotations

code_to_region_name: dict[int, str] = {
                 30: 'Lombardia',190: 'Sicilia',50: 'Veneto',80: 'Emilia-Romagna',120: 'Lazio',200: 'Sardegna',
                 150: 'Campania',10: 'Piemonte',42: 'Trento',70: 'Liguria',130: 'Abruzzo',100: 'Umbria',
                 180: 'Calabria',160: 'Puglia',110: 'Marche',90: 'Toscana',20: "Valle D Aosta",170: 'Basilicata',
                 60: 'Friuli-Venezia-Giulia',41: 'Bolzano',140: 'Molise'}


code_to_speciality: dict[int, str] = {2: 'Cardiologia',
 3: 'Chirurgia Generale',
 13: 'Nefrologia',
 15: 'Neurologia',
 19: 'Ortopedia E Traumatologia',
 20: 'Ostetricia E Ginecologia',
 21: 'Otorinolaringoiatria',
 23: 'Psichiatria',
 12: 'Recupero E Riabilitazione',
 25: 'Urologia',
 18: 'Oncologia',
 16: 'Oculistica',
 5: 'Chirurgia Vascolare',
 27: 'Dermatologia',
 22: 'Pneumologia',
 10: 'Gastroenterologia',
 9: 'Endocrinologia'}


predict_dataframe_columns: list[str] = [
                        "Timestamp",
                        "Id_pred",
                        "Pred_mean",
                        "Sigma",
                        "Pi_lower_95",
                        "Pi_upper_95",
                    ]
