# Diese Methode filtert die aktuellen Spielergebnisse
def get_current_matches_results() -> dict:
    import All_Matches_Results

    df_all_matches_info = All_Matches_Results.fetch_all_matches_results().get('df_matches_results')
    description = All_Matches_Results.fetch_all_matches_results().get('description')

    df_current_matches_results= df_all_matches_info[df_all_matches_info['Spieltag Aktualität'] == 'Aktueller Spieltag']
    description = description.replace('TYPE_EN', 'current').replace('TYPE_DE', 'das aktuelle Spiel')


    response = {'df_current_matches_results': df_current_matches_results,
                'description': description}
    
    

    return response


