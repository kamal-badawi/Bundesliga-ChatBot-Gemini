
# Diese Methode filtert die nächsten Spielergebnisse (ab 01.01.2025)
# Da die Saison jetzt zu ende ist, wurde ein Anker gesetzt, nach diesem Anker (31.12.2024) werden die Daten so manipuliert, als wären sie noch offen
def get_next_upcoming_Matches_results() -> dict:
    import All_Matches_Results

    df_all_matches_info = All_Matches_Results.fetch_all_matches_results().get('df_matches_results')
    description = All_Matches_Results.fetch_all_matches_results().get('description')

    df_upcoming_matches_info= df_all_matches_info[df_all_matches_info['Spieltag Aktualität'] == 'Nächster Spieltag']
    description = description.replace('TYPE_EN', 'next_upcoming').replace('TYPE_DE', 'das nächste Spiel')


    response = {'df_upcoming_matches_results': df_upcoming_matches_info,
                'description': description}

    return response




