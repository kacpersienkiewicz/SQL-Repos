'''
This file is mainly ment to create a bunch of 

'''

import sqlite3 as sql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# #################################################################################################################################################################################
# get_stats 
# A series of functions to query the SQLite DB to get a dataframe to be used for analysis and other functions
# #################################################################################################################################################################################

def get_player_stats(con, player_id: str):
    # Using the player_id instead of the name is easier to implement and it prevents any confusion between two players with similar or the same name.
    # player_id is findable via the playerdata.txt file
    # name, mp, pts, ast, trb, orb, drb, stl, blk, tov, pf, fga, fgm, fg3a, fg3m, fta, ftm, pm  = player_stats
    return

def get_team_stats(con, team_abbreviation):
   # team, tm_pts, tm_ast, tm_trb, tm_orb, tm_drb, tm_stl, tm_blk, tm_tov, tm_pf, tm_fga, tm_fgm, tm_fg3a, tm_fg3m, tm_fta, tm_ftm, tm_pm  = team_stats
   # team_abbreviations can be found in the file team_data.txt
    query = f"""SELECT SUBSTRING(season_id,2,5) AS Season,
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(pts_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(pts_away) END AS 'Team Points',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(ast_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(ast_away) END AS 'Team Assists',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(reb_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(reb_away) END AS 'Team Total Rebounds',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(oreb_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(oreb_away) END AS 'Team Offensive Rebounds',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(dreb_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(dreb_away) END AS 'Team Defensive Rebounds',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(stl_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(stl_away) END AS 'Team Steals',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(blk_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(blk_away) END AS 'Team Blocks',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(tov_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(tov_away) END AS 'Team Turnovers',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(pf_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(pf_away) END AS 'Team Personal Fouls',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(fga_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(fga_away) END AS 'Team Field Goals Attempted',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(fgm_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(fgm_away) END AS 'Team Field Goals Made',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(fg3a_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(fg3a_away) END AS 'Team 3-pt Field Goals Attempted',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(fg3m_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(fg3m_away) END AS 'Team 3-pt Field Goals Made',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(fta_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(fta_away) END AS 'Team Free Throws Attempted',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(ftm_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(ftm_away) END AS 'Team Free Throws Made',
    CASE WHEN team_abbreviation_home = {team_abbreviation} THEN AVG(plus_minus_home) WHEN team_abbreviation_away = {team_abbreviation} THEN AVG(plus_minus_away) END AS 'Team Plus Minus'
    FROM game
    WHERE team_abbreviation_home = {team_abbreviation} OR team_abbreviation_away = {team_abbreviation}
    GROUP BY Season"""
    dataframe = pd.read_sql_query(query, con, index_col="Season")
    return dataframe

def get_league_stats(con):
    # The season is determined by the year it started. For example, the 1973-1974 season is input as 1973.
    # season, lg_pts, lg_ast, lg_trb, lg_orb, lg_drb, lg_stl, lg_blk, lg_tov, lg_pf, lg_fga, lg_fgm, lg_fg3a, lg_fg3m, lg_fta, lg_ftm = league_stats
    query = """SELECT SUBSTRING(season_id,2,4) as Season,
        AVG(pts_home + pts_away) / 2 as 'League Points', 
        AVG(reb_home + reb_away) / 2 as 'League Rebounds',
        AVG(oreb_home + oreb_away) / 2 as 'League Offensive Rebounds',
        AVG(dreb_home + dreb_away) / 2 as 'League Defensive Rebounds', 
        AVG(ast_home + ast_away) / 2 as 'League Assists', 
        AVG(stl_home + stl_away) / 2 as 'League Steals', 
        AVG(blk_home + blk_away) / 2 as 'League Blocks',
        AVG(tov_home + tov_away) / 2 as 'League Turnovers',
        AVG(pf_home + pf_away) / 2 as 'League Personal Fouls',
        AVG(fga_home + fga_away) / 2 as 'League FGA', 
        AVG(fgm_home + fgm_away) / 2 as 'League FGM',
        AVG(fg3a_home + fg3a_away) / 2 as 'League 3PA', 
        AVG(fg3m_home + fg3m_away) / 2 as 'League 3PM',
        AVG(fta_home + fta_away) / 2 as 'League FTA', 
        AVG(ftm_home + ftm_away) / 2 as 'League FTM' 
        from game group by Season"""
    dataframe = pd.read_sql_query(query, con, index_col="Season")
    return dataframe

# #################################################################################################################################################################################
# PER - Player Efficiency Rating
# #################################################################################################################################################################################

def get_uPER(player_stats, team_stats, league_stats):
    '''
    https://www.basketball-reference.com/about/per.html
    Given a player's stats, and a season (used to calculate team and league stats) spits out a PER, which biases towards offensives stats.
    lg - > league, tm -> team
    mp = minutes played
    pts = points
    ast = assists
    rb = rebounds
    orb = offensive rebounds
    drb = defensive rebounds
    trb = total rebounds
    stl = steals
    blk = blocks
    tov = turnovers
    pf = personal fouls
    fg = field goal made
    fga = field goals attempted
    fg3 = 3-point field goals
    ft = free throws
    factor = arbitrary factor?
    vop = value of possession
    drbp = defensive rebound percentage
    '''
    name, mp, pts, ast, trb, orb, drb, stl, blk, tov, pf, fga, fgm, fg3a, fg3m, fta, ftm, pm  = player_stats # Not all will be used but this is the standard stat array
    team, tm_pts, tm_ast, tm_trb, tm_orb, tm_drb, tm_stl, tm_blk, tm_tov, tm_pf, tm_fga, tm_fgm, tm_fg3a, tm_fg3m, tm_fta, tm_ftm, tm_pm  = team_stats
    season, lg_pts, lg_ast, lg_trb, lg_orb, lg_drb, lg_stl, lg_blk, lg_tov, lg_pf, lg_fga, lg_fgm, lg_fg3a, lg_fg3m, lg_fta, lg_ftm = league_stats
    
    factor = (2 / 3) - (0.5 * (lg_ast / lg_fgm) / (2 * (lg_fgm / lg_ftm)))
    vop = lg_pts / (lg_fga - lg_orb + lg_tov + (0.44 * lg_fta))
    drbp = (lg_trb - lg_orb) / lg_trb

    uPER = 1 / mp * (fg3m + (2/3) * ast + (2 - factor * (tm_ast / tm_fgm)) * fgm \
                    + (ftm * 0.5 * (1 + (1 - (tm_ast / tm_fgm)) + 2/3 * (tm_ast / tm_fgm))) \
                    - vop * tov - vop * drbp * (fga - fgm) \
                    - vop * (0.44  * (0.44 + (0.56 * drbp)) * (fta - ftm)) \
                    + vop * (1 - drbp) * (trb - orb) + vop * drbp * orb + vop * stl + vop * drbp * blk \
                    - pf * ((lg_ftm / lg_pf) - 0.44 * (lg_fta / lg_pf) * vop))
    
    return uPER

def get_aPER(uPER, pace_adjustment):
    # PER is typically adjusted by pace. Basketball Reference has a pace adjustment of league pace / team pace
    # priot to 1973-1974, Basketball Reference uses the following: estimated pace adjustment = 2 * lg_PPG / (tm_PPG + opp_PPG)
    # pace is 48 * (tm_poss + opp_poss) / (2 * (tm_mp/5)), and it estimates possessions per 48 minutes
    return pace_adjustment * uPER

def get_PER(aPER, lg_aPER):
    # Basetball Reference also adjusts per a league average adjusted per over 15 seasons, which is also done here
    return  aPER * (15 / lg_aPER)

def calc_pace_adjustment(lg_pace, tm_pace):
    return lg_pace / tm_pace

def estimate_pace_adjustment(lg_ppg, tm_ppg, opp_ppg):
    return 2 * lg_ppg / (tm_ppg * opp_ppg)

def calc_lg_aPER():
    #wip
    return 

# #################################################################################################################################################################################
#  Graphing Functions
# #################################################################################################################################################################################
def create_save_team_graph(LeagueDF, TeamDF, teamName):
    # Uses the league and team dataframes created by get_league_stats and get_team_stats to create graphs of the team's stats compared to the league average
    # Then it saves the figure into a folder within the directory to avoid issues from the big dataframes being loaded into memory. 
    # I was having issues with the IDE and IPython handling the workspace so I made this
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows = 5, ncols = 1, figsize=(15,30))
    ax1.set_title(f"{teamName} Points by Season")
    ax1.grid('both', 'both')
    ax1.tick_params("x", rotation=45)
    ax1.plot(TeamDF.index, TeamDF["Team Points"], label="Team Points", marker='o')
    ax1.plot(TeamDF.index, TeamDF["Team Points"] - TeamDF["Team Plus Minus"], c='red', marker='x', label="Opponent's Points")
    ax1.plot(TeamDF.index, LeagueDF["League Points"].loc[TeamDF.index], c='black', marker='+', label="League Average Points")
    ax1.legend()

    ax2.set_title(f"{teamName} Assists by Season")
    ax2.tick_params("x", rotation=45)
    ax2.grid('both', 'both')
    ax2.plot(TeamDF.index, TeamDF["Team Assists"], marker='o')

    ax3.set_title(f"{teamName} Rebounds by Season")
    ax3.tick_params("x", rotation=45)
    ax3.grid('both', 'both')
    ax3.bar(TeamDF.index, TeamDF["Team Offensive Rebounds"], bottom=TeamDF["Team Defensive Rebounds"], color='red', label="Offensive Rebounds")
    ax3.bar(TeamDF.index, TeamDF["Team Defensive Rebounds"], color='green', label="Defensive Rebounds")
    ax3.legend()

    ax4.set_title(f"{teamName} Miscellaneous Stats by Season")
    ax4.tick_params("x", rotation=45)
    ax4.grid('both', 'both')
    ax4.plot(TeamDF.index, TeamDF["Team Steals"], c='red', label="Steals", marker='o')
    ax4.plot(TeamDF.index, TeamDF["Team Blocks"], c='green', label="Blocks", marker='o')
    ax4.plot(TeamDF.index, TeamDF["Team Turnovers"], c='black', label="Turnovers", marker='o')
    ax4.plot(TeamDF.index, TeamDF["Team Personal Fouls"], c='brown', label="Fouls", marker='o')
    ax4.legend()

    ax5.set_title(f"{teamName} Shooting Stats by Season")
    ax5.tick_params("x", rotation=45)
    ax5.grid('both', 'both')
    ax5.plot(TeamDF.index, TeamDF["Team Field Goals Attempted"], c='red', label="FGA", marker='o')
    ax5.plot(TeamDF.index, TeamDF["Team Field Goals Made"], c='red', label="FGM", marker='x', linestyle='--')
    ax5.plot(TeamDF.index, TeamDF["Team Free Throws Attempted"], c='green', label="FTA", marker='o')
    ax5.plot(TeamDF.index, TeamDF["Team Free Throws Made"], c='green', label="FTM", marker='x', linestyle='--')
    ax5.plot(TeamDF.index, TeamDF["Team 3-pt Field Goals Attempted"], c='blue', label="FG3A", marker='o')
    ax5.plot(TeamDF.index, TeamDF["Team 3-pt Field Goals Made"], c='blue', label="FG3M", marker='x', linestyle='--')
    ax5.legend()

    plt.savefig(fname=f'Graphs//{teamName}.png',format='png')
