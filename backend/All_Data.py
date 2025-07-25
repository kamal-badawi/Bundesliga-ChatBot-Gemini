# Diese Methode führt alle Bundelaig-Infos aus allen APIs zusammen
def get_all_data() -> dict:
    import Bundesliga_Table
    import All_Bundesliga_Teams
    import Goal_Getters
    import Past_Matches_Results
    import Current_Matches_Results
    import Next_Upcoming_Matches_results
    import All_Upcoming_Excluding_the_Next_One_Matches_Results

    # Bundesliga-Tabelle
    df_bundesliga_table = Bundesliga_Table.fetch_bundesliga_table().get('df_bundesliga_table')

    # Alle Bundesliga-Team
    df_all_bundesliga_teams = All_Bundesliga_Teams.fetch_all_bundesliga_teams().get('df_all_bundesliga_teams')


    # Alle Torschützen
    df_goal_getters  = Goal_Getters.fetch_goal_getters().get('df_goal_getters')


    # Auflistung vergangener Spieltage-Ergebnisse
    df_past_matches_results = Past_Matches_Results.get_past_matches_results().get('df_past_matches_results')



    # Auflistung aktueller Spieltage-Ergebnisse
    df_current_matches_results = Current_Matches_Results.get_current_matches_results().get('df_current_matches_results')

    # Auflistung nächstes Spieltages-Ergebnisse
    df_next_upcoming_Matches_results = Next_Upcoming_Matches_results.get_next_upcoming_Matches_results().get('df_upcoming_matches_results')


    # Auflistung aller zukünftiger Spieltage-Ergebnisse, außer dem nächsten Spiel
    df_all_upcoming_excluding_the_next_one = All_Upcoming_Excluding_the_Next_One_Matches_Results.get_all_upcoming_excluding_the_next_one_results().get('df_all_upcoming_excluding_the_next_one_matches_info')


    source = {'df_bundesliga_table': df_bundesliga_table,
              'df_all_bundesliga_teams': df_all_bundesliga_teams,
              'df_goal_getters': df_goal_getters,
              'df_past_matches_results': df_past_matches_results,
              'df_current_matches_results': df_current_matches_results,
              'df_next_upcoming_Matches_results':df_next_upcoming_Matches_results,
              'df_all_upcoming_excluding_the_next_one_matches_results': df_all_upcoming_excluding_the_next_one}



    return source

