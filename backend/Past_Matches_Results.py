# Diese Methode filtert die vorherigen Spielergebnisse
def get_past_matches_results() -> dict:
    import All_Matches_Results

    df_all_matches_info = All_Matches_Results.fetch_all_matches_results().get('df_matches_results')
    description = All_Matches_Results.fetch_all_matches_results().get('description')

    df_passt_matches_info= df_all_matches_info[df_all_matches_info['Spieltag Aktualität'] == 'Vergangener Spieltag']
    description = description.replace('TYPE_EN', 'past').replace('TYPE_DE', 'die vergangenen Spiele')


    response = {'df_past_matches_results': df_passt_matches_info,
                    'description': description}
    

    return response

