'''
The ultimate goal is to create a dashboard (Tableau at first, dash later) for the NBA's 30 teams from 1996 to 2022, a time frame chosen because it has the most complete data within the database.
First, the data will be fetched with a monstrous SQL query and converted into a dataframe. I will then use pandas to create some new columns representing some advanced statistics that were not calculated in the original database.
With all new columns created, the file can be converted into csv files to be used in Tableau. 
'''

import sqlite3 as sql
import pandas as pd
import numpy as np
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
        WHERE season_type = 'Regular Season' AND Season >= '1996'
        GROUP BY Season"""
    dataframe = pd.read_sql_query(query, con, index_col="Season")
    return dataframe

def get_team_stats(con, team, team_abb):
    # This function looks a bit complex but it just prepends the team abbreviation to each stat instead of tm so that it is easier to concatenate all of the stats into one csv for Tableau.
    # The next function does not do those so the query looks a bit cleaner.
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
        WHERE g.season_type = 'Regular Season' AND Season >= '1996' AND (g.team_abbreviation_home IN {team} OR g.team_abbreviation_away IN {team})
        GROUP BY Season))"""
    dataframe = pd.read_sql_query(query, con, index_col="Season")
    return dataframe

def get_team_stats_simple(con, team, season_type):
    # This was the earlier version of the above function that is much simpler. It does not give unique names to colums because the dataframes didn't need to be concatenated for SQLite.
    query = f"""SELECT Season, mp, gp, losses, wins, tm_pts, tm_ast, tm_treb, tm_oreb, tm_dreb, tm_stl, tm_blk, tm_tov, tm_pf, tm_fga, tm_fgm, tm_fg_pct, tm_fg3a, tm_fg3m,
        tm_fg3_pct, tm_fta, tm_ftm, tm_ft_pct, tm_pm, tm_pts_paint, tm_pts_2nd_chance, tm_pts_fb, tm_pts_off_tov, opp_pts, opp_ast, opp_treb, opp_oreb, opp_dreb, opp_stl, opp_blk,
        opp_tov, opp_pf, opp_fga, opp_fgm, opp_fg_pct, opp_fg3a, opp_fg3m, opp_fg3_pct, opp_fta, opp_ftm, opp_ft_pct, opp_pm, opp_pts_paint, opp_pts_2nd_chance, opp_pts_fb, opp_pts_off_tov,
        tm_poss, opp_poss,
        100 / (tm_poss + opp_poss) * tm_pts as ORtg,
        100 / (tm_poss + opp_poss) * opp_pts as DRtg,
        48 * ((tm_poss + opp_poss) / (2 * mp /5)) as pace,
        ast_pct, ast_tov_ratio, ast_ratio, oreb_pct, dreb_pct, treb_pct, tov_ratio, efg_pct, ts_pct
        FROM(SELECT Season, mp, gp, losses, wins, tm_pts, tm_ast, tm_treb, tm_oreb, tm_dreb, tm_stl, tm_blk, tm_tov, tm_pf, tm_fga, tm_fgm, tm_fg_pct, tm_fg3a, tm_fg3m,
        tm_fg3_pct, tm_fta, tm_ftm, tm_ft_pct, tm_pm, tm_pts_paint, tm_pts_2nd_chance, tm_pts_fb, tm_pts_off_tov, opp_pts, opp_ast, opp_treb, opp_oreb, opp_dreb, opp_stl, opp_blk,
        opp_tov, opp_pf, opp_fga, opp_fgm, opp_fg_pct, opp_fg3a, opp_fg3m, opp_fg3_pct, opp_fta, opp_ftm, opp_ft_pct, opp_pm, opp_pts_paint, opp_pts_2nd_chance, opp_pts_fb, opp_pts_off_tov,
        0.5 * ((tm_fga + 0.4 + tm_fta - 1.07 * (tm_oreb / (tm_oreb + opp_dreb)) * (tm_fga - tm_fgm) + tm_tov) + (opp_fga + 0.4 * opp_fta - 1.07 * (opp_oreb / (opp_oreb + tm_dreb)) * (opp_fga - opp_fgm) + opp_tov)) as tm_poss,
        0.5 * ((opp_fga + 0.4 + opp_fta - 1.07 * (opp_oreb / (opp_oreb + tm_dreb)) * (opp_fga - opp_fgm) + opp_tov) + (tm_fga + 0.4 * tm_fta - 1.07 * (tm_oreb / (tm_oreb + opp_dreb)) * (tm_fga - tm_fgm) + tm_tov)) as opp_poss,
        tm_ast / tm_fgm * 100 as ast_pct,
        tm_ast / tm_tov as ast_tov_ratio,
        100 * tm_ast / (tm_fga + 0.44 * tm_fta + tm_ast + tm_tov) as ast_ratio,
        100 * (tm_oreb * (mp / 5)) / (mp * (tm_oreb + opp_dreb)) as oreb_pct,
        100 * (tm_dreb * (mp / 5)) / (mp * (tm_dreb + opp_oreb)) as dreb_pct,
        100 * (tm_treb * (mp / 5)) / (mp * (tm_treb + opp_treb)) as treb_pct,
        100 * tm_tov / (tm_fga + 0.44 * tm_fta + tm_tov) as tov_ratio,
        (tm_fgm + 0.5 * tm_fg3m) / tm_fga as efg_pct,
        tm_pts / (2 * (tm_fga + 0.44 * tm_fta)) as ts_pct
        FROM(SELECT SUBSTRING(g.season_id,2,5) AS Season, SUM(g.min) AS mp,
        COUNT(CASE WHEN (g.team_abbreviation_home IN {team} OR g.team_abbreviation_away IN {team}) THEN g.game_date END) AS gp,
        COUNT(CASE WHEN g.team_abbreviation_home IN {team} AND g.wl_home = 'L' THEN g.wl_home WHEN g.team_abbreviation_away IN {team} AND g.wl_away = 'L' THEN g.wl_away END) AS losses,
        COUNT(CASE WHEN g.team_abbreviation_home IN {team} AND g.wl_home = 'W' THEN g.wl_home WHEN g.team_abbreviation_away IN {team} AND g.wl_away = 'W' THEN g.wl_away END) AS wins,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.pts_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.pts_away) END AS tm_pts,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ast_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ast_away) END AS tm_ast,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.reb_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.reb_away) END AS tm_treb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.oreb_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.oreb_away) END AS tm_oreb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.dreb_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.dreb_away) END AS tm_dreb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.stl_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.stl_away) END AS tm_stl,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.blk_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.blk_away) END AS tm_blk,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.tov_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.tov_away) END AS tm_tov,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.pf_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.pf_away) END AS tm_pf,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fga_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fga_away) END AS tm_fga,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fgm_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fgm_away) END AS tm_fgm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg_pct_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg_pct_away) END AS tm_fg_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3a_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3a_away) END AS tm_fg3a,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3m_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3m_away) END AS tm_fg3m,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3_pct_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3_pct_away) END AS tm_fg3_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fta_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fta_away) END AS tm_fta,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ftm_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ftm_away) END AS tm_ftm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ft_pct_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ft_pct_away) END AS tm_ft_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.plus_minus_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.plus_minus_away) END AS tm_pm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_paint_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_paint_away) END AS tm_pts_paint,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_2nd_chance_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_2nd_chance_away) END AS tm_pts_2nd_chance,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_fb_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_fb_away) END AS tm_pts_fb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_off_to_home) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_off_to_away) END AS tm_pts_off_tov,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.pts_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.pts_home) END AS opp_pts,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ast_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ast_home) END AS opp_ast,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.reb_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.reb_home) END AS opp_treb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.oreb_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.oreb_home) END AS opp_oreb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.dreb_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.dreb_home) END AS opp_dreb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.stl_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.stl_home) END AS opp_stl,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.blk_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.blk_home) END AS opp_blk,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.tov_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.tov_home) END AS opp_tov,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.pf_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.pf_home) END AS opp_pf,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fga_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fga_home) END AS opp_fga,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fgm_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fgm_home) END AS opp_fgm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg_pct_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg_pct_home) END AS opp_fg_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3a_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3a_home) END AS opp_fg3a,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3m_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3m_home) END AS opp_fg3m,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fg3_pct_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fg3_pct_home) END AS opp_fg3_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.fta_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.fta_home) END AS opp_fta,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ftm_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ftm_home) END AS opp_ftm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.ft_pct_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.ft_pct_home) END AS opp_ft_pct,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(g.plus_minus_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(g.plus_minus_home) END AS opp_pm,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_paint_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_paint_home) END AS opp_pts_paint,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_2nd_chance_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_2nd_chance_home) END AS opp_pts_2nd_chance,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_fb_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_fb_home) END AS opp_pts_fb,
        CASE WHEN g.team_abbreviation_home IN {team} THEN AVG(o.pts_off_to_away) WHEN g.team_abbreviation_away IN {team} THEN AVG(o.pts_off_to_home) END AS opp_pts_off_tov
        FROM game as g
        JOIN other_stats as o
        ON g.game_id = o.game_id
        WHERE g.season_type = {season_type} AND Season >= '1996' AND (g.team_abbreviation_home IN {team} OR g.team_abbreviation_away IN {team})
        GROUP BY Season))"""
    dataframe = pd.read_sql_query(query, con, index_col="Season")
    return dataframe


############################################################################################################################################
# Functions to Calculate Team Stats like Offensive/Defensive Rating and Assist Ratio
#
# Sources: 
# https://www.basketball-reference.com/about/glossary.html
# https://www.fromtherumbleseat.com/pages/advanced-basketball-statistics-formula-sheet
# https://www.espn.com/nba/hollinger/teamstats
#
# Note: Technically, many of the stats (like rebounding rates) are intended to be used for individual players, but substituting team values for player values should give an estimate of the team's stats.
# These stats also appear on https://www.nba.com/stats/teams/advanced so this seems like a legitimate way to caulcuate a team stat.  
# I also don't use any of these functions however I keep them around with sources to show where the equations are originally from.
############################################################################################################################################

def get_possessions(tm_fga, tm_fgm, tm_fta, tm_oreb, tm_dreb, tm_tov, opp_fga, opp_fgm, opp_fta, opp_oreb, opp_dreb, opp_tov):
    # Many of the calculations require normalization by possessions which was unfortunately not given by the database.
    # This requires an estimate based on the ways that a possession can end: free throws (which are often not paired with a field goal attempt, unless it is an and-one), field goal attempt, turnovers and offensive rebounds
    # Source: https://www.basketball-reference.com/about/glossary.html
    tm_poss = 0.5 * ((tm_fga + 0.4 + tm_fta - 1.07 * (tm_oreb / (tm_oreb + opp_dreb)) \
            * (tm_fga - tm_fgm) + tm_tov) + (opp_fga + 0.4 * opp_fta - 1.07 * (opp_oreb / (opp_oreb + tm_dreb)) \
            * (opp_fga - opp_fgm) + opp_tov))
    return tm_poss

def get_ORtg(tm_pts, tm_poss, opp_poss):
    # Offensive Rating, this is a measure of how many points a team scores per 100 possessions
    # Source: https://www.fromtherumbleseat.com/pages/advanced-basketball-statistics-formula-sheet
    return 100 / (tm_poss + opp_poss) * tm_pts

def get_DRtg(opp_pts, tm_poss, opp_poss):
    # Defensive Rating, this is a measure of how many points a the opposing team scores per 100 possessions
    # Source: https://www.fromtherumbleseat.com/pages/advanced-basketball-statistics-formula-sheet
    return 100 / (tm_poss + opp_poss) * opp_pts

def get_Net_Rtg(DRtg, ORtg):
    return ORtg - DRtg

def get_ast_pct(tm_ast, tm_fgm):
    # Assist Percentage
    return tm_ast / tm_fgm * 100

def get_ast_tov_ratio(ast, tov):
    # Assist to Turnover Ratio
    return ast / tov

def get_ast_ratio(tm_fga, tm_fta, tm_ast, tm_tov):
    # Assist Ratio
    # Source: https://www.espn.com/nba/hollinger/teamstats
    return 100 * tm_ast / (tm_fga + 0.44 * tm_fta + tm_ast + tm_tov)

def get_oreb_pct(tm_min, tm_oreb, opp_dreb):
    # Offensive Rebounding Percentage
    # Source: https://www.basketball-reference.com/about/glossary.html
    return 100 * (tm_oreb * (tm_min / 5)) / (tm_min * (tm_oreb + opp_dreb))

def get_dreb_pct(tm_min, tm_dreb, opp_oreb):
    # Defensive Rebounding Percentage
    # Source: https://www.basketball-reference.com/about/glossary.html
    return 100 * (tm_dreb * (tm_min / 5)) / (tm_min * (tm_dreb + opp_oreb))

def get_treb_pct(tm_min, tm_treb, opp_treb):
    # Total Rebounding Percentage
    # Source: https://www.basketball-reference.com/about/glossary.html
    return 100 * (tm_treb * (tm_min / 5)) / (tm_min * (tm_treb + opp_treb))

def get_tov_ratio(tm_fga, tm_fta, tm_tov):
    # Turnover Percentage
    # Source: https://www.espn.com/nba/hollinger/teamstats
    return 100 * tm_tov / (tm_fga + 0.44 * tm_fta + tm_tov)

def get_efg_pct(tm_fgm, tm_fg3m, tm_fga):
    # Effective Field Goal Percentage
    # Source: https://www.basketball-reference.com/about/glossary.html
    return (tm_fgm + 0.5 * tm_fg3m) / tm_fga

def get_true_shooting(tm_fga, tm_fta, tm_pts):
    # True Shooting Percentage
    # Source: https://www.basketball-reference.com/about/glossary.html
    tsa = tm_fga + 0.44 * tm_fta #True Shooting Attempts
    return tm_pts / (2 * tsa)

def get_pace(tm_poss, opp_poss, tm_min):
    # Pace is a measure of how fast a team plays the game
    # Source: https://www.basketball-reference.com/about/glossary.html
    return 48 * ((tm_poss + opp_poss) / (2 * tm_min /5))

def get_pyth_w(games, tm_pts, opp_pts):
    # Pythagorean Wins, the rmse is reported as 3.48 wins.
    # Source: https://www.basketball-reference.com/about/glossary.html
    return games * (np.power(tm_pts, 16.5) / (np.power(tm_pts, 16.5) + np.power(opp_pts, 16.5)))

############################################################################################################################################
# END Functions
############################################################################################################################################

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
"Hawks":('TCB','MIH','STL','ATL'),
"Celtics":('(\'BOS\')'),
"Nets":('NJN','BKN'),
"Hornets":('CHN','CHA'),
"Bulls":('(\'CHI\')'),
"Cavaliers":('(\'CLE\')'),
"Mavericks":('(\'DAL\')'),
"Nuggets":('(\'DEN\')'),
"Pistons":('FTW', 'DET'),
"Warriors":('PHW','SFW','GOS','GSW'),
"Rockets":('SDR','HOU'),
"Pacers":('(\'IND\')'),
"Lakers":('MNL','LAL'),
"Clippers":('SDC', 'LAC'),
"Grizzlies":('VAN','MEM'),
"Heat":('(\'MIA\')'),
"Bucks":('(\'MIL\')'),
"Timberwolves":('(\'MIN\')'),
"Pelicans":('NOH','NOK','NOP'),
"Knicks":('(\'NYK\')'),
"Thunder":('SEA','OKC'),
"Magic":('(\'ORL\')'),
"76ers":('SYR', 'PHI'),
"Suns":('(\'PHX\')'),
"Trail Blazers":('(\'POR\')'),
"Kings":('ROC','CIN','KCK','SAC'),
"Spurs":('(\'SAS\')'),
"Raptors":('(\'TOR\')'),
"Jazz":('NOJ','UTH', 'UTA'),
"Wizards":('CHZ','BLT','CAP','WAS')
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
    Regular_Season_Dict[i] = get_team_stats(con, teams[i], i, '\'Regular Season\'', 'reg')

League_Dict['Regular Season'] = get_league_stats(con,'\'Regular Season\'', 'reg')

team_abbs=['ATL','BOS','BKN','CHA','CHI','CLE', 'DAL', 'DEN','DET','GSW','HOU', 'IND','LAL', 'LAC', 'MEM', 'MIA', 'MIL', 'MIN','NOP',
           'NYK','OKC', 'ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']

to_concat = []
for i in team_abbs:
    to_concat.append(Regular_Season_Dict[i])
to_concat.append(League_Dict['Regular Season'])

megaDF = pd.concat(to_concat, axis=1)

megaDF = pd.concat(to_concat, axis=1)
megaDF.to_csv("NBAOverview1996-2022.csv")
