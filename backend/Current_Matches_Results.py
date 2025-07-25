# Diese Methode filtert die aktuellen Spielergebnisse (ab 01.01.2025)
# Da die Saison jetzt zu ende ist, wurde ein Anker gesetzt, nach diesem Anker (31.12.2024) werden die Daten so manipuliert, als wären sie noch offen
def get_current_matches_results() -> dict:
    import All_Matches_Results

    df_all_matches_info = All_Matches_Results.fetch_all_matches_results().get('df_matches_results')
    description = All_Matches_Results.fetch_all_matches_results().get('description')

    df_current_matches_results= df_all_matches_info[df_all_matches_info['Spieltag Aktualität'] == 'Aktueller Spieltag']
    description = description.replace('TYPE_EN', 'current').replace('TYPE_DE', 'das aktuelle Spiel')


    response = {'df_current_matches_results': df_current_matches_results,
                'description': description}

    return response