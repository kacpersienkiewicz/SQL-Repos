'''
The ultimate goal is to create a dashboard (Tableau at first, dash later) for the NBA's 30 teams from 1996 to 2022, a time frame chosen because it has the most complete data within the database, though the 2012 regular season does not exist in the database.
First, the data will be fetched with a monstrous SQL query and converted into a dataframe. I will then use pandas to create some new columns representing some advanced statistics that were not calculated in the original database.
With all new columns created, the file can be converted into csv files to be used in Tableau. 

Functions to Calculate Team Stats like Offensive/Defensive Rating and Assist Ratio:

Sources: 
https://www.basketball-reference.com/about/glossary.html
https://www.fromtherumbleseat.com/pages/advanced-basketball-statistics-formula-sheet
https://www.espn.com/nba/hollinger/teamstats

Note: Technically, many of the stats (like rebounding rates) are intended to be used for individual players, but substituting team values for player values should give an estimate of the team's stats.
These stats also appear on https://www.nba.com/stats/teams/advanced so this seems like a legitimate way to caulcuate a team stat.  
I also don't use any of these functions however I keep them around with sources to show where the equations are originally from.
'''

import sqlite3 as sql
import pandas as pd
con = sql.connect("Data/nba.sqlite")
cur = con.cursor()

def get_league_stats(con):
    query =f"""SELECT SUBSTRING(season_id,2,5) as Season,
        AVG(pts_home + pts_away) / 2 as lg_pts, 
        AVG(reb_home + reb_away) / 2 as lg_treb,
        AVG(oreb_home + oreb_away) / 2 as lg_oreb,
        AVG(dreb_home + dreb_away) / 2 as lg_dreb, 
        AVG(ast_home + ast_away) / 2 as lg_ast, 
        AVG(stl_home + stl_away) / 2 as lg_stl, 
        AVG(blk_home + blk_away) / 2 as lg_blk,
        AVG(tov_home + tov_away) / 2 as lg_tov,
        AVG(pf_home + pf_away) / 2 as lg_pf,
        AVG(fga_home + fga_away) / 2 as lg_fga, 
        AVG(fgm_home + fgm_away) / 2 as lg_fgm,
        AVG(fg3a_home + fg3a_away) / 2 as lg_fg3a, 
        AVG(fg3m_home + fg3m_away) / 2 as lg_fg3m,
        AVG(fta_home + fta_away) / 2 as lg_fta, 
        AVG(ftm_home + ftm_away) / 2 as lg_ftm 
        FROM game
        WHERE SUBSTRING(season_id,1,1) = '2' AND Season >= '1996'
        GROUP BY Season"""
    dataframe = pd.read_sql_query(query, con, index_col="Season")
    return dataframe

def get_team_stats(con, team, team_abb):
    # This function looks a bit complex but it just prepends the team abbreviation to each stat instead of tm so that it is easier to concatenate all of the stats into one csv for Tableau.
    # The next function does not do those so the query looks a bit cleaner.
    # I decided not to include 
    query = f"""SELECT Season, {team_abb}_mp, {team_abb}_gp, {team_abb}_losses, {team_abb}_wins, {team_abb}_pts, {team_abb}_ast, {team_abb}_treb, {team_abb}_oreb, {team_abb}_dreb, {team_abb}_stl, {team_abb}_blk, {team_abb}_tov, {team_abb}_pf, {team_abb}_fga, {team_abb}_fgm, {team_abb}_fg_pct, {team_abb}_fg3a, {team_abb}_fg3m,
        {team_abb}_fg3_pct, {team_abb}_fta, {team_abb}_ftm, {team_abb}_ft_pct, {team_abb}_pm, {team_abb}_pts_paint, {team_abb}_pts_2nd_chance, {team_abb}_pts_fb, {team_abb}_pts_off_tov, {team_abb}_opp_pts, {team_abb}_opp_ast, {team_abb}_opp_treb, {team_abb}_opp_oreb, {team_abb}_opp_dreb, {team_abb}_opp_stl, {team_abb}_opp_blk,
        {team_abb}_opp_tov, {team_abb}_opp_pf, {team_abb}_opp_fga, {team_abb}_opp_fgm, {team_abb}_opp_fg_pct, {team_abb}_opp_fg3a, {team_abb}_opp_fg3m, {team_abb}_opp_fg3_pct, {team_abb}_opp_fta, {team_abb}_opp_ftm, {team_abb}_opp_ft_pct, {team_abb}_opp_pm, {team_abb}_opp_pts_paint, {team_abb}_opp_pts_2nd_chance, {team_abb}_opp_pts_fb, {team_abb}_opp_pts_off_tov,
        {team_abb}_poss, {team_abb}_opp_poss,
        100 / ({team_abb}_poss + {team_abb}_opp_poss) * {team_abb}_pts as {team_abb}_ORtg,
        100 / ({team_abb}_poss + {team_abb}_opp_poss) * {team_abb}_opp_pts as {team_abb}_DRtg,
        48 * (({team_abb}_poss + {team_abb}_opp_poss) / (2 * {team_abb}_mp /5)) as {team_abb}_pace,
        {team_abb}_ast_pct, {team_abb}_ast_tov_ratio, {team_abb}_ast_ratio, {team_abb}_oreb_pct, {team_abb}_dreb_pct, {team_abb}_treb_pct, {team_abb}_tov_ratio, {team_abb}_efg_pct, {team_abb}_ts_pct
        FROM(SELECT Season, {team_abb}_mp, {team_abb}_gp, {team_abb}_losses, {team_abb}_wins, {team_abb}_pts, {team_abb}_ast, {team_abb}_treb, {team_abb}_oreb, {team_abb}_dreb, {team_abb}_stl, {team_abb}_blk, {team_abb}_tov, {team_abb}_pf, {team_abb}_fga, {team_abb}_fgm, {team_abb}_fg_pct, {team_abb}_fg3a, {team_abb}_fg3m,
        {team_abb}_fg3_pct, {team_abb}_fta, {team_abb}_ftm, {team_abb}_ft_pct, {team_abb}_pm, {team_abb}_pts_paint, {team_abb}_pts_2nd_chance, {team_abb}_pts_fb, {team_abb}_pts_off_tov, {team_abb}_opp_pts, {team_abb}_opp_ast, {team_abb}_opp_treb, {team_abb}_opp_oreb, {team_abb}_opp_dreb, {team_abb}_opp_stl, {team_abb}_opp_blk,
        {team_abb}_opp_tov, {team_abb}_opp_pf, {team_abb}_opp_fga, {team_abb}_opp_fgm, {team_abb}_opp_fg_pct, {team_abb}_opp_fg3a, {team_abb}_opp_fg3m, {team_abb}_opp_fg3_pct, {team_abb}_opp_fta, {team_abb}_opp_ftm, {team_abb}_opp_ft_pct, {team_abb}_opp_pm, {team_abb}_opp_pts_paint, {team_abb}_opp_pts_2nd_chance, {team_abb}_opp_pts_fb, {team_abb}_opp_pts_off_tov,
        0.5 * (({team_abb}_fga + 0.4 + {team_abb}_fta - 1.07 * ({team_abb}_oreb / ({team_abb}_oreb + {team_abb}_opp_dreb)) * ({team_abb}_fga - {team_abb}_fgm) + {team_abb}_tov) + ({team_abb}_opp_fga + 0.4 * {team_abb}_opp_fta - 1.07 * ({team_abb}_opp_oreb / ({team_abb}_opp_oreb + {team_abb}_dreb)) * ({team_abb}_opp_fga - {team_abb}_opp_fgm) + {team_abb}_opp_tov)) as {team_abb}_poss,
        0.5 * (({team_abb}_opp_fga + 0.4 + {team_abb}_opp_fta - 1.07 * ({team_abb}_opp_oreb / ({team_abb}_opp_oreb + {team_abb}_dreb)) * ({team_abb}_opp_fga - {team_abb}_opp_fgm) + {team_abb}_opp_tov) + ({team_abb}_fga + 0.4 * {team_abb}_fta - 1.07 * ({team_abb}_oreb / ({team_abb}_oreb + {team_abb}_opp_dreb)) * ({team_abb}_fga - {team_abb}_fgm) + {team_abb}_tov)) as {team_abb}_opp_poss,
        {team_abb}_ast / {team_abb}_fgm * 100 as {team_abb}_ast_pct,
        {team_abb}_ast / {team_abb}_tov as {team_abb}_ast_tov_ratio,
        100 * {team_abb}_ast / ({team_abb}_fga + 0.44 * {team_abb}_fta + {team_abb}_ast + {team_abb}_tov) as {team_abb}_ast_ratio,
        100 * ({team_abb}_oreb * ({team_abb}_mp / 5)) / ({team_abb}_mp * ({team_abb}_oreb + {team_abb}_opp_dreb)) as {team_abb}_oreb_pct,
        100 * ({team_abb}_dreb * ({team_abb}_mp / 5)) / ({team_abb}_mp * ({team_abb}_dreb + {team_abb}_opp_oreb)) as {team_abb}_dreb_pct,
        100 * ({team_abb}_treb * ({team_abb}_mp / 5)) / ({team_abb}_mp * ({team_abb}_treb + {team_abb}_opp_treb)) as {team_abb}_treb_pct,
        100 * {team_abb}_tov / ({team_abb}_fga + 0.44 * {team_abb}_fta + {team_abb}_tov) as {team_abb}_tov_ratio,
        ({team_abb}_fgm + 0.5 * {team_abb}_fg3m) / {team_abb}_fga as {team_abb}_efg_pct,
        {team_abb}_pts / (2 * ({team_abb}_fga + 0.44 * {team_abb}_fta)) as {team_abb}_ts_pct
        FROM(SELECT SUBSTRING(g.season_id,2,5) AS Season, SUM(g.min) AS {team_abb}_mp,
        COUNT(CASE WHEN (g.team_abbreviation_home IN {team} OR g.team_abbreviation_away IN {team}) THEN g.game_date END) AS {team_abb}_gp,
        COUNT(CASE WHEN g.team_abbreviation_home IN {team} AND g.wl_home = 'L' THEN g.wl_home WHEN g.team_abbreviation_away IN {team} AND g.wl_away = 'L' THEN g.wl_away END) AS {team_abb}_losses,
        COUNT(CASE WHEN g.team_abbreviation_home IN {team} AND g.wl_home = 'W' THEN g.wl_home WHEN g.team_abbreviation_away IN {team} AND g.wl_away = 'W' THEN g.wl_away END) AS {team_abb}_wins,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.pts_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.pts_away) END AS {team_abb}_pts,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ast_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ast_away) END AS {team_abb}_ast,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.reb_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.reb_away) END AS {team_abb}_treb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.oreb_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.oreb_away) END AS {team_abb}_oreb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.dreb_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.dreb_away) END AS {team_abb}_dreb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.stl_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.stl_away) END AS {team_abb}_stl,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.blk_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.blk_away) END AS {team_abb}_blk,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.tov_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.tov_away) END AS {team_abb}_tov,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.pf_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.pf_away) END AS {team_abb}_pf,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fga_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fga_away) END AS {team_abb}_fga,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fgm_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fgm_away) END AS {team_abb}_fgm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg_pct_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg_pct_away) END AS {team_abb}_fg_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3a_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3a_away) END AS {team_abb}_fg3a,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3m_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3m_away) END AS {team_abb}_fg3m,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3_pct_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3_pct_away) END AS {team_abb}_fg3_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fta_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fta_away) END AS {team_abb}_fta,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ftm_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ftm_away) END AS {team_abb}_ftm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ft_pct_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ft_pct_away) END AS {team_abb}_ft_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.plus_minus_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.plus_minus_away) END AS {team_abb}_pm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_paint_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_paint_away) END AS {team_abb}_pts_paint,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_2nd_chance_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_2nd_chance_away) END AS {team_abb}_pts_2nd_chance,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_fb_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_fb_away) END AS {team_abb}_pts_fb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_off_to_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_off_to_away) END AS {team_abb}_pts_off_tov,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.pts_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.pts_home) END AS {team_abb}_opp_pts,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ast_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ast_home) END AS {team_abb}_opp_ast,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.reb_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.reb_home) END AS {team_abb}_opp_treb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.oreb_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.oreb_home) END AS {team_abb}_opp_oreb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.dreb_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.dreb_home) END AS {team_abb}_opp_dreb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.stl_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.stl_home) END AS {team_abb}_opp_stl,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.blk_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.blk_home) END AS {team_abb}_opp_blk,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.tov_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.tov_home) END AS {team_abb}_opp_tov,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.pf_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.pf_home) END AS {team_abb}_opp_pf,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fga_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fga_home) END AS {team_abb}_opp_fga,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fgm_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fgm_home) END AS {team_abb}_opp_fgm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg_pct_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg_pct_home) END AS {team_abb}_opp_fg_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3a_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3a_home) END AS {team_abb}_opp_fg3a,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3m_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3m_home) END AS {team_abb}_opp_fg3m,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3_pct_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3_pct_home) END AS {team_abb}_opp_fg3_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fta_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fta_home) END AS {team_abb}_opp_fta,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ftm_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ftm_home) END AS {team_abb}_opp_ftm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ft_pct_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ft_pct_home) END AS {team_abb}_opp_ft_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.plus_minus_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.plus_minus_home) END AS {team_abb}_opp_pm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_paint_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_paint_home) END AS {team_abb}_opp_pts_paint,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_2nd_chance_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_2nd_chance_home) END AS {team_abb}_opp_pts_2nd_chance,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_fb_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_fb_home) END AS {team_abb}_opp_pts_fb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_off_to_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_off_to_home) END AS {team_abb}_opp_pts_off_tov
        FROM game as g
        JOIN other_stats as o
        ON g.game_id = o.game_id
        WHERE SUBSTRING(g.season_id,1,1) = '2' AND Season >= '1996' AND (g.team_abbreviation_home IN {team} OR g.team_abbreviation_away IN {team})
        GROUP BY Season))"""
    dataframe = pd.read_sql_query(query, con, index_col="Season")
    return dataframe

teamdata ={
"Hawks": {"Conference": "Eastern", "Division": "South East"},
"Celtics": {"Conference": "Eastern", "Division": "Atlantic"},
"Nets": {"Conference": "Eastern", "Division": "Atlantic"},
"Hornets": {"Conference": "Eastern", "Division": "South East"},
"Bulls": {"Conference": "Eastern", "Division": "Central"},
"Cavaliers": {"Conference": "Eastern", "Division": "Central"},
"Mavericks": {"Conference": "Western", "Division": "South West"},
"Nuggets": {"Conference": "Western", "Division": "North West"},
"Pistons": {"Conference": "Western", "Division": "Central"},
"Warriors": {"Conference": "Western", "Division": "Pacific"},
"Rockets": {"Conference": "Western", "Division": "South West"},
"Pacers": {"Conference": "Eastern", "Division": "Central"},
"Lakers": {"Conference": "Western", "Division": "Pacific"},
"Clippers": {"Conference": "Western", "Division": "Pacific"},
"Grizzlies": {"Conference": "Western", "Division": "South West"},
"Heat": {"Conference": "Eastern", "Division": "South East"},
"Bucks": {"Conference": "Eastern", "Division": "Central"},
"Timberwolves": {"Conference": "Western", "Division": "North West"},
"Pelicans": {"Conference": "Western", "Division": "South West"},
"Knicks": {"Conference": "Eastern", "Division": "Atlantic"},
"Thunder": {"Conference": "Western", "Division": "North West"},
"Magic": {"Conference": "Eastern", "Division": "South East"},
"76ers": {"Conference": "Eastern", "Division": "Atlantic"},
"Suns": {"Conference": "Western", "Division": "Pacific"},
"Trail Blazers": {"Conference": "Western", "Division": "North West"},
"Kings": {"Conference": "Western", "Division": "Pacific"},
"Spurs": {"Conference": "Western", "Division": "South West"},
"Raptors":  {"Conference": "Eastern", "Division": "Atlantic"},
"Jazz": {"Conference": "Western", "Division": "North West"},
"Wizards": {"Conference": "Western", "Division": "South East"}
}

teams={
"ATL":('TCB','MIH','STL','ATL'),
"BOS":('(\'BOS\')'),
"BKN":('NJN','BKN'),
"CHA":('CHN','CHA'),
"CHI":('(\'CHI\')'),
"CLE":('(\'CLE\')'),
"DAL":('(\'DAL\')'),
"DEN":('(\'DEN\')'),
"DET":('FTW', 'DET'),
"GSW":('PHW','SFW','GOS','GSW'),
"HOU":('SDR','HOU'),
"IND":('(\'IND\')'),
"LAL":('MNL','LAL'),
"LAC":('SDC', 'LAC'),
"MEM":('VAN','MEM'),
"MIA":('(\'MIA\')'),
"MIL":('(\'MIL\')'),
"MIN":('(\'MIN\')'),
"NOP":('NOH','NOK','NOP'),
"NYK":('(\'NYK\')'),
"OKC":('SEA','OKC'),
"ORL":('(\'ORL\')'),
"PHI":('SYR', 'PHI'),
"PHX":('(\'PHX\')'),
"POR":('(\'POR\')'),
"SAC":('ROC','CIN','KCK','SAC'),
"SAS":('(\'SAS\')'),
"TOR":('(\'TOR\')'),
"UTA":('NOJ','UTH', 'UTA'),
"WAS":('CHZ','BLT','CAP','WAS')
}

query = "SELECT nickname FROM team"
cur.execute(query)
teamDFs = cur.fetchall()
teamDFs = [i[0] for i in teamDFs]
Regular_Season_Dict = {}
Preseason_Dict = {} 
Playoffs_Dict = {}
League_Dict = {}

for i in teams:
    Regular_Season_Dict[i] = get_team_stats(con, teams[i], i)

League_Dict['Regular Season'] = get_league_stats(con)

team_abbs=['ATL','BOS','BKN','CHA','CHI','CLE', 'DAL', 'DEN','DET','GSW','HOU', 'IND','LAL', 'LAC', 'MEM', 'MIA', 'MIL', 'MIN','NOP',
           'NYK','OKC', 'ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']

to_concat = []
for i in team_abbs:
    to_concat.append(Regular_Season_Dict[i])
to_concat.append(League_Dict['Regular Season'])

megaDF = pd.concat(to_concat, axis=1)

megaDF = pd.concat(to_concat, axis=1)
megaDF.to_csv("NBAOverview1996-2022.csv")
