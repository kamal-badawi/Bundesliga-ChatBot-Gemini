# Diese Methode gibt Informationen zurück
# Diese Informationen werden dem Gemini-Modell übergeben, damit er weiß, in welcher Dictionary welche Daten vorahnden sind
def get_general_information() -> dict:
    import Bundesliga_Table
    import All_Bundesliga_Teams
    import Goal_Getters
    import Past_Matches_Results
    import Current_Matches_Results
    import Next_Upcoming_Matches_results
    import All_Upcoming_Excluding_the_Next_One_Matches_Results

    # Informationen zur Bundesliga-Tabelle
    desc_bundesliga_table= Bundesliga_Table.fetch_bundesliga_table().get('description')

    # Informationen zu allen Teams in der Bundesliga
    desc_all_bundesliga_teams = All_Bundesliga_Teams.fetch_all_bundesliga_teams().get('description')

    # Informationen zu allen Torschützen
    desc_goal_getters = Goal_Getters.fetch_goal_getters().get('description')

    # Informationen zu allen vergangenen Spieltage-Ergebnissen
    desc_past_matches_results = Past_Matches_Results.get_past_matches_results().get('description')

    # Informationen zum aktuellen Spieltag-Ergebnissen
    desc_current_matches_results = Current_Matches_Results.get_current_matches_results().get('description')

    # Informationen zum nächsten Spieltag-Ergebnissen
    desc_next_upcoming_Matches_results = Next_Upcoming_Matches_results.get_next_upcoming_Matches_results().get('description')

    # Informationen zu allen zukünftigen Spieltage-Ergebnissen, außer dem nächsten Spiel
    desc_all_upcoming_excluding_the_next_one_matches_results = All_Upcoming_Excluding_the_Next_One_Matches_Results.get_all_upcoming_excluding_the_next_one_results().get('description')


    information = {'df_bundesliga_table': desc_bundesliga_table,
                    'df_all_bundesliga_teams': desc_all_bundesliga_teams,
                    'df_goal_getters': desc_goal_getters,
                   'df_past_matches_results': desc_past_matches_results,
                   'df_current_matches_results': desc_current_matches_results,
                   'df_next_upcoming_Matches_results':desc_next_upcoming_Matches_results,
                   'df_all_upcoming_excluding_the_next_one_matches_results': desc_all_upcoming_excluding_the_next_one_matches_results}


    return information

