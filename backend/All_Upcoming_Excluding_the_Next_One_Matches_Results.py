# Diese Methode filtert die kommenden aber nicht die nächsten Spielergebnsise (ab 01.01.2025)
# Da die Saison jetzt zu ende ist, wurde ein Anker gesetzt, nach diesem Anker (31.12.2024) werden die Daten so manipuliert, als wären sie noch offen
def get_all_upcoming_excluding_the_next_one_results() -> dict:
    import All_Matches_Results

    df_all_matches_info = All_Matches_Results.fetch_all_matches_results().get('df_matches_results')
    description = All_Matches_Results.fetch_all_matches_results().get('description')

    df_all_upcoming_excluding_the_next_one_matches_info= df_all_matches_info[df_all_matches_info['Spieltag Aktualität'] == 'Zukünftiger Spieltag']
    description = description.replace('TYPE_EN', 'all_upcoming_excluding_the_next_one').replace('TYPE_DE', 'alle zukünftigen Spiele mit Ausnahme des nächsten Spiels')


    response = {'df_all_upcoming_excluding_the_next_one_matches_info': df_all_upcoming_excluding_the_next_one_matches_info,
                    'description': description}

    return response